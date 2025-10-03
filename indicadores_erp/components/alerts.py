"""
Componentes de alertas e notificações
"""
import streamlit as st

def render_main_alerts():
    """Renderiza os alertas principais"""
    st.markdown("""
    <div class="alert-box">
        <h4>⚠️ Pontos de Atenção</h4>
        <ul>
            <li><strong>CAC crescente:</strong> Aumentou 36% de Mai para Set (R$ 323 → R$ 441)</li>
            <li><strong>ROI em queda:</strong> Redução de 31% no período (390% → 271%)</li>
            <li><strong>Relação CAC:LTV em declínio:</strong> Caiu de 4.9:1 para 3.7:1</li>
            <li><strong>TC Leads baixa:</strong> Tendência de queda (5.93% → 3.77%)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)