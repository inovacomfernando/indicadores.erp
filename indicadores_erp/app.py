"""
Arquivo principal refatorado com autenticação
"""
import streamlit as st

from config.settings import PAGE_CONFIG, BENCHMARKS
from config.styles import get_custom_css
from data.loader import load_data, filter_data
from components.header import render_header, render_sidebar
from components.metrics import render_main_metrics
from components.alerts import render_main_alerts

from tabs.tab_evolucao import render_tab_evolucao
from tabs.tab_financeiro import render_tab_financeiro
from tabs.tab_conversao import render_tab_conversao
from tabs.tab_benchmarks import render_tab_benchmarks
from tabs.tab_recomendacoes import render_tab_recomendacoes
from tabs.tab_forecast import render_tab_forecast
from tabs.tab_contador import render_tab_contador

from auth.auth_manager import init_auth_state, is_authenticated, sign_out, get_current_company_id
from pages.login import render_login_page
from pages.data_entry import render_data_entry_page
from pages.admin import render_admin_page

st.set_page_config(**PAGE_CONFIG)

st.markdown(get_custom_css(), unsafe_allow_html=True)

init_auth_state()

if not is_authenticated():
    render_login_page()
else:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Menu")

        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("📝 Cadastrar Métricas", use_container_width=True):
            st.session_state.page = "data_entry"
            st.rerun()

        if st.button("⚙️ Administração", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

        st.markdown("---")

        if st.button("🚪 Sair", use_container_width=True):
            success, message = sign_out()
            if success:
                st.rerun()

    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

    page = st.session_state.page

    if page == "data_entry":
        render_data_entry_page()
    elif page == "admin":
        render_admin_page()
    else:
        company_id = get_current_company_id()

        df = load_data(company_id)

        if df.empty:
            st.warning("⚠️ Nenhuma métrica cadastrada ainda. Use o menu 'Cadastrar Métricas' para adicionar dados.")
        else:
            render_header()

            selected_months = render_sidebar(df)

            df_filtered = filter_data(df, selected_months)

            render_main_metrics(df_filtered)

            render_main_alerts(df_filtered)

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

            st.markdown("---")
            st.caption("Dashboard de Marketing - SaaS ERP | Atualizado em Outubro 2025")



