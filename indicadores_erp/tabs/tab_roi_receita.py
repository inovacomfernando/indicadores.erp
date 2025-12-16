import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def intelligent_load_and_clean(file):
    """
    Carrega dados de um arquivo, encontra o cabeçalho correto e realiza uma limpeza básica.
    """
    try:
        if file.name.lower().endswith(('.xlsx', '.xls')):
            df_raw = pd.read_excel(file, header=None, sheet_name=0)
            header_row_index = 0
            # Tenta encontrar a linha de cabeçalho com base na contagem de não-nulos
            for i, row in df_raw.head(10).iterrows():
                if row.notna().sum() / len(row) > 0.5: # Se mais de 50% da linha for não-nula
                    header_row_index = i
                    break
            df = pd.read_excel(file, header=header_row_index)
        else:
            # Para CSV, tenta detectar o separador
            df = pd.read_csv(file, sep=None, engine='python')

        df.dropna(axis='columns', how='all', inplace=True)
        df.dropna(axis='rows', how='all', inplace=True)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
        return None

def clean_numeric_column(series: pd.Series) -> pd.Series:
    """Limpa uma coluna para garantir que ela seja numérica."""
    if series.dtype == 'object':
        series = series.astype(str).str.replace(r'[R$\s]', '', regex=True).str.replace(',', '.', regex=False)
    return pd.to_numeric(series, errors='coerce')

def render_tab_roi_receita():
    st.header("Análise de Receita e ROI")
    st.write("Faça o upload de uma planilha para analisar a performance de receita ou ROI ao longo do tempo.")

    uploaded_file = st.file_uploader("Selecione sua planilha", type=['csv', 'xlsx', 'xls'])

    if uploaded_file:
        df = intelligent_load_and_clean(uploaded_file)

        if df is None or df.empty:
            st.warning("Não foi possível carregar dados da planilha ou a planilha está vazia.")
            return

        st.info("Planilha carregada com sucesso! Agora, configure a sua análise.")
        
        cols = df.columns.tolist()
        
        # --- PAINEL DE CONFIGURAÇÃO ---
        with st.expander("Configurar Colunas para Análise", expanded=True):
            col_periodo = st.selectbox("Selecione a coluna de Período/Data:", cols)
            col_valor = st.selectbox("Selecione a coluna de Valor (Receita/ROI):", cols, index=len(cols)-1 if len(cols)>1 else 0)

        if not col_periodo or not col_valor:
            st.warning("Por favor, selecione as colunas de período e valor para continuar.")
            return
            
        try:
            # --- PROCESSAMENTO DOS DADOS ---
            analysis_df = df[[col_periodo, col_valor]].copy()
            analysis_df.dropna(subset=[col_periodo, col_valor], inplace=True)

            # Converter coluna de período para datetime
            analysis_df['periodo'] = pd.to_datetime(analysis_df[col_periodo], errors='coerce')
            
            # Limpar e converter coluna de valor
            analysis_df['valor'] = clean_numeric_column(analysis_df[col_valor])
            
            # Verificar se houve problemas na conversão
            if analysis_df['periodo'].isnull().any():
                st.warning("Algumas datas não puderam ser reconhecidas e foram ignoradas. Verifique o formato da coluna de período.")
            if analysis_df['valor'].isnull().any():
                st.warning("Alguns valores não puderam ser convertidos para número e foram ignorados. Verifique a coluna de valor.")

            analysis_df.dropna(subset=['periodo', 'valor'], inplace=True)
            
            if analysis_df.empty:
                st.error("Nenhum dado válido para análise após a limpeza. Verifique suas seleções e a qualidade dos dados na planilha.")
                return

            # Ordenar por período e calcular acumulado
            analysis_df.sort_values('periodo', inplace=True)
            analysis_df['acumulado'] = analysis_df['valor'].cumsum()
            analysis_df['periodo_str'] = analysis_df['periodo'].dt.strftime('%Y-%m-%d') # Coluna para o gráfico

            # --- EXIBIÇÃO DOS RESULTADOS ---
            st.success("Análise concluída!")

            # KPIs
            total_acumulado = analysis_df['acumulado'].iloc[-1]
            media_mensal = analysis_df['valor'].mean()
            
            col1, col2 = st.columns(2)
            col1.metric("Receita Total Acumulada", f"R$ {total_acumulado:,.2f}")
            col2.metric("Média de Receita por Período", f"R$ {media_mensal:,.2f}")

            # Gráficos
            st.subheader("Performance de Receita Mensal")
            fig_mensal = px.bar(analysis_df, x='periodo_str', y='valor', title="Receita por Período", labels={'periodo_str': 'Período', 'valor': 'Valor'})
            st.plotly_chart(fig_mensal, use_container_width=True)

            st.subheader("Crescimento Acumulado da Receita")
            fig_acumulado = px.line(analysis_df, x='periodo_str', y='acumulado', title="Receita Acumulada ao Longo do Tempo", markers=True, labels={'periodo_str': 'Período', 'acumulado': 'Valor Acumulado'})
            st.plotly_chart(fig_acumulado, use_container_width=True)

            # Tabela de dados
            with st.expander("Ver dados processados"):
                st.dataframe(analysis_df[['periodo', 'valor', 'acumulado']])

        except Exception as e:
            st.error(f"Ocorreu um erro durante a análise: {e}")
            st.error("Verifique se as colunas selecionadas são adequadas para esta análise (uma para datas/períodos e outra para valores numéricos).")

