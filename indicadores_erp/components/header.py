"""
Componentes de header e sidebar
"""
import streamlit as st

def render_header():
    """Renderiza o header principal"""
    st.markdown('<div class="main-header">📊 Dashboard de Marketing - SaaS ERP</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Análise de Performance: Maio - Setembro 2025</div>', 
                unsafe_allow_html=True)

def render_sidebar(df):
    """Renderiza a sidebar com filtros"""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/073763/ffffff?text=SaaS+ERP", 
                 use_container_width=True)
        st.markdown("---")
        
        st.subheader("Filtros")
        selected_months = st.multiselect(
            "Selecione os meses:",
            options=df['Mês'].tolist(),
            default=df['Mês'].tolist()
        )
        
        st.markdown("---")
        st.subheader("Sobre")
        st.info("""
        Dashboard interativo para análise de KPIs de marketing digital 
        com benchmarks do setor de SaaS ERP.
        """)
        
        st.markdown("---")
        st.caption("Desenvolvido para análise estratégica de marketing")
        
        return selected_months