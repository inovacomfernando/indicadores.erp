"""
Carregamento e preparação de dados
"""
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Carrega os dados do dashboard"""
    data = {
        'Mês': ['Mai/25', 'Jun/25', 'Jul/25', 'Ago/25', 'Set/25'],
        'Sessões': [5218, 5600, 5717, 7654, 8028],
        'Primeira Visita': [2900, 3562, 3500, 5400, 5548],
        'Leads': [270, 290, 401, 600, 604],
        'TC Usuários (%)': [9.32, 8.79, 11.46, 11.11, 10.89],
        'Clientes Web': [16, 15, 18, 20, 24],
        'TC Leads (%)': [5.93, 5.50, 4.50, 3.33, 3.97],
        'Receita Web': [2114.56, 1991.31, 2591.91, 2728.92, 3393.42],
        'Ticket Médio': [132.16, 132.75, 149.99, 136.45, 141.40],
        'Custo Meta': [2238.52, 2328.16, 2731.39, 3476.39, 3807.17],
        'Custo Google': [2934.49, 3083.29, 3194.67, 4932.45, 6127.84],
        'Total Ads': [5173.01, 5411.32, 5926.06, 8408.84, 9935.01],
        'CAC': [323.31, 360.75, 329.23, 420.44, 413.96],
        'LTV': [1585.92, 1593.00, 1799.88, 1637.40, 1696.80],
        'CAC:LTV': [4.9, 4.4, 5.5, 3.9, 4.1],
        'ROI (%)': [390.52, 341.57, 446.70, 289.45, 309.90]
    }
    return pd.DataFrame(data)

def filter_data(df, selected_months):
    """Filtra dados pelos meses selecionados"""
    return df[df['Mês'].isin(selected_months)]