"""
Tab 2: Análise Financeira
"""
import streamlit as st
from utils.charts import (
    criar_grafico_barras,
    criar_grafico_area
)


def render_tab_financeiro(df_filtered, benchmarks):
    """
    Renderiza a tab financeira
    
    Args:
        df_filtered: DataFrame filtrado
        benchmarks: Dict com benchmarks
    """
    st.subheader("Análise Financeira")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### CAC vs LTV")
        fig1 = criar_grafico_barras(
            df=df_filtered,
            x_col='Mês',
            y_cols=['CAC', 'LTV'],
            names=['CAC', 'LTV'],
            colors=['#ef4444', '#10b981'],
            height=350,
            barmode='group'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### Investimento em Ads")
        fig2 = criar_grafico_barras(
            df=df_filtered,
            x_col='Mês',
            y_cols=['Custo Meta', 'Custo Google'],
            names=['Meta Ads', 'Google Ads'],
            colors=['#1877f2', '#ea4335'],
            height=350,
            barmode='stack'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("### Evolução do ROI")
    fig3 = criar_grafico_area(
        df=df_filtered,
        x_col='Mês',
        y_col='ROI (%)',
        color='#8b5cf6',
        height=350,
        benchmark_line={
            'value': benchmarks['ROI (%)']['ideal'],
            'color': 'green',
            'text': 'Benchmark Ideal'
        }
    )
    st.plotly_chart(fig3, use_container_width=True)