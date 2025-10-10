"""
Carregamento e preparação de dados
"""
import pandas as pd
import streamlit as st
from datetime import datetime
from auth.supabase_client import get_supabase_client

@st.cache_data(ttl=300)
def load_data(company_id: str = None):
    """
    Carrega os dados do dashboard do Supabase

    Args:
        company_id: ID da empresa (obrigatório para dados filtrados)

    Returns:
        DataFrame com os dados das métricas
    """
    if not company_id:
        return pd.DataFrame()

    try:
        supabase = get_supabase_client()

        response = supabase.table('monthly_metrics')\
            .select('*')\
            .eq('company_id', company_id)\
            .order('year', desc=False)\
            .order('month_number', desc=False)\
            .execute()

        if not response.data:
            return pd.DataFrame()

        df = pd.DataFrame(response.data)

        df_formatted = pd.DataFrame({
            'Mês': df['month'],
            'Sessões': df['sessions'],
            'Primeira Visita': df['first_visits'],
            'Leads': df['leads'],
            'TC Usuários (%)': df['tc_users'],
            'Clientes Web': df['web_clients'],
            'TC Leads (%)': df['tc_leads'],
            'Receita Web': df['web_revenue'],
            'Ticket Médio': df['avg_ticket'],
            'Custo Meta': df['meta_cost'],
            'Custo Google': df['google_cost'],
            'Total Ads': df['total_ads'],
            'CAC': df['cac'],
            'LTV': df['ltv'],
            'CAC:LTV': df['cac_ltv_ratio'],
            'ROI (%)': df['roi']
        })

        df_formatted.attrs['carregado_em'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return df_formatted

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()


def filter_data(df, selected_months):
    """Filtra dados pelos meses selecionados"""
    return df[df['Mês'].isin(selected_months)]


def get_data_info(df):
    """
    Retorna informações sobre quando os dados foram carregados
    
    Returns:
        str: Timestamp do carregamento
    """
    return df.attrs.get('carregado_em', 'Desconhecido')


def force_reload_data(company_id: str = None):
    """
    Força o recarregamento dos dados limpando o cache

    Args:
        company_id: ID da empresa
    """
    st.cache_data.clear()
    return load_data(company_id)




