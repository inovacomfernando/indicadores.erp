"""
Data entry page for monthly metrics
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from auth.supabase_client import get_supabase_client
from auth.auth_manager import get_current_company_id

MONTHS = {
    'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
    'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
    'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
}

MONTH_ABBR = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}

def render_data_entry_page():
    """Render data entry form for monthly metrics"""
    st.title("📝 Cadastro de Métricas Mensais")
    st.markdown("---")

    company_id = get_current_company_id()
    if not company_id:
        st.error("Erro: Empresa não identificada. Faça login novamente.")
        return

    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox("Mês", list(MONTHS.keys()))
    with col2:
        current_year = datetime.now().year
        selected_year = st.selectbox("Ano", list(range(current_year - 1, current_year + 2)))

    month_number = MONTHS[selected_month]
    month_abbr = MONTH_ABBR[month_number]
    month_label = f"{month_abbr}/{str(selected_year)[2:]}"

    st.markdown("---")
    st.subheader("Métricas de Tráfego")

    col1, col2 = st.columns(2)
    with col1:
        sessions = st.number_input("Sessões", min_value=0, value=0, step=1)
    with col2:
        first_visits = st.number_input("Primeira Visita", min_value=0, value=0, step=1)

    st.markdown("---")
    st.subheader("Métricas de Conversão")

    col1, col2, col3 = st.columns(3)
    with col1:
        leads = st.number_input("Leads", min_value=0, value=0, step=1)
    with col2:
        tc_users = st.number_input("TC Usuários (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.01, format="%.2f")
    with col3:
        web_clients = st.number_input("Clientes Web", min_value=0, value=0, step=1)

    tc_leads = st.number_input("TC Leads (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.01, format="%.2f")

    st.markdown("---")
    st.subheader("Métricas Financeiras")

    col1, col2 = st.columns(2)
    with col1:
        web_revenue = st.number_input("Receita Web (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    with col2:
        avg_ticket = st.number_input("Ticket Médio (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")

    st.markdown("---")
    st.subheader("Investimento em Ads")

    col1, col2 = st.columns(2)
    with col1:
        meta_cost = st.number_input("Custo Meta Ads (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    with col2:
        google_cost = st.number_input("Custo Google Ads (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")

    total_ads = meta_cost + google_cost

    st.markdown("---")
    st.subheader("Métricas Calculadas")

    col1, col2, col3 = st.columns(3)
    with col1:
        cac = st.number_input("CAC (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    with col2:
        ltv = st.number_input("LTV (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    with col3:
        cac_ltv_ratio = st.number_input("CAC:LTV Ratio", min_value=0.0, value=0.0, step=0.01, format="%.2f")

    roi = st.number_input("ROI (%)", min_value=0.0, value=0.0, step=0.01, format="%.2f")

    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col2:
        if st.button("💾 Salvar Métricas", type="primary", use_container_width=True):
            save_metrics(
                company_id=company_id,
                month=month_label,
                year=selected_year,
                month_number=month_number,
                sessions=sessions,
                first_visits=first_visits,
                leads=leads,
                tc_users=tc_users,
                web_clients=web_clients,
                tc_leads=tc_leads,
                web_revenue=web_revenue,
                avg_ticket=avg_ticket,
                meta_cost=meta_cost,
                google_cost=google_cost,
                total_ads=total_ads,
                cac=cac,
                ltv=ltv,
                cac_ltv_ratio=cac_ltv_ratio,
                roi=roi
            )

def save_metrics(company_id, month, year, month_number, sessions, first_visits, leads,
                tc_users, web_clients, tc_leads, web_revenue, avg_ticket, meta_cost,
                google_cost, total_ads, cac, ltv, cac_ltv_ratio, roi):
    """Save metrics to database"""
    try:
        supabase = get_supabase_client()

        data = {
            'company_id': company_id,
            'month': month,
            'year': year,
            'month_number': month_number,
            'sessions': sessions,
            'first_visits': first_visits,
            'leads': leads,
            'tc_users': tc_users,
            'web_clients': web_clients,
            'tc_leads': tc_leads,
            'web_revenue': web_revenue,
            'avg_ticket': avg_ticket,
            'meta_cost': meta_cost,
            'google_cost': google_cost,
            'total_ads': total_ads,
            'cac': cac,
            'ltv': ltv,
            'cac_ltv_ratio': cac_ltv_ratio,
            'roi': roi
        }

        existing = supabase.table('monthly_metrics')\
            .select('id')\
            .eq('company_id', company_id)\
            .eq('month', month)\
            .eq('year', year)\
            .maybeSingle()\
            .execute()

        if existing.data:
            response = supabase.table('monthly_metrics')\
                .update(data)\
                .eq('id', existing.data['id'])\
                .execute()
            st.success(f"✅ Métricas de {month}/{year} atualizadas com sucesso!")
        else:
            response = supabase.table('monthly_metrics')\
                .insert(data)\
                .execute()
            st.success(f"✅ Métricas de {month}/{year} cadastradas com sucesso!")

        st.cache_data.clear()

    except Exception as e:
        st.error(f"❌ Erro ao salvar métricas: {str(e)}")
