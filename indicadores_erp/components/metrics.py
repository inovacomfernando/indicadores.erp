"""
Cards de métricas principais
"""
import streamlit as st
import numpy as np

def render_main_metrics(df_filtered):
    """Renderiza as 8 métricas principais"""
    
    # Adiciona um espaço em branco para separar do topo
    st.write("")

    # Verifica se o dataframe não está vazio para evitar erros
    if df_filtered.empty:
        st.warning("Nenhum dado disponível para o período selecionado.")
        return

    # --- Cálculos prévios ---
    cac_medio = df_filtered['CAC'].mean()
    ltv_medio = df_filtered['LTV'].mean()

    st.subheader("Indicadores Gerais de Negócio")
    col1, col2, col3, col4 = st.columns(4)
    
    # --- Linha 1: CAC, LTV, ROI, TC Leads ---
    with col1:
        # Evitar erro se houver apenas um mês selecionado
        if len(df_filtered) > 1:
            cac_variacao = ((df_filtered['CAC'].iloc[-1] - df_filtered['CAC'].iloc[0]) / 
                            df_filtered['CAC'].iloc[0] * 100) if df_filtered['CAC'].iloc[0] != 0 else np.nan
        else:
            cac_variacao = np.nan
            
        st.metric(
            "CAC Médio",
            f"R$ {cac_medio:.2f}",
            f"{cac_variacao:+.1f}%" if not np.isnan(cac_variacao) else " ",
            delta_color="inverse",
            help="Custo de Aquisição por Cliente: Total de investimentos em marketing e vendas dividido pelo número de novos clientes."
        )
    
    with col2:
        if len(df_filtered) > 1:
            ltv_variacao = ((df_filtered['LTV'].iloc[-1] - df_filtered['LTV'].iloc[0]) / 
                            df_filtered['LTV'].iloc[0] * 100) if df_filtered['LTV'].iloc[0] != 0 else np.nan
        else:
            ltv_variacao = np.nan
            
        st.metric(
            "LTV Médio",
            f"R$ {ltv_medio:.2f}",
            f"{ltv_variacao:+.1f}%" if not np.isnan(ltv_variacao) else " ",
            help="Lifetime Value: Receita média que um cliente gera durante todo o seu relacionamento com a empresa."
        )
    
    with col3:
        roi_medio = df_filtered['ROI (%)'].mean()
        if len(df_filtered) > 1:
            roi_variacao = (df_filtered['ROI (%)'].iloc[-1] - df_filtered['ROI (%)'].iloc[0])
        else:
            roi_variacao = np.nan
            
        st.metric(
            "ROI Médio",
            f"{roi_medio:.1f}%",
            f"{roi_variacao:+.1f} p.p." if not np.isnan(roi_variacao) else " ",
            help="Retorno sobre o Investimento: Percentual de lucro ou prejuízo em relação ao que foi investido em anúncios."
        )
    
    with col4:
        tc_leads_medio = df_filtered['TC Leads (%)'].mean()
        if len(df_filtered) > 1:
            tc_variacao = (df_filtered['TC Leads (%)'].iloc[-1] - df_filtered['TC Leads (%)'].iloc[0])
        else:
            tc_variacao = np.nan
        
        st.metric(
            "TC Leads → Vendas",
            f"{tc_leads_medio:.2f}%",
            f"{tc_variacao:+.1f} p.p." if not np.isnan(tc_variacao) else " ",
            delta_color="normal",
            help="Taxa de Conversão de Leads: Percentual de leads que se tornaram clientes."
        )
        
    st.write("---")
    st.subheader("Indicadores de Aquisição e Receita")
    col5, col6, col7, col8 = st.columns(4)

    # --- Linha 2: Receita, Leads, CPL, CAC:LTV ---
    with col5:
        receita_total = df_filtered['Receita Web'].sum()
        if len(df_filtered) > 1:
            receita_variacao = ((df_filtered['Receita Web'].iloc[-1] - df_filtered['Receita Web'].iloc[0]) / 
                                df_filtered['Receita Web'].iloc[0] * 100) if df_filtered['Receita Web'].iloc[0] != 0 else np.nan
        else:
            receita_variacao = np.nan
            
        st.metric(
            "Receita Web (Total)",
            f"R$ {receita_total:,.2f}",
            f"{receita_variacao:+.1f}%" if not np.isnan(receita_variacao) else " ",
            help="Soma da receita gerada através dos canais web no período selecionado."
        )
        
    with col6:
        leads_total = df_filtered['Leads'].sum()
        if len(df_filtered) > 1:
            leads_variacao = ((df_filtered['Leads'].iloc[-1] - df_filtered['Leads'].iloc[0]) / 
                              df_filtered['Leads'].iloc[0] * 100) if df_filtered['Leads'].iloc[0] != 0 else np.nan
        else:
            leads_variacao = np.nan

        st.metric(
            "Leads Gerados (Total)",
            f"{int(leads_total)}",
            f"{leads_variacao:+.1f}%" if not np.isnan(leads_variacao) else " ",
            help="Número total de leads gerados no período selecionado."
        )
        
    with col7:
        # Calcula CPL (Custo por Lead)
        df_cpl = df_filtered.copy()
        # Evitar divisão por zero se não houver leads
        if df_cpl['Leads'].sum() > 0:
            cpl_total = df_cpl['Total Ads'].sum() / df_cpl['Leads'].sum()
        else:
            cpl_total = 0
        
        # Variação do CPL (mês a mês)
        df_cpl['CPL'] = (df_cpl['Total Ads'] / df_cpl['Leads']).replace([np.inf, -np.inf], np.nan)
        if len(df_cpl) > 1 and df_cpl['CPL'].notna().any():
            cpl_variacao = ((df_cpl['CPL'].iloc[-1] - df_cpl['CPL'].iloc[0]) / 
                            df_cpl['CPL'].iloc[0] * 100) if df_cpl['CPL'].iloc[0] != 0 else np.nan
        else:
            cpl_variacao = np.nan

        st.metric(
            "Custo por Lead (CPL)",
            f"R$ {cpl_total:.2f}",
            f"{cpl_variacao:+.1f}%" if not np.isnan(cpl_variacao) else " ",
            delta_color="inverse",
            help="Custo por Lead: Investimento total em anúncios dividido pelo número de leads gerados."
        )
        
    with col8:
        # A métrica é LTV:CAC
        if cac_medio > 0:
            ltv_cac_ratio = ltv_medio / cac_medio
        else:
            ltv_cac_ratio = 0

        # Variação do Ratio (LTV/CAC)
        df_ratio = df_filtered.copy()
        # Evitar divisão por zero
        df_ratio['LTV_CAC'] = (df_ratio['LTV'] / df_ratio['CAC']).replace([np.inf, -np.inf], np.nan)
        
        ratio_variacao = np.nan
        if len(df_ratio) > 1:
            # Pega o primeiro e último valor válido para calcular a variação
            series_ratio = df_ratio['LTV_CAC'].dropna()
            if len(series_ratio) > 1:
                ratio_inicial = series_ratio.iloc[0]
                ratio_final = series_ratio.iloc[-1]
                # A variação é a diferença de pontos, não percentual
                ratio_variacao = ratio_final - ratio_inicial
            
        st.metric(
            "LTV:CAC Ratio",
            f"{ltv_cac_ratio:.1f}:1",
            f"{ratio_variacao:+.1f}" if not np.isnan(ratio_variacao) else " ",
            help=f"Proporção entre LTV (R$ {ltv_medio:.2f}) e CAC (R$ {cac_medio:.2f}). Um valor > 3 é geralmente considerado saudável."
        )