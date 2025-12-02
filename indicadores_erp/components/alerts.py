"""
Componentes de alertas e notificações com análise dinâmica
"""
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

def analyze_trend(series):
    """
    Analisa a tendência de uma série temporal
    Retorna: (tendencia, percentual_variacao, valor_inicial, valor_final)
    """
    # Remove zeros e valores nulos
    clean_series = series[series > 0].dropna()
    
    if len(clean_series) < 2:
        return None, 0, 0, 0
    
    valor_inicial = clean_series.iloc[0]
    valor_final = clean_series.iloc[-1]
    
    # Calcula variação percentual
    if valor_inicial > 0:
        percentual = ((valor_final - valor_inicial) / valor_inicial) * 100
    else:
        percentual = 0
    
    # Determina tendência
    if percentual > 5:
        tendencia = "crescente"
    elif percentual < -5:
        tendencia = "queda"
    else:
        tendencia = "estável"
    
    return tendencia, percentual, valor_inicial, valor_final

def calculate_metrics_health(df):
    """
    Calcula a saúde geral das métricas e identifica pontos de atenção
    """
    # Filtra apenas meses com dados (remove zeros)
    df_valid = df[df['Sessões'] > 0].copy()
    
    if len(df_valid) < 2:
        return []
    
    alerts = []
    
    # 1. Análise de CAC
    cac_trend, cac_var, cac_inicial, cac_final = analyze_trend(df_valid['CAC'])
    if cac_trend == "crescente" and abs(cac_var) > 10:
        alerts.append({
            'icon': '📈',
            'title': 'CAC crescente',
            'message': f'Aumentou {abs(cac_var):.1f}% no período (R$ {cac_inicial:.0f} → R$ {cac_final:.0f})',
            'severity': 'high'
        })
    
    # 2. Análise de ROI
    roi_trend, roi_var, roi_inicial, roi_final = analyze_trend(df_valid['ROI (%)'])
    if roi_trend == "queda" and abs(roi_var) > 15:
        alerts.append({
            'icon': '📉',
            'title': 'ROI em queda',
            'message': f'Redução de {abs(roi_var):.1f}% no período ({roi_inicial:.0f}% → {roi_final:.0f}%)',
            'severity': 'high'
        })
    
    # 3. Análise de CAC:LTV
    cac_ltv_trend, cac_ltv_var, cac_ltv_inicial, cac_ltv_final = analyze_trend(df_valid['CAC:LTV'])
    if cac_ltv_trend == "queda" and abs(cac_ltv_var) > 10:
        alerts.append({
            'icon': '⚠️',
            'title': 'Relação CAC:LTV em declínio',
            'message': f'Caiu de {cac_ltv_inicial:.1f}:1 para {cac_ltv_final:.1f}:1',
            'severity': 'medium'
        })
    elif cac_ltv_final < 3:
        alerts.append({
            'icon': '🚨',
            'title': 'CAC:LTV abaixo do ideal',
            'message': f'Relação atual: {cac_ltv_final:.1f}:1 (ideal: >3:1)',
            'severity': 'high'
        })
    
    # 4. Análise de Taxa de Conversão de Leads
    tc_leads_trend, tc_leads_var, tc_leads_inicial, tc_leads_final = analyze_trend(df_valid['TC Leads (%)'])
    if tc_leads_trend == "queda" and abs(tc_leads_var) > 15:
        alerts.append({
            'icon': '📊',
            'title': 'TC Leads em queda',
            'message': f'Tendência de queda ({tc_leads_inicial:.2f}% → {tc_leads_final:.2f}%)',
            'severity': 'medium'
        })
    elif tc_leads_final < 3:
        alerts.append({
            'icon': '⚡',
            'title': 'TC Leads baixa',
            'message': f'Taxa atual: {tc_leads_final:.2f}% (atenção ao funil de conversão)',
            'severity': 'medium'
        })
    
    # 5. Análise de Taxa de Conversão de Usuários
    tc_users_trend, tc_users_var, tc_users_inicial, tc_users_final = analyze_trend(df_valid['TC Usuários (%)'])
    if tc_users_trend == "queda" and abs(tc_users_var) > 15:
        alerts.append({
            'icon': '👥',
            'title': 'TC Usuários em declínio',
            'message': f'Redução de {abs(tc_users_var):.1f}% ({tc_users_inicial:.2f}% → {tc_users_final:.2f}%)',
            'severity': 'medium'
        })
    
    # 6. Análise de Custo Total
    custo_trend, custo_var, custo_inicial, custo_final = analyze_trend(df_valid['Total Ads'])
    if custo_trend == "crescente" and abs(custo_var) > 30:
        alerts.append({
            'icon': '💰',
            'title': 'Custo de Ads crescendo rapidamente',
            'message': f'Aumento de {abs(custo_var):.1f}% (R$ {custo_inicial:.0f} → R$ {custo_final:.0f})',
            'severity': 'medium'
        })
    
    # 7. Análise de Receita vs Custo
    if len(df_valid) > 0:
        df_valid['Margem'] = ((df_valid['Receita Web'] - df_valid['Total Ads']) / df_valid['Receita Web'] * 100)
        margem_media = df_valid['Margem'].mean()
        
        if margem_media < 20:
            alerts.append({
                'icon': '💸',
                'title': 'Margem de lucro apertada',
                'message': f'Margem média: {margem_media:.1f}% (custo ads vs receita)',
                'severity': 'high'
            })
    
    # 8. Análise de Ticket Médio
    ticket_trend, ticket_var, ticket_inicial, ticket_final = analyze_trend(df_valid['Ticket Médio'])
    if ticket_trend == "queda" and abs(ticket_var) > 10:
        alerts.append({
            'icon': '🎫',
            'title': 'Ticket Médio em queda',
            'message': f'Redução de {abs(ticket_var):.1f}% (R$ {ticket_inicial:.2f} → R$ {ticket_final:.2f})',
            'severity': 'low'
        })
    
    return alerts

