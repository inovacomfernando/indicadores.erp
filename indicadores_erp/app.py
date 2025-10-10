"""
Main Streamlit application
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from auth.auth_manager import init_auth_state, is_authenticated, sign_out, get_current_company_id
from data.loader import load_data, filter_data
from pages.login import render_login_page
from pages.data_entry import render_data_entry_page
from pages.admin import render_admin_page

# Page configuration
st.set_page_config(
    page_title="Dashboard Marketing - SaaS ERP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
init_auth_state()

# Show login page if not authenticated
if not is_authenticated():
    render_login_page()
    st.stop()

# Sidebar navigation
with st.sidebar:
    st.title("📊 Dashboard Marketing")
    st.markdown("---")
    
    # User info
    if st.session_state.user:
        st.markdown(f"**Usuário:** {st.session_state.user.email}")
    
    st.markdown("---")
    
    # Navigation menu
    page = st.radio(
        "Navegação",
        ["📈 Dashboard", "📝 Cadastrar Métricas", "⚙️ Administração"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Sair", use_container_width=True):
        success, message = sign_out()
        if success:
            st.rerun()

# Main content based on selected page
if page == "📈 Dashboard":
    st.title("📈 Dashboard de Marketing")
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.info("📊 Nenhum dado disponível. Use o menu 'Cadastrar Métricas' para adicionar dados.")
    else:
        # Display metrics and charts here
        st.success(f"✅ {len(df)} registros carregados com sucesso!")
        
        # Show data preview
        st.subheader("Prévia dos Dados")
        st.dataframe(df, use_container_width=True)

elif page == "📝 Cadastrar Métricas":
    render_data_entry_page()

elif page == "⚙️ Administração":
    render_admin_page()


