"""
Arquivo principal refatorado
"""
import streamlit as st

# Imports dos módulosfrom config.styles import get_custom_css
from data.loader import load_data, filter_data
from components.header import render_header, render_sidebar
from components.metrics import render_main_metrics
from components.alerts import render_main_alerts

# Imports das tabs
from tabs.tab_resultados import render_tab_resultados
from tabs.tab_financeiro import render_tab_financeiro
from tabs.tab_conversao import render_tab_conversao
from tabs.tab_evolucao import render_tab_evolucao
from tabs.tab_forecast import render_tab_forecast
from tabs.tab_benchmarks import render_tab_benchmarks
from tabs.tab_contador import render_tab_contador
from tabs.tab_recomendacoes import render_tab_recomendacoes
from tabs.tab_roi_receita import render_tab_roi_receita

# Alias para benchmarks (para usar em minúsculo no código)
benchmarks = BENCHMARKS

# Configuração da página
st.set_page_config(**PAGE_CONFIG)

# CSS customizado
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Carregar dados
df = load_data()

# Renderizar header
render_header()

# Renderizar sidebar e obter filtros
selected_months = render_sidebar(df)

# Filtrar dados
df_filtered = filter_data(df, selected_months)

# Métricas principais
render_main_metrics(df_filtered)

# Alertas dinâmicos (agora recebe o DataFrame)
render_main_alerts(df_filtered)

# Criação das tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Resultados",
    "💰 Financeiro",
    "🎯 Conversão",
    "📈 Evolução",
    "🔮 Forecast",
    "📏 Benchmarks",
    "🧮 Contador",
    "💡 Recomendações",
    "💵 ROI em Receita"
])

with tab1:
    render_tab_resultados(df_filtered, benchmarks)

with tab2:
    render_tab_financeiro(df_filtered, benchmarks)

with tab3:
    render_tab_conversao(df_filtered, benchmarks)

with tab4:
    render_tab_evolucao(df_filtered)

with tab5:
    render_tab_forecast(df_filtered)

with tab6:
    render_tab_benchmarks(df_filtered, benchmarks)

with tab7:
    render_tab_contador()

with tab8:
    render_tab_recomendacoes(df_filtered, benchmarks)

with tab9:
    # Aqui vamos passar o df filtrado para enriquecer os insights de ROI
    render_tab_roi_receita(df_filtered)

# Footer
st.markdown("---")
st.caption("Dashboard de Marketing - SaaS ERP | Atualizado em Dezembro 2025")