def render_main_alerts(df):
    """
    Renderiza os alertas principais com um visual moderno e baseado nos dados reais.
    Args:
        df: DataFrame com os dados do loader.
    """
    alerts = calculate_metrics_health(df)
    
    # --- Template Base para os Alertas ---
    alert_template = """
    <div class="alert-box" style="background-color: #262730; border-left: 6px solid {border_color}; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h4 style="color: {border_color}; margin-top: 0; font-weight: 600;">{icon} {title}</h4>
        {content}
        <p style="color: #95a5a6; font-size: 0.85em; margin-bottom: 0; margin-top: 15px;">
            <em>📅 Os resultados são atualizados automaticamente e apurados no primeiro dia útil do próximo mês.</em>
        </p>
    </div>
    """

    if not alerts:
        content = '<p style="color: #bdc3c7; margin-bottom: 10px;">Nenhum ponto crítico de atenção identificado no momento.</p>'
        st.markdown(alert_template.format(
            border_color="#2ecc71",
            icon="✅",
            title="Métricas Saudáveis",
            content=content
        ), unsafe_allow_html=True)
        return
    
    # Separa alertas por severidade
    high_alerts = [a for a in alerts if a['severity'] == 'high']
    medium_alerts = [a for a in alerts if a['severity'] == 'medium']
    low_alerts = [a for a in alerts if a['severity'] == 'low']
    
    # Renderiza alertas de alta severidade
    if high_alerts:
        alerts_html = "<ul style='color: #bdc3c7; margin-bottom: 10px; padding-left: 20px;'>"
        for alert in high_alerts:
            alerts_html += f"<li><strong>{alert['icon']} {alert['title']}:</strong> {alert['message']}</li>"
        alerts_html += "</ul>"
        
        st.markdown(alert_template.format(
            border_color="#e74c3c",
            icon="🚨",
            title="Pontos Críticos de Atenção",
            content=alerts_html
        ), unsafe_allow_html=True)

    # Renderiza alertas de média severidade
    if medium_alerts:
        alerts_html = "<ul style='color: #bdc3c7; margin-bottom: 10px; padding-left: 20px;'>"
        for alert in medium_alerts:
            alerts_html += f"<li><strong>{alert['icon']} {alert['title']}:</strong> {alert['message']}</li>"
        alerts_html += "</ul>"
        
        st.markdown(alert_template.format(
            border_color="#f39c12",
            icon="⚠️",
            title="Pontos de Monitoramento",
            content=alerts_html
        ), unsafe_allow_html=True)

    # Renderiza alertas de baixa severidade
    if low_alerts:
        alerts_html = "<ul style='color: #bdc3c7; margin-bottom: 10px; padding-left: 20px;'>"
        for alert in low_alerts:
            alerts_html += f"<li><strong>{alert['icon']} {alert['title']}:</strong> {alert['message']}</li>"
        alerts_html += "</ul>"

        st.markdown(alert_template.format(
            border_color="#3498db",
            icon="ℹ️",
            title="Observações",
            content=alerts_html
        ), unsafe_allow_html=True)

def render_insights(df):
    """
    Renderiza insights adicionais e recomendações
    """
    df_valid = df[df['Sessões'] > 0].copy()
    
    if len(df_valid) < 2:
        return
    
    insights = []
    
    # Insight sobre melhor performance
    best_roi_idx = df_valid['ROI (%)'].idxmax()
    best_month = df_valid.loc[best_roi_idx, 'Mês']
    best_roi = df_valid.loc[best_roi_idx, 'ROI (%)']
    
    insights.append(f"**Melhor ROI:** {best_month} com {best_roi:.1f}%")
    
    # Insight sobre eficiência de conversão
    best_tc_idx = df_valid['TC Leads (%)'].idxmax()
    best_tc_month = df_valid.loc[best_tc_idx, 'Mês']
    best_tc = df_valid.loc[best_tc_idx, 'TC Leads (%)']
    
    insights.append(f"**Melhor TC Leads:** {best_tc_month} com {best_tc:.2f}%")
    
    # Insight sobre crescimento de receita
    receita_trend, receita_var, _, _ = analyze_trend(df_valid['Receita Web'])
    if receita_trend == "crescente":
        insights.append(f"**Receita Web:** Crescimento de {abs(receita_var):.1f}% no período ✅")
    
    if insights:
        st.markdown("### 💡 Insights Positivos")
        for insight in insights:
            st.markdown(f"- {insight}")
