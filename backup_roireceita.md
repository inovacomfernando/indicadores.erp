import streamlit as st
import pandas as pd
import plotly.express as px

def clean_numeric_column(series: pd.Series) -> pd.Series:
    """Limpa uma coluna para garantir que ela seja numérica, removendo R$, espaços e ajustando a vírgula decimal."""
    if series.dtype == 'object' or pd.api.types.is_categorical_dtype(series):
        series = series.astype(str).str.replace(r'[R$\s]', '', regex=True).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    return pd.to_numeric(series, errors='coerce')

def render_tab_roi_receita():
    st.header("Análise de Receita e ROI")
    st.write("Faça o upload de uma planilha para analisar a performance de receita ou ROI ao longo do tempo.")

    uploaded_file = st.file_uploader("Selecione sua planilha", type=['csv', 'xlsx', 'xls'])

    if uploaded_file:
        try:
            if uploaded_file.name.lower().endswith(('.xlsx', '.xls')):
                df_raw = pd.read_excel(uploaded_file, engine='openpyxl')
            else:
                df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
            
            df_raw.dropna(axis='columns', how='all', inplace=True)
            df_raw.dropna(axis='rows', how='all', inplace=True)
            df_raw = df_raw.loc[:, ~df_raw.columns.str.contains('^Unnamed')]

        except Exception as e:
            st.error(f"Erro ao ler a planilha: {e}")
            st.warning("Verifique se o arquivo não está corrompido e se o formato é suportado.")
            return

        if df_raw.empty:
            st.warning("A planilha está vazia ou não foi possível extrair dados.")
            return

        with st.expander("Pré-visualização dos dados carregados", expanded=False):
            st.info("Verifique abaixo as primeiras linhas da sua planilha para garantir que a leitura foi bem-sucedida.")
            st.dataframe(df_raw.head())

        # --- PAINEL DE CONFIGURAÇÃO ---
        st.markdown("---")
        st.subheader("Configure sua Análise")
        
        cols = df_raw.columns.tolist()
        col_periodo = st.selectbox("1. Selecione a coluna de Período/Data:", cols)
        col_valor = st.selectbox("2. Selecione a coluna de Valor (Receita/ROI):", cols, index=len(cols)-1 if len(cols)>1 else 0)

        if st.button("Analisar Dados", type="primary"):
            if not col_periodo or not col_valor:
                st.warning("Por favor, selecione as colunas de período e valor para continuar.")
                return
            
            try:
                # --- PROCESSAMENTO E LIMPEZA DOS DADOS ---
                analysis_df = df_raw[[col_periodo, col_valor]].copy()
                analysis_df.dropna(subset=[col_periodo, col_valor], inplace=True)

                # Converter coluna de período para datetime
                analysis_df['periodo'] = pd.to_datetime(analysis_df[col_periodo], errors='coerce')
                
                # Limpar e converter coluna de valor
                analysis_df['valor'] = clean_numeric_column(analysis_df[col_valor])
                
                # Remover linhas onde a conversão falhou
                analysis_df.dropna(subset=['periodo', 'valor'], inplace=True)
                
                if analysis_df.empty:
                    st.error("Nenhum dado válido para análise após a limpeza. Verifique suas seleções e a qualidade dos dados na planilha (ex: formato de data, valores numéricos).")
                    return

                # --- AGRUPAMENTO POR MÊS PARA GARANTIR FIDELIDADE ---
                analysis_df['mes_ano'] = analysis_df['periodo'].dt.to_period('M')
                monthly_df = analysis_df.groupby('mes_ano').agg(valor_total=('valor', 'sum')).reset_index()
                monthly_df['mes_ano_str'] = monthly_df['mes_ano'].dt.strftime('%Y-%m')
                monthly_df.sort_values('mes_ano', inplace=True)

                # Calcular acumulado sobre os dados mensais
                monthly_df['acumulado'] = monthly_df['valor_total'].cumsum()

                # --- EXIBIÇÃO DOS RESULTADOS ---
                st.success("Análise concluída com sucesso!")
                st.markdown("---")

                # KPIs
                total_acumulado = monthly_df['acumulado'].iloc[-1]
                media_mensal = monthly_df['valor_total'].mean()
                
                col1, col2 = st.columns(2)
                col1.metric("Receita Total Acumulada", f"R$ {total_acumulado:,.2f}")
                col2.metric("Média de Receita por Mês", f"R$ {media_mensal:,.2f}")

                # Gráficos
                st.subheader("Performance de Receita Mensal")
                fig_mensal = px.bar(monthly_df, x='mes_ano_str', y='valor_total', title="Receita por Mês", labels={'mes_ano_str': 'Mês', 'valor_total': 'Valor Total'})
                st.plotly_chart(fig_mensal, use_container_width=True)

                st.subheader("Crescimento Acumulado da Receita")
                fig_acumulado = px.line(monthly_df, x='mes_ano_str', y='acumulado', title="Receita Acumulada ao Longo do Tempo", markers=True, labels={'mes_ano_str': 'Mês', 'acumulado': 'Valor Acumulado'})
                st.plotly_chart(fig_acumulado, use_container_width=True)

                # Tabela de dados
                with st.expander("Ver dados processados e agrupados por mês"):
                    display_df = monthly_df[['mes_ano_str', 'valor_total', 'acumulado']].copy()
                    display_df.rename(columns={'mes_ano_str': 'Mês', 'valor_total': 'Valor Total no Mês', 'acumulado': 'Valor Acumulado'}, inplace=True)
                    st.dataframe(display_df)

            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise: {e}")
                st.error("Verifique se as colunas selecionadas são adequadas (uma para datas, outra para valores).")
