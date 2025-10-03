"""
Cards de métricas principais
"""
import streamlit as st

def render_main_metrics(df_filtered):
    """Renderiza as 4 métricas principais"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cac_medio = df_filtered['CAC'].mean()
        cac_variacao = ((df_filtered['CAC'].iloc[-1] - df_filtered['CAC'].iloc[0]) / 
                        df_filtered['CAC'].iloc[0] * 100)
        st.metric(
            "CAC Médio",
            f"R$ {cac_medio:.2f}",
            f"{cac_variacao:+.1f}%",
            delta_color="inverse"
        )
    
    with col2:
        ltv_medio = df_filtered['LTV'].mean()
        ltv_variacao = ((df_filtered['LTV'].iloc[-1] - df_filtered['LTV'].iloc[0]) / 
                        df_filtered['LTV'].iloc[0] * 100)
        st.metric(
            "LTV Médio",
            f"R$ {ltv_medio:.2f}",
            f"{ltv_variacao:+.1f}%"
        )
    
    with col3:
        roi_medio = df_filtered['ROI (%)'].mean()
        roi_variacao = ((df_filtered['ROI (%)'].iloc[-1] - df_filtered['ROI (%)'].iloc[0]) / 
                        df_filtered['ROI (%)'].iloc[0] * 100)
        st.metric(
            "ROI Médio",
            f"{roi_medio:.1f}%",
            f"{roi_variacao:+.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        tc_leads_medio = df_filtered['TC Leads (%)'].mean()
        tc_variacao = ((df_filtered['TC Leads (%)'].iloc[-1] - df_filtered['TC Leads (%)'].iloc[0]) / 
                       df_filtered['TC Leads (%)'].iloc[0] * 100)
        st.metric(
            "TC Leads → Vendas",
            f"{tc_leads_medio:.2f}%",
            f"{tc_variacao:+.1f}%",
            delta_color="inverse"
        )