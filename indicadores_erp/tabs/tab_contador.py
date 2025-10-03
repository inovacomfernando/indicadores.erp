"""
Tab 7: Parceria Contador
"""
import streamlit as st
import pandas as pd
from config.settings import PLANOS, EXTENSOES, CUSTOS_LEAD
from utils.calculations import calcular_comissao, calcular_cac_ltv_ratio
from utils.charts import (
    criar_grafico_comparativo,
    criar_grafico_barras,
    criar_grafico_subplots
)
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def render_tab_contador(df_filtered):
    """
    Renderiza a tab de parceria com contador
    
    Args:
        df_filtered: DataFrame filtrado
    """
    st.subheader("🤝 Parceria Contador: Simulação de Indicadores")
    
    # ========== CONFIGURAÇÃO DO MODELO ==========
    st.markdown("### ⚙️ Configuração do Modelo de Parceria")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        percentual_comissao = st.slider(
            "Percentual de Comissão (%)",
            min_value=5.0,
            max_value=25.0,
            value=15.0,
            step=0.5,
            help="Ajuste o percentual de comissão mensal sobre o valor do plano + extensões"
        ) / 100
        
        st.info(f"💡 Comissão selecionada: **{percentual_comissao*100:.1f}%**")
    
    with col_config2:
        meses_comissao = st.slider(
            "Período de Comissão (meses)",
            min_value=3,
            max_value=12,
            value=6,
            step=1,
            help="Por quantos meses o contador receberá comissão"
        )
        
        st.info(f"📅 Período: **{meses_comissao} meses**")
    
    st.markdown("---")
    
    # ========== SELEÇÃO DE PLANO E EXTENSÕES ==========
    st.markdown("### 📦 Configuração do Plano do Cliente")
    
    col_plano1, col_plano2 = st.columns([1, 1])
    
    with col_plano1:
        plano_selecionado = st.selectbox(
            "Selecione o Plano:",
            options=list(PLANOS.keys()),
            index=1,
            help="Escolha o plano base do cliente"
        )
        
        valor_plano = PLANOS[plano_selecionado]
        st.metric("Valor do Plano", f"R$ {valor_plano:.2f}")
    
    with col_plano2:
        extensoes_selecionadas = st.multiselect(
            "Selecione as Extensões (opcional):",
            options=list(EXTENSOES.keys()),
            help="Adicione extensões ao plano base"
        )
        
        valor_extensoes = sum([EXTENSOES[ext] for ext in extensoes_selecionadas])
        st.metric("Valor das Extensões", f"R$ {valor_extensoes:.2f}")
    
    # Cálculos
    valor_total_mensal = valor_plano + valor_extensoes
    comissao_mensal = calcular_comissao(valor_total_mensal, percentual_comissao)
    comissao_total_periodo = comissao_mensal * meses_comissao
    
    # ========== RESUMO DO PLANO ==========
    st.markdown("#### 💰 Resumo do Plano Configurado")
    
    col_resumo1, col_resumo2, col_resumo3, col_resumo4 = st.columns(4)
    
    with col_resumo1:
        st.metric("Plano Base", f"R$ {valor_plano:.2f}")
    
    with col_resumo2:
        st.metric("Extensões", f"R$ {valor_extensoes:.2f}")
    
    with col_resumo3:
        st.metric("Total Mensal", f"R$ {valor_total_mensal:.2f}",
                  delta=f"+R$ {valor_extensoes:.2f}" if valor_extensoes > 0 else None)
    
    with col_resumo4:
        st.metric("Comissão Mensal", f"R$ {comissao_mensal:.2f}",
                  delta=f"{percentual_comissao*100:.1f}%")
    
    # Detalhamento das extensões
    if extensoes_selecionadas:
        with st.expander("📋 Detalhamento das Extensões Selecionadas"):
            df_extensoes = pd.DataFrame({
                'Extensão': extensoes_selecionadas,
                'Valor Mensal': [f"R$ {EXTENSOES[ext]:.2f}" for ext in extensoes_selecionadas]
            })
            st.dataframe(df_extensoes, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ========== DADOS DE REFERÊNCIA ==========
    ticket_medio = df_filtered['Ticket Médio'].mean()
    roi_medio = df_filtered['ROI (%)'].mean()
    ltv_medio = df_filtered['LTV'].mean()
    cac_medio = df_filtered['CAC'].mean()
    ltv_estimado = valor_total_mensal * 12
    
    # Card resumo
    st.markdown(f"""
    <div class="metric-card">
        <h4>📋 Resumo do Modelo de Parceria</h4>
        <ul>
            <li><strong>Plano:</strong> {plano_selecionado} - R$ {valor_plano:.2f}/mês</li>
            <li><strong>Extensões:</strong> {len(extensoes_selecionadas)} selecionada(s) - R$ {valor_extensoes:.2f}/mês</li>
            <li><strong>Valor Total Mensal:</strong> R$ {valor_total_mensal:.2f}</li>
            <li><strong>Comissão:</strong> {percentual_comissao*100:.1f}% por {meses_comissao} meses</li>
            <li><strong>Comissão mensal:</strong> R$ {comissao_mensal:.2f}</li>
            <li><strong>Comissão total:</strong> R$ {comissao_total_periodo:.2f}</li>
        </ul>
        <hr>
        <h5>Dados de Referência:</h5>
        <ul>
            <li>Ticket Médio histórico: R$ {ticket_medio:.2f}</li>
            <li>CAC médio (via ads): R$ {cac_medio:.2f}</li>
            <li>LTV médio: R$ {ltv_medio:.2f}</li>
            <li>Custo por Lead: R$ {CUSTOS_LEAD['min']:.2f} - R$ {CUSTOS_LEAD['max']:.2f}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== ANÁLISE COMISSÃO VS CUSTO LEAD ==========
    st.markdown("### 💡 Análise: Comissão vs Custo por Lead")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico comparativo
        fig_comp = criar_grafico_comparativo(
            categorias=['Custo Lead Mín', 'Custo Lead Máx', 'Custo Lead Médio', 'Comissão Mensal'],
            valores=[
                CUSTOS_LEAD['min'],
                CUSTOS_LEAD['max'],
                CUSTOS_LEAD['medio'],
                comissao_mensal
            ],
            colors=['#fbbf24', '#f59e0b', '#d97706', '#10b981'],
            texts=[
                f"R$ {CUSTOS_LEAD['min']:.2f}",
                f"R$ {CUSTOS_LEAD['max']:.2f}",
                f"R$ {CUSTOS_LEAD['medio']:.2f}",
                f"R$ {comissao_mensal:.2f}"
            ],
            title=f"Comparação com Comissão de {percentual_comissao*100:.1f}%",
            height=350
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        # Análise do percentual
        ratio_min = (comissao_mensal / CUSTOS_LEAD['max']) * 100
        ratio_max = (comissao_mensal / CUSTOS_LEAD['min']) * 100
        ratio_medio = (comissao_mensal / CUSTOS_LEAD['medio']) * 100
        
        st.markdown("**Análise do Percentual:**")
        
        # Status baseado no ratio médio
        if ratio_medio <= 80:
            status_color = "🟢"
            status_text = "Excelente"
            status_class = "success-box"
        elif ratio_medio <= 100:
            status_color = "🟡"
            status_text = "Saudável"
            status_class = "success-box"
        elif ratio_medio <= 120:
            status_color = "🟠"
            status_text = "Limítrofe"
            status_class = "alert-box"
        else:
            status_color = "🔴"
            status_text = "Alto"
            status_class = "alert-box"
        
        st.metric("Comissão vs Lead Mín", f"{ratio_max:.0f}%")
        st.metric("Comissão vs Lead Máx", f"{ratio_min:.0f}%")
        st.metric("Comissão vs Lead Médio", f"{ratio_medio:.0f}%",
                  delta=f"{status_color} {status_text}")
        
        mensagem = f"O percentual de **{percentual_comissao*100:.1f}%** está **{status_text.lower()}**. A comissão mensal (R$ {comissao_mensal:.2f}) representa **{ratio_medio:.0f}%** do custo médio por lead."
        
        st.markdown(f"""
        <div class="{status_class}">
            <h4>{status_color} Avaliação</h4>
            <p>{mensagem}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== SIMULAÇÃO MENSAL ==========
    st.markdown("### 💰 Simulação: Receita Mensal por Cliente Indicado")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Comissão Mensal", f"R$ {comissao_mensal:,.2f}")
    
    with col2:
        st.metric(f"Comissão Total ({meses_comissao}m)", f"R$ {comissao_total_periodo:,.2f}")
    
    with col3:
        st.metric("Receita Empresa/Mês", f"R$ {valor_total_mensal:,.2f}")
    
    with col4:
        st.metric("LTV Estimado (12m)", f"R$ {ltv_estimado:,.2f}")
    
    # Tabela mês a mês
    st.markdown("#### 📅 Detalhamento Mês a Mês (Por Cliente)")
    
    meses_detalhe = [f"Mês {i+1}" for i in range(meses_comissao)]
    dados_mensais = {
        'Mês': meses_detalhe,
        'Receita Empresa': [f"R$ {valor_total_mensal:.2f}"] * meses_comissao,
        'Comissão Contador': [f"R$ {comissao_mensal:.2f}"] * meses_comissao,
        '% Comissão': [f"{percentual_comissao*100:.1f}%"] * meses_comissao,
        'Lucro Empresa': [f"R$ {valor_total_mensal - comissao_mensal:.2f}"] * meses_comissao
    }
    
    df_mensal = pd.DataFrame(dados_mensais)
    st.dataframe(df_mensal, use_container_width=True, hide_index=True)
    
    # Gráfico mês a mês
    fig_mensal = criar_grafico_barras(
        df=df_mensal,
        x_col='Mês',
        y_cols=['Receita Empresa', 'Comissão Contador'],
        names=['Receita Empresa', 'Comissão Contador'],
        colors=['#10b981', '#3b82f6'],
        title=f"Distribuição Mensal: {plano_selecionado} + {len(extensoes_selecionadas)} extensão(ões)",
        height=400,
        barmode='group'
    )
    st.plotly_chart(fig_mensal, use_container_width=True)
    
    st.markdown("---")
    
    # ========== COMPARATIVO CAC ==========
    st.markdown("### 📊 Comparativo: CAC Ads vs CAC Indicação")
    
    cac_indicacao = comissao_total_periodo
    economia_vs_ads = cac_medio - cac_indicacao
    cac_ltv_indicacao = calcular_cac_ltv_ratio(ltv_estimado, cac_indicacao)
    cac_ltv_ads = calcular_cac_ltv_ratio(ltv_medio, cac_medio)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cac = criar_grafico_comparativo(
            categorias=['CAC Google Ads', 'CAC Indicação'],
            valores=[cac_medio, cac_indicacao],
            colors=['#ea4335', '#10b981'],
            texts=[f'R$ {cac_medio:.2f}', f'R$ {cac_indicacao:.2f}'],
            title="Comparação de CAC",
            height=350
        )
        st.plotly_chart(fig_cac, use_container_width=True)
        
        st.metric(
            "Economia vs Ads",
            f"R$ {economia_vs_ads:,.2f}",
            f"{(economia_vs_ads/cac_medio)*100:.1f}%"
        )
    
    with col2:
        fig_ratio = go.Figure()
        fig_ratio.add_trace(go.Bar(
            x=['CAC:LTV Ads', 'CAC:LTV Indicação'],
            y=[cac_ltv_ads, cac_ltv_indicacao],
            marker_color=['#ea4335', '#10b981'],
            text=[f'{cac_ltv_ads:.1f}:1', f'{cac_ltv_indicacao:.1f}:1'],
            textposition='outside'
        ))
        fig_ratio.add_hline(
            y=4,
            line_dash="dash",
            line_color="orange",
            annotation_text="Benchmark Ideal (4:1)"
        )
        fig_ratio.update_layout(
            title="Relação CAC:LTV",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig_ratio, use_container_width=True)
    
    st.markdown("---")
    
    # ========== SIMULADOR DE IMPACTO ==========
    st.markdown("### 🎯 Simulador de Impacto")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Parâmetros da Simulação**")
        num_clientes = st.slider(
            "Número de clientes indicados/mês:",
            min_value=1,
            max_value=50,
            value=10,
            step=1
        )
        
        meses_simulacao = st.slider(
            "Período de simulação (meses):",
            min_value=1,
            max_value=12,
            value=6,
            step=1
        )
    
    with col2:
        # Cálculos
        total_clientes = num_clientes * meses_simulacao
        comissao_mensal_total = num_clientes * comissao_mensal
        comissao_total_simulacao = comissao_mensal_total * meses_simulacao
        receita_mensal_total = num_clientes * valor_total_mensal
        receita_total_simulacao = receita_mensal_total * meses_simulacao
        economia_total = economia_vs_ads * total_clientes
        
        st.markdown("**Resultados da Simulação**")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Total Clientes", f"{total_clientes}")
            st.metric("Comissão/Mês", f"R$ {comissao_mensal_total:,.2f}")
        
        with col_b:
            st.metric("Comissão Total", f"R$ {comissao_total_simulacao:,.2f}")
            st.metric("Receita/Mês", f"R$ {receita_mensal_total:,.2f}")
        
        with col_c:
            roi_indicacao = ((receita_total_simulacao - comissao_total_simulacao) / comissao_total_simulacao) * 100
            st.metric("ROI Indicação", f"{roi_indicacao:.1f}%")
            st.metric("Economia Total", f"R$ {economia_total:,.2f}")
    
    st.markdown("---")
    
    # ========== PROJEÇÃO MENSAL ==========
    st.markdown("### 📈 Projeção Mensal de Crescimento")
    
    meses_proj = [f"Mês {i+1}" for i in range(meses_simulacao)]
    receita_mensal_proj = []
    comissao_mensal_proj = []
    
    for i in range(meses_simulacao):
        clientes_ativos = min((i + 1) * num_clientes, num_clientes * min(i + 1, meses_comissao))
        receita_mes = clientes_ativos * valor_total_mensal
        receita_mensal_proj.append(receita_mes)
        
        if i < meses_comissao:
            comissao_mes = (i + 1) * num_clientes * comissao_mensal
        else:
            comissao_mes = num_clientes * meses_comissao * comissao_mensal
        
        comissao_mensal_proj.append(comissao_mes)
    
    fig_proj = criar_grafico_subplots(
        titulos=['Receita Mensal da Empresa', 'Comissão Mensal aos Contadores'],
        dados_list=[
            {
                'x': meses_proj,
                'y': receita_mensal_proj,
                'name': 'Receita Mensal',
                'color': '#10b981',
                'text': [f'R$ {v:,.0f}' for v in receita_mensal_proj]
            },
            {
                'x': meses_proj,
                'y': comissao_mensal_proj,
                'name': 'Comissão Mensal',
                'color': '#3b82f6',
                'text': [f'R$ {v:,.0f}' for v in comissao_mensal_proj]
            }
        ],
        height=600
    )
    st.plotly_chart(fig_proj, use_container_width=True)
    
    # Resumo da projeção
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Receita Mensal (último mês)", f"R$ {receita_mensal_proj[-1]:,.2f}")
    
    with col2:
        st.metric("Comissão Mensal (último mês)", f"R$ {comissao_mensal_proj[-1]:,.2f}")
    
    with col3:
        margem_ultimo_mes = ((receita_mensal_proj[-1] - comissao_mensal_proj[-1]) / receita_mensal_proj[-1]) * 100
        st.metric("Margem Líquida", f"{margem_ultimo_mes:.1f}%")
    
    st.markdown("---")
    
    # ========== ANÁLISE DE BENEFÍCIOS ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="success-box">
            <h4>✅ Vantagens da Parceria</h4>
            <ul>
                <li><strong>Menor CAC:</strong> Economia de R$ {economia_vs_ads:.2f} por cliente ({(economia_vs_ads/cac_medio)*100:.1f}% de redução)</li>
                <li><strong>Comissão competitiva:</strong> R$ {comissao_mensal:.2f}/mês ({percentual_comissao*100:.1f}% sobre R$ {valor_total_mensal:.2f})</li>
                <li><strong>Flexibilidade:</strong> Comissão ajustada ao plano + extensões</li>
                <li><strong>Maior qualidade:</strong> Indicações têm melhor fit</li>
                <li><strong>CAC:LTV melhor:</strong> {cac_ltv_indicacao:.1f}:1 vs {cac_ltv_ads:.1f}:1 (ads)</li>
                <li><strong>Sem risco:</strong> Pagamento após conversão</li>
                <li><strong>Escalável:</strong> Rede cresce exponencialmente</li>
                <li><strong>Confiança:</strong> Indicação profissional aumenta credibilidade</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📌 Pontos de Atenção</h4>
            <ul>
                <li><strong>Gestão:</strong> Sistema de tracking necessário</li>
                <li><strong>Treinamento:</strong> Contadores precisam conhecer o produto</li>
                <li><strong>SLA:</strong> Prazos claros para pagamentos</li>
                <li><strong>Qualificação:</strong> Critérios para indicações válidas</li>
                <li><strong>Suporte:</strong> Canal dedicado para parceiros</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== PLANO DE AÇÃO ==========
    st.markdown("### 🎯 Recomendações Estratégicas")
    
    st.markdown("""
    <div class="alert-box">
        <h4>📋 Plano de Ação Sugerido</h4>
        <ol>
            <li><strong>Fase 1 - Piloto (Mês 1-2):</strong>
                <ul>
                    <li>Selecionar 5-10 contadores parceiros</li>
                    <li>Criar material de apoio e treinamento</li>
                    <li>Definir processo de tracking</li>
                    <li>Meta: 3-5 clientes indicados</li>
                </ul>
            </li>
            <li><strong>Fase 2 - Expansão (Mês 3-6):</strong>
                <ul>
                    <li>Recrutar 20-30 contadores</li>
                    <li>Implementar gamificação</li>
                    <li>Criar programa de benefícios</li>
                    <li>Meta: 10-15 clientes/mês</li>
                </ul>
            </li>
            <li><strong>Fase 3 - Escala (Mês 7+):</strong>
                <ul>
                    <li>Automatizar onboarding</li>
                    <li>Criar comunidade de parceiros</li>
                    <li>Desenvolver co-marketing</li>
                    <li>Meta: 20+ clientes/mês</li>
                </ul>
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== KPIs ==========
    st.markdown("### 📊 KPIs para Monitoramento")
    
    kpis_parceria = pd.DataFrame({
        'KPI': [
            'Número de Parceiros Ativos',
            'Indicações Qualificadas/Mês',
            'Taxa de Conversão Indicações',
            'CAC Médio por Indicação',
            'LTV Médio Clientes Indicados',
            'Tempo Médio de Conversão',
            'NPS dos Parceiros',
            'Receita via Parceria (%)',
            'Ticket Médio Parceria'
        ],
        'Meta Mês 3': [
            '15', '10', '40%',
            f'R$ {cac_indicacao:.2f}',
            f'R$ {ltv_estimado:.2f}',
            '30 dias', '8+', '10%',
            f'R$ {valor_total_mensal:.2f}'
        ],
        'Meta Mês 6': [
            '30', '20', '45%',
            f'R$ {cac_indicacao*0.9:.2f}',
            f'R$ {ltv_estimado*1.1:.2f}',
            '25 dias', '9+', '20%',
            f'R$ {valor_total_mensal*1.15:.2f}'
        ],
        'Meta Mês 12': [
            '50+', '30+', '50%',
            f'R$ {cac_indicacao*0.8:.2f}',
            f'R$ {ltv_estimado*1.2:.2f}',
            '20 dias', '9+', '30%',
            f'R$ {valor_total_mensal*1.3:.2f}'
        ]
    })
    
    st.dataframe(kpis_parceria, use_container_width=True, hide_index=True)
    
    # ========== COMPARATIVO DE PLANOS ==========
    st.markdown("### 📊 Comparativo: Comissão por Tipo de Plano")
    
    dados_comparativo = []
    for nome_plano, valor_base in PLANOS.items():
        comissao_plano = calcular_comissao(valor_base, percentual_comissao)
        comissao_total_plano = comissao_plano * meses_comissao
        dados_comparativo.append({
            'Plano': nome_plano,
            'Valor Mensal': f'R$ {valor_base:.2f}',
            'Comissão Mensal': f'R$ {comissao_plano:.2f}',
            f'Comissão Total ({meses_comissao}m)': f'R$ {comissao_total_plano:.2f}'
        })
    
    df_comparativo = pd.DataFrame(dados_comparativo)
    st.dataframe(df_comparativo, use_container_width=True, hide_index=True)
    
    # Gráfico comparativo
    planos_nomes = list(PLANOS.keys())
    comissoes_mensais = [calcular_comissao(PLANOS[p], percentual_comissao) for p in planos_nomes]
    
    fig_comp_planos = criar_grafico_comparativo(
        categorias=planos_nomes,
        valores=comissoes_mensais,
        colors=['#10b981', '#3b82f6', '#8b5cf6'],
        texts=[f'R$ {v:.2f}' for v in comissoes_mensais],
        title=f"Comissão Mensal por Plano ({percentual_comissao*100:.1f}%)",
        height=400
    )
    st.plotly_chart(fig_comp_planos, use_container_width=True)
    
    st.info("""
    💡 **Nota:** Configure diferentes combinações para simular diversos cenários.
    Para análises precisas, rastreie a origem dos leads e planos contratados.
    """)