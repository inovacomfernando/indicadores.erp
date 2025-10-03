"""
Tab 6: Forecast e Análise Preditiva
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.forecast import (
    prever_cenarios,
    avaliar_qualidade_previsao,
    interpretar_tendencia
)
from utils.charts import criar_grafico_projecao


def render_tab_forecast(df):
    """
    Renderiza a tab de forecast
    
    Args:
        df: DataFrame completo (não filtrado)
    """
    st.subheader("🔮 Forecast: Cenários para Projeção e Estratégia")
    
    try:
        # Preparação dos dados
        meses = df['Mês'].tolist()
        previsao_meses = ["Out/25", "Nov/25", "Dez/25"]
        
        # KPIs para previsão
        kpis = ["Leads", "Clientes Web", "Receita Web", "CAC", "LTV", "ROI (%)"]
        
        # Calcular previsões
        resultados = {}
        for kpi in kpis:
            resultados[kpi] = prever_cenarios(df, kpi, num_previsoes=len(previsao_meses))
        
        # Exibir resultados
        st.markdown("### Previsões com Validação Estatística")
        
        for kpi in kpis:
            if resultados[kpi]:
                st.markdown(f"#### {kpi}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Gráfico com previsões
                    fig = criar_grafico_projecao(
                        meses_historico=meses,
                        valores_historico=df[kpi].tolist(),
                        meses_previsao=previsao_meses,
                        valores_previsao=resultados[kpi]['previsao'].tolist(),
                        valores_otimista=resultados[kpi]['otimista'].tolist(),
                        valores_conservador=resultados[kpi]['conservador'].tolist(),
                        title=f"Previsão: {kpi}",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Métricas de qualidade
                    st.markdown("**Métricas de Qualidade**")
                    metricas = resultados[kpi]['metricas']
                    
                    # Avaliação
                    avaliacao = avaliar_qualidade_previsao(
                        metricas['R²'],
                        metricas['MAPE']
                    )
                    
                    st.metric(
                        "R² (Ajuste do Modelo)",
                        f"{metricas['R²']:.3f}",
                        f"{avaliacao['r2']['emoji']} {avaliacao['r2']['status']}"
                    )
                    
                    st.metric(
                        "MAPE (Erro %)",
                        f"{metricas['MAPE']:.1f}%",
                        f"{avaliacao['mape']['emoji']} {avaliacao['mape']['status']}"
                    )
                    
                    # Tendência
                    tend = interpretar_tendencia(
                        metricas['Tendência (tau)'],
                        metricas['P-valor tendência']
                    )
                    
                    st.metric(
                        "Tendência",
                        f"{metricas['Tendência (tau)']:.3f}",
                        f"{tend['emoji']} {tend['direcao']}"
                    )
                
                st.markdown("---")
        
        # Análise de correlação
        st.markdown("### Análise de Correlação entre KPIs")
        corr_matrix = df[kpis].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            labels=dict(color="Correlação"),
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig_corr.update_layout(
            title="Matriz de Correlação",
            height=500
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Insights
        st.markdown("### Insights das Análises")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Qualidade das Previsões:**
            - Modelos com R² > 0.8 são altamente confiáveis
            - MAPE < 10% indica previsões precisas
            - Tendências significativas sugerem padrões consistentes
            
            **Recomendações para Uso:**
            1. Priorize KPIs com maior R² e menor MAPE
            2. Use intervalos de confiança para planejamento
            3. Considere tendências significativas nas decisões
            """)
        
        with col2:
            st.markdown("""
            **Limitações do Modelo:**
            - Assume tendência linear
            - Sensível a mudanças bruscas
            - Requer monitoramento contínuo
            
            **Próximos Passos:**
            1. Atualizar dados mensalmente
            2. Validar previsões vs. realizado
            3. Ajustar modelos conforme necessário
            """)
    
    except Exception as e:
        st.error(f"""
        ❌ Erro ao gerar previsões e análises estatísticas.
        
        Erro: {str(e)}
        
        Verifique:
        1. Formato dos dados
        2. Quantidade de dados históricos
        3. Dependências instaladas
        """)