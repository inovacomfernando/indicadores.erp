"""
Tab 6: Forecast e Análise Preditiva Inteligente

IMPORTANTE - CONTROLE DE APURAÇÃO:
==================================
Os dados são apurados no PRIMEIRO DIA ÚTIL do mês seguinte.

Para atualizar meses apurados, edite o arquivo: config_apuracao.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.forecast import (
    prever_cenarios,
    avaliar_qualidade_previsao,
    interpretar_tendencia
)
from utils.charts import criar_grafico_projecao

# Tenta importar a configuração de apuração
try:
    from config.config_apuracao import get_meses_apurados, get_info_apuracao
    USA_CONFIG_APURACAO = True
except ImportError:
    USA_CONFIG_APURACAO = False
    # Fallback para lista hardcoded
    # IMPORTANTE: Set/25 está incluído - é o último mês apurado
    MESES_APURADOS_FALLBACK = ['Mai/25', 'Jun/25', 'Jul/25', 'Ago/25', 'Set/25']


def get_ultimo_mes_apurado(df):
    """
    Identifica o último mês oficialmente apurado
    
    REGRA: Dados são apurados no primeiro dia útil do mês seguinte
    Portanto, só consideramos meses COMPLETOS e já processados
    """
    if USA_CONFIG_APURACAO:
        meses_apurados = get_meses_apurados()
    else:
        meses_apurados = MESES_APURADOS_FALLBACK
    
    # Pega o último mês da lista de apurados que existe no DataFrame
    for mes in reversed(meses_apurados):
        if mes in df['Mês'].values:
            return mes
    
    return None


def get_meses_forecast(ultimo_mes_apurado, df):
    """
    Retorna os meses para forecast baseado no último mês apurado
    """
    todos_meses = df['Mês'].tolist()
    
    # Encontra o índice do último mês apurado
    try:
        idx_ultimo = todos_meses.index(ultimo_mes_apurado)
    except ValueError:
        return []
    
    # Retorna os meses seguintes que ainda não foram apurados
    meses_forecast = todos_meses[idx_ultimo + 1:]
    # Remove zeros do final
    meses_forecast = [m for m in meses_forecast if m]
    
    return meses_forecast


def aplicar_ajustes_precos(previsao_base, mes, ticket_medio_atual):
    """
    Aplica ajustes de preços dos novos planos
    
    Novos preços:
    - MEI: R$ 84,90
    - Simples Nacional: R$ 154,90
    - Lucro Real/Presumido: R$ 199,90
    
    Ticket Médio estimado: R$ 146,56 (considerando distribuição de clientes)
    """
    # Novo ticket médio ponderado (estimativa)
    novo_ticket_medio = 146.56
    
    # Aumento percentual
    aumento_percentual = (novo_ticket_medio / ticket_medio_atual) - 1
    
    # Aplica gradualmente a partir de Out/25
    if mes == 'Out/25':
        # Início gradual (20% dos clientes no novo preço)
        fator = 1 + (aumento_percentual * 0.20)
    elif mes == 'Nov/25':
        # Metade dos clientes migrados
        fator = 1 + (aumento_percentual * 0.50)
    elif mes == 'Dez/25':
        # Maioria dos clientes no novo preço
        fator = 1 + (aumento_percentual * 0.80)
    else:
        # Totalmente migrado
        fator = 1 + aumento_percentual
    
    return previsao_base * fator


def aplicar_campanha_black_friday(previsao_base, mes, metrica):
    """
    Aplica efeito da campanha Black Friday
    
    Campanha:
    - Última semana de Out/25: Esquenta Black (pequeno aumento)
    - Nov/25 completo: Black Friday principal (grande aumento)
    - Até 12/Dez: Extensão (redução gradual)
    - Pós 12/Dez: Parada operacional (forte redução)
    """
    
    if metrica in ['Leads', 'Sessões', 'Primeira Visita', 'Clientes Web']:
        # Aumento de tráfego e conversões
        if mes == 'Out/25':
            # Esquenta Black (última semana representa ~25% do mês)
            return previsao_base * 1.15  # +15% no mês
        elif mes == 'Nov/25':
            # Black Friday mês completo
            return previsao_base * 1.45  # +45% no mês
        elif mes == 'Dez/25':
            # Até dia 12 (40% do mês) + parada depois
            return previsao_base * 0.85  # -15% (média do mês)
    
    elif metrica in ['Receita Web']:
        # Receita considerando desconto de até 50% nos 4 primeiros meses
        if mes == 'Out/25':
            # Esquenta com desconto menor
            return previsao_base * 1.10  # +10% (mais clientes, desconto moderado)
        elif mes == 'Nov/25':
            # Black Friday com desconto maior, mas muito mais volume
            return previsao_base * 1.25  # +25% (desconto compensado por volume)
        elif mes == 'Dez/25':
            # Redução por parada
            return previsao_base * 0.75  # -25%
    
    elif metrica in ['CAC']:
        # CAC tende a subir em campanhas agressivas
        if mes == 'Out/25':
            return previsao_base * 1.10
        elif mes == 'Nov/25':
            return previsao_base * 1.20  # Competição aumenta CPC
        elif mes == 'Dez/25':
            return previsao_base * 0.90  # Redução de investimento
    
    elif metrica in ['Total Ads', 'Custo Meta', 'Custo Google']:
        # Aumento de investimento em ads
        if mes == 'Out/25':
            return previsao_base * 1.20
        elif mes == 'Nov/25':
            return previsao_base * 1.50  # Investimento máximo
        elif mes == 'Dez/25':
            return previsao_base * 0.60  # Redução significativa
    
    return previsao_base


def render_tab_forecast(df):
    """
    Renderiza a tab de forecast com lógica de apuração
    
    Args:
        df: DataFrame completo
    """
    st.subheader("🔮 Forecast: Cenários para Projeção e Estratégia")
    
    # Identifica último mês apurado
    ultimo_mes = get_ultimo_mes_apurado(df)
    
    if not ultimo_mes:
        st.error("❌ Não há dados apurados suficientes para gerar previsões.")
        return
    
    # Info sobre apuração
    if USA_CONFIG_APURACAO:
        info = get_info_apuracao()
        st.info(f"""
        📅 **Informações sobre Apuração e Forecast:**
        
        - **Último mês apurado:** {info['ultimo_mes']}
        - **Próximo mês a apurar:** {info['proximo_mes']}
        - **Data estimada de apuração:** {info['data_estimada']}
        - **Total de meses apurados:** {info['total_meses']}
        - **Forecast baseado em:** Dados históricos até {info['ultimo_mes']}
        
        ⚠️ **Atenção:** 
        - Apenas meses COMPLETOS e APURADOS são usados nas previsões
        - Para atualizar após nova apuração, edite: `config/config_apuracao.py`
        """)
    else:
        st.info(f"""
        📅 **Informações sobre Apuração e Forecast:**
        
        - **Último mês apurado:** {ultimo_mes}
        - **Próximo mês a ser apurado:** Após {ultimo_mes}, no primeiro dia útil do mês seguinte
        - **Forecast baseado em:** Dados históricos de {ultimo_mes} e anteriores
        
        ⚠️ **Atenção:** 
        - Meses com dados parciais NÃO são considerados para forecast
        - Apenas meses COMPLETOS e APURADOS são usados nas previsões
        - Para facilitar atualizações, crie o arquivo `config/config_apuracao.py`
        """)
    
    # Meses para forecast
    meses_forecast = get_meses_forecast(ultimo_mes, df)
    
    if not meses_forecast:
        st.warning("⚠️ Não há períodos futuros para projeção.")
        return
    
    st.markdown(f"**Projetando para:** {', '.join(meses_forecast)}")
    
    # Debug: Mostra status de cada mês
    with st.expander("🔍 Ver status detalhado dos meses"):
        st.markdown("#### Status de Apuração por Mês")
        
        if USA_CONFIG_APURACAO:
            meses_apurados_lista = get_meses_apurados()
        else:
            meses_apurados_lista = MESES_APURADOS_FALLBACK
        
        todos_meses = df['Mês'].tolist()
        status_data = []
        
        for mes in todos_meses:
            if not mes or mes == '':
                continue
                
            valores = df[df['Mês'] == mes].iloc[0]
            tem_dados = valores['Sessões'] > 0 or valores['Receita Web'] > 0
            esta_apurado = mes in meses_apurados_lista
            
            status_data.append({
                'Mês': mes,
                'Tem Dados': '✅ Sim' if tem_dados else '❌ Não',
                'Oficialmente Apurado': '✅ SIM' if esta_apurado else '❌ NÃO',
                'Usado no Forecast': '✅ Sim' if esta_apurado else '❌ Não',
                'Status': '📊 Histórico' if esta_apurado else ('🔮 Projeção' if mes in meses_forecast else '⏳ Aguardando')
            })
        
        df_status = pd.DataFrame(status_data)
        st.dataframe(df_status, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Legenda:**
        - ✅ **Oficialmente Apurado**: Mês está na lista de controle e é usado para gerar previsões
        - ❌ **NÃO Apurado**: Mês não está oficialmente apurado (mesmo tendo dados parciais)
        - 📊 **Histórico**: Dados usados como base para previsões
        - 🔮 **Projeção**: Meses que serão previstos
        - ⏳ **Aguardando**: Mês com dados parciais aguardando apuração oficial
        """)
    
    
    # Info sobre campanhas
    if 'Out/25' in meses_forecast or 'Nov/25' in meses_forecast or 'Dez/25' in meses_forecast:
        st.markdown("""
        ---
        ### 🎯 Eventos Considerados no Forecast
        
        **Aumento de Preços dos Planos:**
        - MEI: R$ 84,90
        - Simples Nacional: R$ 154,90
        - Lucro Real/Presumido: R$ 199,90
        
        **Campanha Black Friday 2025:**
        - 🔥 **Última semana de Out/25:** Esquenta Black (aumento moderado)
        - 🚀 **Nov/25 completo:** Black Friday principal (até 50% OFF nos 4 primeiros meses)
        - 📉 **Até 12/Dez:** Extensão da campanha
        - 🛑 **Pós 12/Dez:** Parada operacional de fim de ano
        
        ---
        """)
    
    try:
        # Filtra apenas dados apurados (usando a lista oficial de meses apurados)
        if USA_CONFIG_APURACAO:
            meses_apurados_lista = get_meses_apurados()
        else:
            meses_apurados_lista = MESES_APURADOS_FALLBACK
        
        # Filtra o DataFrame para incluir APENAS meses apurados
        df_historico = df[df['Mês'].isin(meses_apurados_lista)].copy()
        
        if len(df_historico) < 3:
            st.error("❌ Dados históricos insuficientes para gerar previsões (mínimo 3 meses apurados).")
            return
        
        meses_historico = df_historico['Mês'].tolist()
        
        # Exibe quais meses estão sendo usados
        st.success(f"✅ Usando dados históricos de: {', '.join(meses_historico)}")
        
        # KPIs para previsão
        kpis = ["Leads", "Clientes Web", "Receita Web", "CAC", "LTV", "ROI (%)", "Total Ads"]
        
        # Ticket médio atual para cálculo de ajuste
        ticket_medio_atual = df_historico['Ticket Médio'].iloc[-1]
        
        # Calcular previsões
        resultados = {}
        for kpi in kpis:
            resultados[kpi] = prever_cenarios(df_historico, kpi, num_previsoes=len(meses_forecast))
        
        # Exibir resultados
        st.markdown("### Previsões com Validação Estatística")
        
        for kpi in kpis:
            if resultados[kpi]:
                st.markdown(f"#### {kpi}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Aplica ajustes nas previsões
                    previsoes_ajustadas = []
                    otimista_ajustado = []
                    conservador_ajustado = []
                    
                    for i, mes in enumerate(meses_forecast):
                        prev_base = resultados[kpi]['previsao'].iloc[i]
                        otim_base = resultados[kpi]['otimista'].iloc[i]
                        cons_base = resultados[kpi]['conservador'].iloc[i]
                        
                        # Aplica campanha Black Friday
                        prev_base = aplicar_campanha_black_friday(prev_base, mes, kpi)
                        otim_base = aplicar_campanha_black_friday(otim_base, mes, kpi)
                        cons_base = aplicar_campanha_black_friday(cons_base, mes, kpi)
                        
                        # Aplica ajuste de preços (apenas para Receita Web e LTV)
                        if kpi in ['Receita Web', 'LTV']:
                            prev_base = aplicar_ajustes_precos(prev_base, mes, ticket_medio_atual)
                            otim_base = aplicar_ajustes_precos(otim_base, mes, ticket_medio_atual)
                            cons_base = aplicar_ajustes_precos(cons_base, mes, ticket_medio_atual)
                        
                        previsoes_ajustadas.append(prev_base)
                        otimista_ajustado.append(otim_base)
                        conservador_ajustado.append(cons_base)
                    
                    # Gráfico com previsões ajustadas
                    fig = criar_grafico_projecao(
                        meses_historico=meses_historico,
                        valores_historico=df_historico[kpi].tolist(),
                        meses_previsao=meses_forecast,
                        valores_previsao=previsoes_ajustadas,
                        valores_otimista=otimista_ajustado,
                        valores_conservador=conservador_ajustado,
                        title=f"Previsão: {kpi} (com ajustes de campanha)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Métricas de qualidade
                    st.markdown("**Métricas de Qualidade**")
                    metricas = resultados[kpi]['metricas']
                    
                    # Avaliação
                    avaliacao = avaliar_qualidade_previsao(
                        metricas['R²'],
                        metricas['MAPE']
                    )
                    
                    st.metric(
                        "R² (Ajuste do Modelo)",
                        f"{metricas['R²']:.3f}",
                        f"{avaliacao['r2']['emoji']} {avaliacao['r2']['status']}"
                    )
                    
                    st.metric(
                        "MAPE (Erro %)",
                        f"{metricas['MAPE']:.1f}%",
                        f"{avaliacao['mape']['emoji']} {avaliacao['mape']['status']}"
                    )
                    
                    # Tendência
                    tend = interpretar_tendencia(
                        metricas['Tendência (tau)'],
                        metricas['P-valor tendência']
                    )
                    
                    st.metric(
                        "Tendência",
                        f"{metricas['Tendência (tau)']:.3f}",
                        f"{tend['emoji']} {tend['direcao']}"
                    )
                
                st.markdown("---")
        
        # Análise de correlação
        st.markdown("### Análise de Correlação entre KPIs")
        corr_matrix = df_historico[kpis].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            labels=dict(color="Correlação"),
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig_corr.update_layout(
            title="Matriz de Correlação (Dados Históricos)",
            height=500
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Insights
        st.markdown("### 💡 Insights e Recomendações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Sobre as Previsões:**
            - ✅ Modelos com R² > 0.8 são altamente confiáveis
            - ✅ MAPE < 10% indica previsões precisas
            - ✅ Tendências significativas sugerem padrões consistentes
            
            **Ajustes Aplicados:**
            - 📊 Efeito da campanha Black Friday
            - 💰 Impacto do aumento de preços
            - 📅 Sazonalidade de fim de ano
            """)
        
        with col2:
            st.markdown("""
            **Limitações do Modelo:**
            - ⚠️ Assume comportamento baseado em histórico
            - ⚠️ Eventos inesperados podem alterar previsões
            - ⚠️ Requer atualização após cada apuração
            
            **Próximos Passos:**
            1. Monitorar resultados vs. previsões
            2. Ajustar estratégia com base nos dados
            3. Atualizar modelo após cada apuração
            """)
    
    except Exception as e:
        st.error(f"""
        ❌ Erro ao gerar previsões e análises estatísticas.
        
        Erro: {str(e)}
        
        Verifique:
        1. Formato dos dados
        2. Quantidade de dados históricos
        3. Dependências instaladas
        """)
