"""
Componentes de header e sidebar
"""
import streamlit as st
from datetime import datetime



def render_header():
    """Renderiza o header principal"""
    st.markdown(
        '<div class="main-header">📊 Dashboard de Marketing - SaaS ERP</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">Análise de Performance: Maio - Dezembro 2025</div>',
        unsafe_allow_html=True
    )


def render_sidebar(df):
    """Renderiza a sidebar com filtros e controles"""
    with st.sidebar:

        st.image("assets/vendasimples.png", use_container_width=True)

        st.markdown("---")

        # Filtros
        st.subheader("📊 Filtros")
        selected_months = st.multiselect(
            "Selecione os meses:",
            options=df['Mês'].tolist(),
            default=df['Mês'].tolist()
        )

        # Controle de Dados
        st.markdown("---")
        st.subheader("🔄 Controle de Dados")

        # Timestamp do cache
        if hasattr(df, 'attrs') and 'carregado_em' in df.attrs:
            st.caption("📅 Dados carregados em:")
            st.code(df.attrs['carregado_em'], language=None)
        else:
            st.caption("📅 Cache ativo (sem timestamp)")

        # Botões
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🔄 Recarregar",
                use_container_width=True,
                help="Limpa o cache e recarrega os dados"
            ):
                st.cache_data.clear()
                st.success("✅ Cache limpo!")
                st.rerun()

        with col2:
            if st.button(
                "🔃 Atualizar",
                use_container_width=True,
                help="Atualiza a visualização sem limpar cache"
            ):
                st.rerun()

        # Instruções
        with st.expander("ℹ️ Como atualizar dados"):
            st.markdown("""
            **Após alterar dados no loader.py:**

            1. 📝 Edite `data/loader.py`
            2. 💾 Salve as alterações
            3. 🔄 Clique em "Recarregar"
            4. ✅ Dados atualizados!

            **Atalhos:**
            - Pressione `C` → "Clear cache"

            **Cache:**
            - ⏰ TTL: 5 minutos
            - 🔄 Auto-renovação ativa
            """)

        # Informações de apuração
        try:
            from config.config_apuracao import get_info_apuracao

            st.markdown("---")
            st.subheader("📅 Status de Apuração")

            info = get_info_apuracao()

            st.metric(
                "Último mês apurado",
                info['ultimo_mes'],
                help="Último mês com dados oficialmente apurados"
            )

            with st.expander("📋 Ver detalhes"):
                st.markdown(f"""
                **Informações:**
                - 🟢 Meses apurados: {info['total_meses']}
                - ⏳ Próximo: {info['proximo_mes']}
                - 📅 Data estimada: {info['data_estimada']}

                **Meses apurados:**
                """)

                for mes in info['meses']:
                    st.markdown(f"- ✓ {mes}")

                st.info("""
                💡 **Regra:** Dados são apurados no
                primeiro dia útil do mês seguinte.
                """)
        except ImportError:
            pass

        # Sobre
        st.markdown("---")
        st.subheader("ℹ️ Sobre")
        st.info("""
        Dashboard interativo para análise de KPIs de marketing digital 
        com benchmarks do setor de SaaS ERP.

        **Recursos:**
        - 📊 Análise de performance
        - 🔮 Forecast inteligente
        - ⚠️ Alertas automáticos
        - 📈 Benchmarks do setor
        """)

        # Estatísticas rápidas
        if len(selected_months) > 0:
            st.markdown("---")
            st.subheader("📈 Resumo Rápido")

            df_filtered = df[df['Mês'].isin(selected_months)]
            df_valid = df_filtered[df_filtered['Sessões'] > 0]

            if len(df_valid) > 0:
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Meses",
                        len(df_valid),
                        help="Meses com dados no período filtrado"
                    )

                with col2:
                    total_leads = df_valid['Leads'].sum()
                    st.metric("Total de Leads", total_leads)

