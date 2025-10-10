"""
Login page
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from auth.auth_manager import sign_in, sign_up, init_auth_state

def render_login_page():
    """Render login/signup page"""
    init_auth_state()

    st.markdown("""
        <style>
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    st.title("📊 Dashboard Marketing - SaaS ERP")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Login", "Cadastro"])

    with tab1:
        st.subheader("Fazer Login")

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="seu@email.com")
            password = st.text_input("Password", type="password", placeholder="Sua senha")
            submit = st.form_submit_button("Entrar", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Preencha todos os campos")
                else:
                    success, message = sign_in(email, password)

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

    with tab2:
        st.subheader("Criar Conta")

        with st.form("signup_form"):
            company_name = st.text_input("Nome da Empresa", placeholder="Minha Empresa")
            email = st.text_input("Email", placeholder="seu@email.com", key="signup_email")
            password = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres", key="signup_password")
            password_confirm = st.text_input("Confirmar Senha", type="password", placeholder="Repita sua senha")
            submit = st.form_submit_button("Criar Conta", use_container_width=True)

            if submit:
                if not company_name or not email or not password or not password_confirm:
                    st.error("Preencha todos os campos")
                elif password != password_confirm:
                    st.error("As senhas não coincidem")
                elif len(password) < 6:
                    st.error("A senha deve ter no mínimo 6 caracteres")
                else:
                    success, message = sign_up(email, password, company_name)

                    if success:
                        st.success(message)
                    else:
                        st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)
