"""
Tab 4: Comparação com Benchmarks
"""
import streamlit as st
import pandas as pd


def render_tab_benchmarks(df_filtered, benchmarks):
    """
    Renderiza a tab de benchmarks
    
    Args:
        df_filtered: DataFrame filtrado
        benchmarks: Dict com benchmarks
    """
    st.subheader("Comparação com Benchmarks SaaS ERP")
    
    benchmark_data = pd.DataFrame({
        'Métrica': [
            'TC Usuários → Leads',
            'TC Leads → Vendas',
            'CAC',
            'CAC:LTV',
            'ROI',
            'Ticket Médio'
        ],
        'Sua Média': [
            f"{df_filtered['TC Usuários (%)'].mean():.2f}%",
            f"{df_filtered['TC Leads (%)'].mean():.2f}%",
            f"R$ {df_filtered['CAC'].mean():.2f}",
            f"{df_filtered['CAC:LTV'].mean():.1f}:1",
            f"{df_filtered['ROI (%)'].mean():.1f}%",
            f"R$ {df_filtered['Ticket Médio'].mean():.2f}"
        ],
        'Benchmark': [
            '8-15%',
            '4.5-6%',
            'R$ 250-500',
            '≥3:1 (ideal 4-7:1)',
            '300-500%',
            'R$ 120-200'
        ],
        'Status': [
            '✅ Na meta',
            '⚠️ Limítrofe',
            '✅ Aceitável',
            '⚠️ Declínio',
            '✅ Bom',
            '✅ Normal'
        ]
    })
    
    st.dataframe(benchmark_data, use_container_width=True, hide_index=True)