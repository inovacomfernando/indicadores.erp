"""
Authentication manager for Streamlit app
"""
import streamlit as st
from indicadores_erp.auth.supabase_client import get_supabase_client

def init_auth_state():
    """Initialize authentication state in session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'company_id' not in st.session_state:
        st.session_state.company_id = None

def sign_up(email: str, password: str, company_name: str):
    """
    Sign up a new user

    Args:
        email: User email
        password: User password
        company_name: Company name

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        supabase = get_supabase_client()

        # Criar empresa primeiro
        company_response = supabase.table('companies').insert({
            'name': company_name
        }).execute()

        if not company_response.data:
            return False, "Erro ao criar empresa. Tente novamente."

        company_id = company_response.data[0]['id']

        # Criar usuário com company_id nos metadados
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "company_id": company_id
                }
            }
        })

        if response.user:
            return True, "Cadastro realizado com sucesso! Faça login para continuar."

        return False, "Erro no cadastro. Tente novamente."

    except Exception as e:
        return False, f"Erro no cadastro: {str(e)}"

def sign_in(email: str, password: str):
    """
    Sign in a user

    Args:
        email: User email
        password: User password

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        supabase = get_supabase_client()

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user:
            st.session_state.authenticated = True
            st.session_state.user = response.user

            company_id = response.user.user_metadata.get('company_id')
            st.session_state.company_id = company_id

            return True, "Login realizado com sucesso!"

        return False, "Erro no login. Verifique suas credenciais."

    except Exception as e:
        return False, f"Erro no login: {str(e)}"

def sign_out():
    """Sign out the current user"""
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()

        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.company_id = None

        return True, "Logout realizado com sucesso!"

    except Exception as e:
        return False, f"Erro no logout: {str(e)}"

def is_authenticated() -> bool:
    """
    Check if user is authenticated

    Returns:
        bool: True if authenticated, False otherwise
    """
    return st.session_state.get('authenticated', False)

def get_current_company_id():
    """
    Get current user's company ID

    Returns:
        str: Company ID or None
    """
    return st.session_state.get('company_id')

