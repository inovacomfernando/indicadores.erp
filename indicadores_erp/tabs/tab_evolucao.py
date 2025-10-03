"""
Tab 1: Evolução de Leads e Clientes
"""
import streamlit as st
from utils.charts import (
    criar_grafico_linha,
    criar_grafico_barras,
    criar_grafico_barras_com_texto
)


def render_tab_evolucao(df_filtered):
    """
    Renderiza a tab de evolução
    
    Args:
        df_filtered: DataFrame filtrado pelos meses selecionados
    """
    st.subheader("Evolução de Leads e Clientes")
    
    # Gráfico principal: Evolução de Leads e Clientes
    fig1 = criar_grafico_linha(
        df=df_filtered,
        x_col='Mês',
        y_cols=['Leads', 'Clientes Web'],
        names=['Leads', 'Clientes'],
        colors=['#3b82f6', '#10b981'],
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Duas colunas para gráficos secundários
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tráfego do Site")
        fig2 = criar_grafico_barras(
            df=df_filtered,
            x_col='Mês',
            y_cols=['Sessões', 'Primeira Visita'],
            names=['Total Sessões', 'Primeira Visita'],
            colors=['#073763', '#3b82f6'],
            height=350,
            barmode='group'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("Receita Web Mensal")
        fig3 = criar_grafico_barras_com_texto(
            df=df_filtered,
            x_col='Mês',
            y_col='Receita Web',
            color='#10b981',
            height=350,
            formato='R$ {:.0f}'
        )
        st.plotly_chart(fig3, use_container_width=True)