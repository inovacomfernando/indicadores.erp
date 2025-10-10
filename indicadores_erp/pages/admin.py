"""
Admin panel for data management
"""
import streamlit as st
import pandas as pd
from auth.supabase_client import get_supabase_client
from auth.auth_manager import get_current_company_id

def render_admin_page():
    """Render admin panel for managing data"""
    st.title("⚙️ Painel Administrativo")
    st.markdown("---")

    company_id = get_current_company_id()
    if not company_id:
        st.error("Erro: Empresa não identificada. Faça login novamente.")
        return

    tab1, tab2 = st.tabs(["📊 Métricas Cadastradas", "🗑️ Gerenciar Dados"])

    with tab1:
        render_metrics_list(company_id)

    with tab2:
        render_data_management(company_id)

def render_metrics_list(company_id):
    """Display list of all metrics for the company"""
    st.subheader("Métricas Cadastradas")

    try:
        supabase = get_supabase_client()

        response = supabase.table('monthly_metrics')\
            .select('*')\
            .eq('company_id', company_id)\
            .order('year', desc=True)\
            .order('month_number', desc=True)\
            .execute()

        if not response.data:
            st.info("Nenhuma métrica cadastrada ainda. Use o menu 'Cadastrar Métricas' para adicionar dados.")
            return

        df = pd.DataFrame(response.data)

        display_df = pd.DataFrame({
            'Mês': df['month'],
            'Ano': df['year'],
            'Sessões': df['sessions'],
            'Leads': df['leads'],
            'Clientes': df['web_clients'],
            'Receita': df['web_revenue'].apply(lambda x: f"R$ {x:,.2f}"),
            'CAC': df['cac'].apply(lambda x: f"R$ {x:,.2f}"),
            'ROI': df['roi'].apply(lambda x: f"{x:.2f}%")
        })

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown(f"**Total de registros:** {len(df)}")

    except Exception as e:
        st.error(f"Erro ao carregar métricas: {str(e)}")

def render_data_management(company_id):
    """Render data management section"""
    st.subheader("Gerenciar Dados")

    st.markdown("### 🗑️ Excluir Métricas")

    try:
        supabase = get_supabase_client()

        response = supabase.table('monthly_metrics')\
            .select('id, month, year')\
            .eq('company_id', company_id)\
            .order('year', desc=True)\
            .order('month_number', desc=True)\
            .execute()

        if not response.data:
            st.info("Nenhuma métrica cadastrada.")
            return

        metrics = response.data
        options = [f"{m['month']}/{m['year']}" for m in metrics]
        metric_ids = {f"{m['month']}/{m['year']}": m['id'] for m in metrics}

        selected_metric = st.selectbox(
            "Selecione a métrica para excluir",
            options,
            key="delete_metric_select"
        )

        col1, col2 = st.columns([3, 1])

        with col2:
            if st.button("🗑️ Excluir", type="secondary", use_container_width=True):
                metric_id = metric_ids[selected_metric]

                confirm = st.warning(f"⚠️ Tem certeza que deseja excluir as métricas de {selected_metric}?")

                col_yes, col_no = st.columns(2)

                with col_yes:
                    if st.button("✅ Sim, excluir", key="confirm_delete"):
                        delete_metric(metric_id, selected_metric)

                with col_no:
                    if st.button("❌ Cancelar", key="cancel_delete"):
                        st.info("Operação cancelada.")

    except Exception as e:
        st.error(f"Erro ao carregar métricas: {str(e)}")

    st.markdown("---")
    st.markdown("### 🔄 Limpar Cache")
    st.markdown("Use esta opção se os dados não estiverem atualizando corretamente.")

    if st.button("🔄 Limpar Cache", type="secondary"):
        st.cache_data.clear()
        st.success("✅ Cache limpo com sucesso!")
        st.rerun()

def delete_metric(metric_id, metric_label):
    """Delete a metric record"""
    try:
        supabase = get_supabase_client()

        response = supabase.table('monthly_metrics')\
            .delete()\
            .eq('id', metric_id)\
            .execute()

        st.success(f"✅ Métricas de {metric_label} excluídas com sucesso!")
        st.cache_data.clear()
        st.rerun()

    except Exception as e:
        st.error(f"❌ Erro ao excluir métricas: {str(e)}")
