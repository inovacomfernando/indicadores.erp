"""
Componentes de header e sidebar
"""
import streamlit as st
from datetime import datetime


def render_header():
    """Renderiza o header principal"""
    st.markdown('<div class="main-header">📊 Dashboard de Marketing - SaaS ERP</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Análise de Performance: Maio - Dezembro 2025</div>', 
                unsafe_allow_html=True)


def render_sidebar(df):
    """Renderiza a sidebar com filtros e controles"""
    with st.sidebar:
    try:
        st.markdown(
            f'<a href="https://vendasimples.com.br"><img src="assets/vs.png" style="width: 100%;"></a>',
            unsafe_allow_html=True
        )
    except:
        st.markdown("### 📊 Dashboard Marketing")
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
        
        # Mostra quando os dados foram carregados
        if hasattr(df, 'attrs') and 'carregado_em' in df.attrs:
            st.caption(f"📅 Dados carregados em:")
            st.code(df.attrs['carregado_em'], language=None)
        else:
            st.caption("📅 Cache ativo (sem timestamp)")
        
        # Botão para forçar recarga
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Recarregar", use_container_width=True, 
                        help="Limpa o cache e recarrega os dados"):
                st.cache_data.clear()
                st.success("✅ Cache limpo!")
                st.rerun()
        
        with col2:
            if st.button("🔃 Atualizar", use_container_width=True,
                        help="Atualiza a visualização sem limpar cache"):
                st.rerun()
        
        # Instruções em expander
        with st.expander("ℹ️ Como atualizar dados"):
            st.markdown("""
            **Após alterar dados no loader.py:**
            
            1. 📝 Edite `data/loader.py`
            2. 💾 Salve as alterações (Ctrl+S)
            3. 🔄 Clique em "Recarregar" acima
            4. ✅ Dados atualizados!
            
            **Ou use atalhos:**
            - Pressione `C` → "Clear cache"
            - Aguarde 5 min (auto-atualização)
            
            **Status do cache:**
            - ⏰ TTL: 5 minutos
            - 🔄 Auto-renovação ativada
            """)
        
        # Informações de apuração (se disponível)
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
                - ✅ Meses apurados: {info['total_meses']}
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
            pass  # Arquivo de configuração não existe
        
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
        
        # Estatísticas rápidas (se tiver dados filtrados)
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
                        help="Meses com dados no período selecionado"
                    )
                
                with col2:
                    total_leads = df_valid['Leads'].sum()
                    st.metric(
                        "Leads",
                        f"{total_leads:.0f}",
                        help="Total de leads no período"
                    )
                
                # Indicador de saúde geral
                roi_medio = df_valid['ROI (%)'].mean()
                if roi_medio > 300:
                    status = "🟢 Excelente"
                    cor = "#00d4aa"
                elif roi_medio > 200:
                    status = "🟡 Bom"
                    cor = "#ffa502"
                else:
                    status = "🔴 Atenção"
                    cor = "#ff4757"
                
                st.markdown(f"""
                <div style="
                    background: {cor}20; 
                    border-left: 3px solid {cor}; 
                    padding: 10px; 
                    border-radius: 5px;
                    margin-top: 10px;
                ">
                    <strong>{status}</strong><br>
                    <small>ROI médio: {roi_medio:.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("---")
        st.caption("🔧 Desenvolvido para análise estratégica de marketing")
        st.caption(f"⏰ Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        return selected_months

