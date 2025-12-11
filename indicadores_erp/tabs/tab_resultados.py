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
