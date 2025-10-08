"""
Carregamento e preparação de dados
"""
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Carrega os dados do dashboard"""
    data = {
        'Mês': ['Mai/25', 'Jun/25', 'Jul/25', 'Ago/25', 'Set/25', 'Out/25', 'Nov/25', 'Dez/25'],
        'Sessões': [5218, 5600, 5717, 7654, 8028, 2181, 0, 0],
        'Primeira Visita': [2900, 3562, 3500, 5400, 5548, 1720, 0, 0],
        'Leads': [270, 290, 401, 600, 604, 168, 0, 0],
        'TC Usuários (%)': [9.32, 8.79, 11.46, 11.11, 10.89, 9.80, 0, 0],
        'Clientes Web': [16, 15, 18, 20, 24, 3, 0, 0],
        'TC Leads (%)': [5.93, 5.50, 4.50, 3.33, 3.97, 1.79, 0, 0],
        'Receita Web': [2114.56, 1991.31, 2591.91, 2728.92, 3393.42, 424.20, 0, 0],
        'Ticket Médio': [132.16, 132.75, 149.99, 136.45, 141.40, 141.40, 0, 0],
        'Custo Meta': [2238.52, 2328.16, 2731.39, 3476.39, 3807.17, 897.10, 0, 0],
        'Custo Google': [2934.49, 3083.29, 3194.67, 4932.45, 6127.84, 1499.88, 0, 0],
        'Total Ads': [5173.01, 5411.32, 5926.06, 8408.84, 9935.01, 2396.98, 0, 0],
        'CAC': [323.31, 360.75, 329.23, 420.44, 413.96, 798.99, 0, 0],
        'LTV': [1585.92, 1593.00, 1799.88, 1637.40, 1696.80, 1696.80, 0, 0],
        'CAC:LTV': [4.9, 4.4, 5.5, 3.9, 4.1, 2.1, 0, 0],
        'ROI (%)': [390.52, 341.57, 446.70, 289.45, 309.90, 112.37, 0, 0]
    }
    return pd.DataFrame(data)

def filter_data(df, selected_months):
    """Filtra dados pelos meses selecionados"""

    return df[df['Mês'].isin(selected_months)]









