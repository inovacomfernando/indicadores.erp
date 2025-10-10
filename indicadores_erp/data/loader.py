"""
Data loader for monthly metrics from Supabase
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from ..auth.supabase_client import get_supabase_client
from ..auth.auth_manager import get_current_company_id

@st.cache_data(ttl=300)
def load_data():
    """
    Load monthly metrics data from Supabase for the current company

    Returns:
        pd.DataFrame: DataFrame with monthly metrics
    """
    try:
        company_id = get_current_company_id()
        
        if not company_id:
            st.error("Erro: Empresa não identificada. Faça login novamente.")
            return pd.DataFrame()

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
        
        # Ensure proper data types
        numeric_columns = ['sessions', 'first_visits', 'leads', 'web_clients', 
                          'web_revenue', 'avg_ticket', 'meta_cost', 'google_cost', 
                          'total_ads', 'cac', 'ltv', 'roi', 'tc_users', 'tc_leads',
                          'cac_ltv_ratio']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def filter_data(df, start_date=None, end_date=None):
    """
    Filter data by date range

    Args:
        df: DataFrame with monthly metrics
        start_date: Start date (optional)
        end_date: End date (optional)

    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if df.empty:
        return df

    filtered_df = df.copy()

    if start_date:
        filtered_df = filtered_df[
            (filtered_df['year'] > start_date.year) |
            ((filtered_df['year'] == start_date.year) & 
             (filtered_df['month_number'] >= start_date.month))
        ]

    if end_date:
        filtered_df = filtered_df[
            (filtered_df['year'] < end_date.year) |
            ((filtered_df['year'] == end_date.year) & 
             (filtered_df['month_number'] <= end_date.month))
        ]

    return filtered_df
