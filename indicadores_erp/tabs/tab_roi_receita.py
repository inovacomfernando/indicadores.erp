import streamlit as st
import pandas as pd
import re

@st.cache_data
def intelligent_load_and_clean(file):
    """
    Carrega dados de um arquivo, encontra o cabeçalho correto e realiza uma limpeza de tipos inteligente.
    """
    df = None
    if file.name.lower().endswith(('.xlsx', '.xls')):
        df_raw = pd.read_excel(file, header=None, sheet_name=0)
        header_row_index = 0
        for i, row in df_raw.head(10).iterrows():
            if row.notna().sum() / df_raw.shape[1] > 0.5:
                numeric_count = pd.to_numeric(row, errors='coerce').notna().sum()
                if numeric_count / row.notna().sum() < 0.5:
                    header_row_index = i
                    break
        df = pd.read_excel(file, header=header_row_index, sheet_name=0)
    else:
        df = pd.read_csv(file, encoding='utf-8', sep=None, engine='python')

    df.dropna(axis='columns', how='all', inplace=True)
    df.dropna(axis='rows', how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Remove colunas 'Unnamed'
    df.reset_index(drop=True, inplace=True)
    
    return df

@st.cache_data
def run_cohort_analysis(df: pd.DataFrame):
    """
    Transforma o DataFrame em um formato de coorte e calcula o ROI mensal e acumulado.
    """
    if df.empty:
        return pd.DataFrame()

    # A primeira coluna é a safra (cohort)
    cohort_col = df.columns[0]
    df.rename(columns={cohort_col: 'safra'}, inplace=True)
    
    # Derreter o dataframe para o formato longo
    df_long = df.melt(id_vars='safra', var_name='mes', value_name='valor_roi')
    
    # Limpeza e conversão de tipos
    # Extrai o número do mês (ex: de 'Mês 1' para 1)
    df_long['mes_num'] = df_long['mes'].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)
    
    # Limpa a coluna de valor (remove 'R$', espaços, e converte para float)
    if df_long['valor_roi'].dtype == 'object':
        df_long['valor_roi'] = df_long['valor_roi'].astype(str).str.replace(r'[R$\s]', '', regex=True)
        df_long['valor_roi'] = df_long['valor_roi'].str.replace(',', '.').astype(float)
    
    df_long.dropna(subset=['valor_roi'], inplace=True)
    df_long.sort_values(by=['safra', 'mes_num'], inplace=True)
    
    # Calcula o ROI acumulado para cada safra
    df_long['roi_acumulado'] = df_long.groupby('safra')['valor_roi'].cumsum()
    
    return df_long

def render_tab_roi_receita():
    st.header("Análise de Performance de Safra (Cohort)")
    st.write("Acompanhe o ROI (Retorno sobre Investimento) mensal e acumulado de cada safra.")

    uploaded_file = st.file_uploader("Faça o upload da sua planilha de ROI", type=['csv', 'xlsx'])
    
    if uploaded_file:
        try:
            df_cleaned = intelligent_load_and_clean(uploaded_file)
            
            if df_cleaned.empty:
                st.warning("Não foi possível encontrar dados válidos na planilha."); return

            df_cohort = run_cohort_analysis(df_cleaned)

            if df_cohort.empty:
                st.warning("A análise de coorte não pôde ser gerada. Verifique a estrutura da sua planilha."); return

            st.success("Análise de coorte processada com sucesso!")

            # Filtro de Safras
            all_cohorts = df_cohort['safra'].unique()
            selected_cohorts = st.multiselect("Selecione as safras para visualizar:", options=all_cohorts, default=all_cohorts)
            
            if not selected_cohorts:
                st.info("Selecione pelo menos uma safra para visualizar os gráficos.")
                return

            df_filtered = df_cohort[df_cohort['safra'].isin(selected_cohorts)]

            # Gráficos
            st.subheader("ROI Acumulado por Safra")
            st.line_chart(df_filtered, x='mes_num', y='roi_acumulado', color='safra')

            st.subheader("ROI Mensal por Safra")
            st.line_chart(df_filtered, x='mes_num', y='valor_roi', color='safra')
            
            st.subheader("Dados Detalhados da Análise")
            st.dataframe(df_filtered)

        except Exception as e:
            st.error(f"Ocorreu um erro inesperado durante a análise: {e}")
            st.error("Por favor, verifique se a estrutura da sua planilha corresponde a um formato de coorte (ex: primeira coluna com a safra, colunas seguintes com os valores mensais).")

