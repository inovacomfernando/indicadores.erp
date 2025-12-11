"""
Tab Resultados: Análise Detalhada dos Resultados e Impactos
"""
import streamlit as st
import numpy as np

def render_tab_resultados(df_filtered, benchmarks):
    """
    Renderiza a tab de resultados detalhados, consolidando as informações
    das outras abas.
    
    Args:
        df_filtered: DataFrame com os dados filtrados.
        benchmarks: Dicionário com os benchmarks do negócio.
    """
    st.subheader("Resultados Consolidados e Análise de Impacto")
    
    st.markdown("""
    Esta seção apresenta uma análise aprofundada dos resultados obtidos, 
    conectando os dados da operação com os impactos tangíveis no negócio, vendas e marketing,
    com base no período selecionado.
    """)
    
    # --- Cálculos Chave ---
    # Evitar divisão por zero e tratar dados vazios
    if df_filtered.empty:
        st.warning("Não há dados para o período selecionado.")
        return

    # Último mês dos dados filtrados para métricas pontuais
    ultimo_mes = df_filtered.iloc[-1]
    
    # Totais e Médias do período
    total_receita = df_filtered['Receita Web'].sum()
    total_clientes = df_filtered['Clientes Web'].sum()
    total_leads = df_filtered['Leads'].sum()
    total_sessoes = df_filtered['Sessões'].sum()
    total_investido_ads = df_filtered['Total Ads'].sum()
    
    # Médias ponderadas e taxas
    ticket_medio_periodo = total_receita / total_clientes if total_clientes > 0 else 0
    media_cac = df_filtered['CAC'].mean()
    media_ltv = df_filtered['LTV'].mean()
    
    # Taxas de conversão do período
    taxa_conversao_usuarios_leads = (total_leads / total_sessoes * 100) if total_sessoes > 0 else 0
    taxa_conversao_leads_clientes = (total_clientes / total_leads * 100) if total_leads > 0 else 0

    # --- Seção 1: Detalhamento dos Resultados da Operação ---
    st.markdown("---")
    st.markdown("### 1. Desempenho Geral da Operação")
    st.info("Resumo dos principais indicadores acumulados no período selecionado.", icon="📊")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Total", f"R$ {total_receita:,.2f}")
    col2.metric("Total de Clientes", f"{total_clientes:,.0f}")
    col3.metric("Total de Leads", f"{total_leads:,.0f}")
    col4.metric("Ticket Médio no Período", f"R$ {ticket_medio_periodo:,.2f}")

    # --- Seção 2: Impacto Estratégico no Negócio ---
    st.markdown("---")
    st.markdown("### 2. Análise Estratégica e Financeira")
    st.info("Indicadores chave que medem a saúde e a sustentabilidade do negócio.", icon="🎯")

    col1, col2, col3 = st.columns(3)
    col1.metric("CAC Médio (Custo por Cliente)", f"R$ {media_cac:,.2f}", 
                help="Custo médio para adquirir um cliente no período.")
    col2.metric("LTV Médio (Valor do Tempo de Vida)", f"R$ {media_ltv:,.2f}",
                help="Receita média esperada de um cliente ao longo do tempo.")
    
    # Relação LTV/CAC
    relacao_ltv_cac = media_ltv / media_cac if media_cac > 0 else 0
    delta_ltv_cac = relacao_ltv_cac - benchmarks['CAC:LTV']['ideal']
    col3.metric("Relação LTV/CAC", f"{relacao_ltv_cac:.1f}x", f"{delta_ltv_cac:.1f}x vs ideal",
                help=f"Ideal: Acima de {benchmarks['CAC:LTV']['ideal']}x. Mostra o retorno sobre o custo de aquisição.")

    # --- Seção 3: Impacto em Vendas e Marketing ---
    st.markdown("---")
    st.markdown("### 3. Funil de Aquisição e Eficiência")
    st.info("Análise da performance do funil de conversão e investimentos em marketing.", icon="📈")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Funil de Marketing (Visitantes para Leads)")
        delta_tc_usuarios = taxa_conversao_usuarios_leads - benchmarks['TC Usuários (%)']['ideal']
        st.metric(
            label="Taxa de Conv. Visitante → Lead",
            value=f"{taxa_conversao_usuarios_leads:.2f}%",
            delta=f"{delta_tc_usuarios:.2f}% vs ideal",
            help="Percentual de sessões que se tornaram Leads."
        )

    with col2:
        st.markdown("#### Funil de Vendas (Leads para Clientes)")
        delta_tc_leads = taxa_conversao_leads_clientes - benchmarks['TC Leads (%)']['ideal']
        st.metric(
            label="Taxa de Conv. Lead → Cliente",
            value=f"{taxa_conversao_leads_clientes:.2f}%",
            delta=f"{delta_tc_leads:.2f}% vs ideal",
            help="Percentual de Leads que se tornaram Clientes."
        )

    st.markdown("#### Análise de Investimento")
    col1, col2, col3 = st.columns(3)
    roi_periodo = ((total_receita - total_investido_ads) / total_investido_ads * 100) if total_investido_ads > 0 else 0
    
    col1.metric("Total Investido em Ads", f"R$ {total_investido_ads:,.2f}")
    col2.metric("ROI de Marketing (Período)", f"{roi_periodo:.1f}%", 
                help="Retorno sobre o Investimento em anúncios. ((Receita - Custo) / Custo).")
    col3.metric("Custo por Lead (CPL)", f"R$ {total_investido_ads/total_leads if total_leads > 0 else 0:,.2f}",
                help="Custo médio para gerar um lead através de anúncios.")
    
    st.markdown("---")
    st.caption(f"Análise baseada nos dados do período selecionado. Benchmarks de referência: TC Visitante→Lead > {benchmarks['TC Usuários (%)']['ideal']}%; TC Lead→Cliente > {benchmarks['TC Leads (%)']['ideal']}%; LTV/CAC > {benchmarks['CAC:LTV']['ideal']}x.")