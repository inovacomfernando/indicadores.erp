"""
Tab 5: Recomendações Estratégicas
"""
import streamlit as st


def render_tab_recomendacoes():
    """
    Renderiza a tab de recomendações
    """
    st.subheader("Recomendações Estratégicas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="alert-box">
            <h4>🎯 Prioridade Alta</h4>
            <ol>
                <li><strong>Monitorar CAC:LTV:</strong> Relação caiu de 4.9:1 para 3.6:1. Atenção máxima para não romper o mínimo de 3:1. Ações:
                    <ul>
                        <li>Reduzir CAC: Otimizar campanhas, pausar keywords caras, investir em canais orgânicos</li>
                        <li>Aumentar LTV: Upsell, cross-sell, retenção e customer success</li>
                    </ul>
                </li>
                <li><strong>Otimizar CAC:</strong> Google Ads subiu +109% em 5 meses. Auditar campanhas e priorizar SEO/conteúdo.</li>
                <li><strong>Melhorar conversão Leads→Vendas:</strong> TC caiu de 5.93% para 3.64%. Implementar lead scoring e revisar funil comercial.</li>
                <li><strong>Qualificar leads:</strong> Foco em qualidade para elevar conversão e ticket médio.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4>📈 Oportunidades</h4>
            <ul>
                <li><strong>Crescimento de leads:</strong> Volume subiu 124% (270→604)</li>
                <li><strong>Tráfego qualificado:</strong> Conversão usuários→leads está dentro do benchmark</li>
                <li><strong>Infraestrutura escalável:</strong> Suporta aumento de 50% sem perda de qualidade</li>
                <li><strong>ROI positivo:</strong> Mantido acima de 260%, modelo sustentável</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)