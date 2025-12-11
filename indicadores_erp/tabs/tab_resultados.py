"""
Tab Resultados: Análise Detalhada dos Resultados e Impactos
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def get_monthly_comparison(df):
    """Calcula a variação percentual do último mês em relação ao penúltimo."""
    # Garante que o DataFrame esteja ordenado por 'Mês' para pegar os dois últimos corretamente
    df_copy = df.copy()
    
    # Converte a coluna 'Mês' para um formato de data para ordenação correta
    # Apenas os 3 primeiros caracteres são necessários para o nome do mês.
    df_copy['month_dt'] = pd.to_datetime(df_copy['Mês'].str.slice(0, 3), format='%b', errors='coerce').dt.month
    df_copy = df_copy.sort_values('month_dt').drop(columns='month_dt')

    if len(df_copy) >= 2:
        last_month = df_copy.iloc[-1]
        previous_month = df_copy.iloc[-2]
        
        comparison = {}
        metrics_to_compare = ['Receita Web', 'ROI (%)', 'Clientes Web', 'Leads']
        
        for metric in metrics_to_compare:
            if previous_month[metric] > 0:
                variation = ((last_month[metric] - previous_month[metric]) / previous_month[metric]) * 100
            else:
                variation = float('inf') # Crescimento infinito se o anterior for 0
            comparison[metric] = (variation, last_month[metric], previous_month[metric])
            
        comparison['period'] = f"{previous_month['Mês']} vs {last_month['Mês']}"
        return comparison
    return None

def get_setback_analysis(df):
    """Identifica os meses com os piores indicadores."""
    analysis = {}
    
    # Pior ROI
    worst_roi_month = df.loc[df[df['ROI (%)'] > 0]['ROI (%)'].idxmin()]
    analysis['Pior ROI'] = (worst_roi_month['Mês'], worst_roi_month['ROI (%)'])
    
    # Pior Aquisição de Clientes
    worst_clients_month = df.loc[df[df['Clientes Web'] > 0]['Clientes Web'].idxmin()]
    analysis['Pior Aquisição de Clientes'] = (worst_clients_month['Mês'], worst_clients_month['Clientes Web'])
    
    return analysis

def create_gauge_chart(value, title, reference):
    """Cria um gráfico de medidor (gauge) para comparar valor com referência."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 16}},
        delta={'reference': reference, 'increasing': {'color': "#28a745"}, 'decreasing': {'color': "#dc3545"}},
        gauge={
            'axis': {'range': [None, reference * 2]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, reference * 0.5], 'color': "#dc3545"},
                {'range': [reference * 0.5, reference], 'color': "#ffc107"},
                {'range': [reference, reference * 2], 'color': "#28a745"}
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def render_tab_resultados(df_filtered, benchmarks):
    """Renderiza a tab de resultados detalhados."""
    st.subheader("Painel de Resultados de Negócio")
    st.markdown("Análise consolidada dos indicadores de Marketing, Vendas e Financeiro.")
    
    # Remove meses sem dados (como 'Dez/25') para evitar distorções
    df_analysis = df_filtered[df_filtered['Total Ads'] > 0].copy()
    
    if df_analysis.empty:
        st.warning("Não há dados de performance para o período selecionado.")
        return

    # --- 1. Resumo do Período ---
    st.markdown("#### 📈 Desempenho Geral no Período Selecionado")
    
    total_ads = df_analysis['Total Ads'].sum()
    total_receita = df_analysis['Receita Web'].sum()
    total_leads = df_analysis['Leads'].sum()
    total_clientes = df_analysis['Clientes Web'].sum()
    
    # Médias e Índices (Cálculos Agregados)
    avg_roi = (total_receita - total_ads) / total_ads * 100 if total_ads > 0 else 0
    avg_cac_ltv = df_analysis['CAC:LTV'].mean()
    avg_ltv = df_analysis['LTV'].mean()
    avg_ticket = df_analysis['Ticket Médio'].mean()

    cols1 = st.columns(4)
    cols1[0].metric("Valor Gasto em Ads", f"R$ {total_ads:,.2f}")
    cols1[1].metric("Receita Gerada", f"R$ {total_receita:,.2f}")
    cols1[2].metric("Total de Leads", f"{total_leads:,.0f}")
    cols1[3].metric("Total de Clientes", f"{total_clientes:,.0f}")

    cols2 = st.columns(4)
    cols2[0].metric("ROI Médio (%)", f"{avg_roi:.2f}%")
    cols2[1].metric("Índice CAC:LTV Médio", f"{avg_cac_ltv:.2f}")
    cols2[2].metric("LTV Médio", f"R$ {avg_ltv:,.2f}")
    cols2[3].metric("Ticket Médio", f"R$ {avg_ticket:,.2f}")

    # Indicador de Receita Potencial com base nos Leads
    st.markdown("---")
    st.markdown("#### 🔮 Projeção de Receita Potencial (Baseado em Leads)")
    if total_leads > 0 and avg_ticket > 0:
        receita_potencial_leads = total_leads * avg_ticket
        st.metric(
            label="Receita Potencial (se todos os leads se tornassem clientes)",
            value=f"R$ {receita_potencial_leads:,.2f}",
            help=f"Este valor representa a receita que seria gerada se todos os {total_leads:,.0f} leads tivessem convertido com o ticket médio de R$ {avg_ticket:,.2f}."
        )
    else:
        st.info("Não há dados suficientes (leads ou ticket médio) para calcular a receita potencial.")

    # Indicador de projeção de receita, conforme solicitado
    if total_receita > 0 and avg_cac_ltv > 0:
        st.markdown("---")
        projecao_receita_ltv = total_receita * avg_cac_ltv
        st.metric(
            label="Receita Projetada (Receita Atual × LTV:CAC)",
            value=f"R$ {projecao_receita_ltv:,.2f}",
            help=f"Projeção baseada na receita do período multiplicada pelo índice LTV:CAC. "
                 f"Cálculo: R$ {total_receita:,.2f} (Receita) × {avg_cac_ltv:.2f} (Índice) = R$ {projecao_receita_ltv:,.2f}."
        )

    # --- Simulador de Aumento de Verba em Ads ---
    st.markdown("---")
    st.markdown("#### 🔬 Simulador de Viabilidade de Aumento de Verba em Ads")
    st.info("Use os controles para simular o impacto de um aumento no investimento em anúncios e uma possível melhoria na conversão.")

    # Dados base para o simulador
    cpl_medio = total_ads / total_leads if total_leads > 0 else 0
    taxa_conversao_atual = total_clientes / total_leads if total_leads > 0 else 0

    if cpl_medio > 0 and taxa_conversao_atual > 0:
        sim_cols = st.columns(2)
        with sim_cols[0]:
            aumento_verba_percent = st.slider(
                "Aumento na Verba de Ads (%)",
                min_value=10,
                max_value=200,
                value=50,
                step=10,
                help="Selecione o aumento percentual no investimento em Ads."
            )
        with sim_cols[1]:
            impacto_conversao_percent = st.slider(
                "Melhoria na Taxa de Conversão (%)",
                min_value=0,
                max_value=50,
                value=5,
                step=1,
                help="Estime o impacto do aumento da verba na taxa de conversão de lead para cliente. Isso pode ocorrer por um público mais qualificado ou otimização de campanha."
            )

        # Cálculos do cenário simulado
        aumento_verba_valor = total_ads * (aumento_verba_percent / 100)
        nova_verba_ads = total_ads + aumento_verba_valor
        
        # Assumimos que o Custo por Lead (CPL) se mantém constante para a simulação
        novos_leads_esperados = nova_verba_ads / cpl_medio
        
        # Calcula a nova taxa de conversão com a melhoria estimada
        nova_taxa_conversao = taxa_conversao_atual * (1 + impacto_conversao_percent / 100)
        novos_clientes_esperados = novos_leads_esperados * nova_taxa_conversao
        
        # A nova receita é baseada nos novos clientes e no ticket médio do período
        nova_receita_esperada = novos_clientes_esperados * avg_ticket
        novo_roi = (nova_receita_esperada - nova_verba_ads) / nova_verba_ads * 100 if nova_verba_ads > 0 else 0

        st.markdown("##### **Resultados da Simulação**")
        res_cols = st.columns(4)
        res_cols[0].metric("Nova Verba de Ads", f"R$ {nova_verba_ads:,.2f}", f"+{aumento_verba_percent}%")
        res_cols[1].metric("Novos Leads Esperados", f"{novos_leads_esperados:,.0f}", f"CPL de R$ {cpl_medio:,.2f}")
        res_cols[2].metric("Novos Clientes Esperados", f"{novos_clientes_esperados:,.0f}", f"Conv. de {(nova_taxa_conversao*100):.2f}%")
        res_cols[3].metric("Nova Receita Esperada", f"R$ {nova_receita_esperada:,.2f}", f"ROI de {novo_roi:.2f}%")
        
        with st.expander("Ver detalhes do cálculo da simulação"):
            st.markdown(f"""
            - **Verba de Ads Atual:** R$ {total_ads:,.2f}
            - **Aumento Selecionado:** {aumento_verba_percent}% (R$ {aumento_verba_valor:,.2f})
            - **Nova Verba Total:** R$ {nova_verba_ads:,.2f}
            - **Custo por Lead (CPL) Médio do Período:** R$ {cpl_medio:,.2f} (assumido como constante)
            - **Leads Esperados com a Nova Verba:** `{nova_verba_ads:,.2f} / {cpl_medio:,.2f} = {novos_leads_esperados:,.0f}`
            - **Taxa de Conversão Atual:** `({total_clientes} / {total_leads}) = {(taxa_conversao_atual * 100):.2f}%`
            - **Melhoria na Conversão Selecionada:** {impacto_conversao_percent}%
            - **Nova Taxa de Conversão Projetada:** `{(taxa_conversao_atual * 100):.2f}% * (1 + {impacto_conversao_percent / 100}) = {(nova_taxa_conversao * 100):.2f}%`
            - **Clientes Esperados com a Nova Conversão:** `{novos_leads_esperados:,.0f} * {(nova_taxa_conversao * 100):.2f}% = {novos_clientes_esperados:,.0f}`
            - **Ticket Médio do Período:** R$ {avg_ticket:,.2f} (assumido como constante)
            - **Receita Total Projetada:** `{novos_clientes_esperados:,.0f} * R$ {avg_ticket:,.2f} = R$ {nova_receita_esperada:,.2f}`
            - **ROI Projetado:** `(R$ {nova_receita_esperada:,.2f} - R$ {nova_verba_ads:,.2f}) / R$ {nova_verba_ads:,.2f} = {novo_roi:.2f}%`
            """)
    else:
        st.warning("Dados insuficientes para o simulador (custo por lead ou taxa de conversão zerados no período).")

    # --- 2. Comparativo Mensal ---
    st.markdown("---")
    st.markdown("#### 🆚 Avanço Mensal (Comparativo)")
    
    monthly_comparison = get_monthly_comparison(df_analysis)
    if monthly_comparison:
        st.info(f"Comparando resultados de **{monthly_comparison['period']}**.")
        comp_cols = st.columns(4)
        comp_cols[0].metric("Variação Receita", f"{monthly_comparison['Receita Web'][1]:,.2f}", f"{monthly_comparison['Receita Web'][0]:.2f}%")
        comp_cols[1].metric("Variação ROI", f"{monthly_comparison['ROI (%)'][1]:.2f}%", f"{monthly_comparison['ROI (%)'][0]:.2f}%")
        comp_cols[2].metric("Variação Clientes", f"{monthly_comparison['Clientes Web'][1]}", f"{monthly_comparison['Clientes Web'][0]:.2f}%")
        comp_cols[3].metric("Variação Leads", f"{monthly_comparison['Leads'][1]}", f"{monthly_comparison['Leads'][0]:.2f}%")
    else:
        st.warning("Selecione pelo menos dois meses para ver o avanço mensal.")

    # --- 3. Comparativo vs. Mercado SaaS ERP ---
    st.markdown("---")
    st.markdown("#### 🌍 Comparativo de Mercado (vs. Ideal SaaS ERP)")
    st.info("Benchmarks ideais são valores de referência. Valores podem variar conforme o estágio da empresa.")

    # Benchmarks (praticado vs. ideal)
    # Estes valores 'ideais' são placeholders e devem ser ajustados conforme a realidade do mercado.
    ideal_benchmarks = {
        'CAC:LTV': 3.0,
        'ROI (%)': 300.0,
        'Taxa de Conversão (%)': 5.0 
    }
    
    tc_praticada = (total_clientes / total_leads) * 100 if total_leads > 0 else 0
    
    bench_cols = st.columns(3)
    with bench_cols[0]:
        st.plotly_chart(create_gauge_chart(avg_cac_ltv, "CAC:LTV (Praticado vs Ideal)", ideal_benchmarks['CAC:LTV']), use_container_width=True)
    with bench_cols[1]:
        st.plotly_chart(create_gauge_chart(avg_roi, "ROI (%) (Praticado vs Ideal)", ideal_benchmarks['ROI (%)']), use_container_width=True)
    with bench_cols[2]:
        st.plotly_chart(create_gauge_chart(tc_praticada, "Taxa Conversão (Leads > Clientes)", ideal_benchmarks['Taxa de Conversão (%)']), use_container_width=True)

    # --- 4. Análise de Recuo e Períodos Críticos ---
    st.markdown("---")
    st.markdown("#### 📉 Análise de Recuo e Pontos de Atenção")
    
    setbacks = get_setback_analysis(df_analysis)
    
    recuo_cols = st.columns(2)
    with recuo_cols[0]:
        st.error("Mês com o **pior ROI** (excluindo valores negativos/nulos)")
        st.metric(label=f"Mês: {setbacks['Pior ROI'][0]}", value=f"{setbacks['Pior ROI'][1]:.2f}%")
    with recuo_cols[1]:
        st.error("Mês com a **pior aquisição de clientes**")
        st.metric(label=f"Mês: {setbacks['Pior Aquisição de Clientes'][0]}", value=f"{setbacks['Pior Aquisição de Clientes'][1]} clientes")

    with st.expander("Considerações sobre a Análise de Tendência"):
        st.warning("""
        **Períodos a serem desconsiderados para análise estatística de tendência:**
        - **Dez/25:** Este mês contém dados zerados e foi automaticamente removido dos cálculos de média e comparações.
        - **Out/25 e Nov/25:** Apresentam quedas abruptas em ROI e CAC. É crucial investigar os eventos ocorridos nestes meses (ex: problemas na campanha, sazonalidade, mudança de estratégia) antes de incluí-los em projeções de longo prazo.
        """, icon="⚠️")
