"""
Arquivo principal refatorado
"""
import streamlit as st

# Imports dos módulos
from config.settings import PAGE_CONFIG, BENCHMARKS
from config.styles import get_custom_css
from data.loader import load_data, filter_data
from components.header import render_header, render_sidebar
from components.metrics import render_main_metrics
from components.alerts import render_main_alerts


# Imports das tabs
from tabs.tab_evolucao import render_tab_evolucao
from tabs.tab_financeiro import render_tab_financeiro
from tabs.tab_conversao import render_tab_conversao
from tabs.tab_benchmarks import render_tab_benchmarks
from tabs.tab_recomendacoes import render_tab_recomendacoes
from tabs.tab_forecast import render_tab_forecast
from tabs.tab_contador import render_tab_contador

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

# Insights positivos (opcional - descomente se quiser exibir)
# render_insights(df_filtered)

# Tabs
tabs = st.tabs([
    "📈 Evolução", 
    "💰 Financeiro", 
    "🎯 Conversão", 
    "📊 Benchmarks", 
    "📋 Recomendações", 
    "🔮 Forecast",
    "🤝 Parceria Contador"
])

with tabs[0]:
    render_tab_evolucao(df_filtered)

with tabs[1]:
    render_tab_financeiro(df_filtered, BENCHMARKS)

with tabs[2]:
    render_tab_conversao(df_filtered, BENCHMARKS)

with tabs[3]:
    render_tab_benchmarks(df_filtered, BENCHMARKS)

with tabs[4]:
    render_tab_recomendacoes()

with tabs[5]:
    render_tab_forecast(df)

with tabs[6]:
    render_tab_contador(df_filtered)

# Footer
st.markdown("---")
st.caption("Dashboard de Marketing - SaaS ERP | Atualizado em Outubro 2025")



