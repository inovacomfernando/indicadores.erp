"""
Tab 3: Funil de Conversão
"""
import streamlit as st
from utils.charts import (
    criar_grafico_funil,
    criar_grafico_linha_com_benchmark
)


def render_tab_conversao(df_filtered, benchmarks):
    """
    Renderiza a tab de conversão
    
    Args:
        df_filtered: DataFrame filtrado
        benchmarks: Dict com benchmarks
    """
    st.subheader("Funil de Conversão")
    
    # Métricas do último mês
    ultimo_mes = df_filtered.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sessões", f"{ultimo_mes['Sessões']:,.0f}")
    with col2:
        st.metric("Leads", f"{ultimo_mes['Leads']:,.0f}")
    with col3:
        st.metric("Clientes", f"{ultimo_mes['Clientes Web']:,.0f}")
    with col4:
        st.metric("Receita", f"R$ {ultimo_mes['Receita Web']:,.2f}")
    
    # Gráfico de funil
    fig1 = criar_grafico_funil(
        labels=['Sessões', 'Primeira Visita', 'Leads', 'Clientes'],
        values=[
            ultimo_mes['Sessões'],
            ultimo_mes['Primeira Visita'],
            ultimo_mes['Leads'],
            ultimo_mes['Clientes Web']
        ],
        colors=['#073763', '#3b82f6', '#8b5cf6', '#10b981'],
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Taxa de Conversão: Usuários → Leads")
        fig2 = criar_grafico_linha_com_benchmark(
            df=df_filtered,
            x_col='Mês',
            y_col='TC Usuários (%)',
            color='#3b82f6',
            benchmark_min=benchmarks['TC Usuários (%)']['min'],
            benchmark_max=benchmarks['TC Usuários (%)']['max'],
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("### Taxa de Conversão: Leads → Vendas")
        fig3 = criar_grafico_linha_com_benchmark(
            df=df_filtered,
            x_col='Mês',
            y_col='TC Leads (%)',
            color='#10b981',
            benchmark_min=benchmarks['TC Leads (%)']['min'],
            benchmark_max=benchmarks['TC Leads (%)']['max'],
            height=300
        )
        st.plotly_chart(fig3, use_container_width=True)