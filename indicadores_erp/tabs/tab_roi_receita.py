"""
Tab: Análise Inteligente de ROI em Receita (12 meses diluídos)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.calculations import calcular_roi


def clean_numeric_column(series: pd.Series) -> pd.Series:
    """
    Limpa coluna numérica sem alterar escala.

    - Remove apenas símbolos (R$, espaço, %).
    - NÃO remove ponto decimal e NÃO insere vírgula.
    - Confia no valor que vem do Excel (que já está como número ou string '2114.56').
    """
    s = series.astype(str).str.replace(r"[R$\s%]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")


def encontrar_payback(row: pd.Series, n_meses: int = 12) -> float | None:
    """
    Retorna o primeiro mês relativo em que o retorno acumulado fica >= 0.
    Usa as colunas roi_1m_valor, roi_2m_valor, ..., roi_Nm_valor.
    """
    for i in range(1, n_meses + 1):
        col = f"roi_{i}m_valor"
        if col in row.index:
            val = row[col]
            if pd.notnull(val) and val >= 0:
                return i
    return None


def gerar_insights_executivos_saas(resumo: dict) -> list[str]:
    """
    Gera insights em linguagem de CEO/CFO para SaaS ERP,
    baseando-se em ROI diluído, payback, LTV e ticket.
    """
    insights = []

    invest_total = resumo.get("invest_total", 0)
    retorno_12m = resumo.get("retorno_12m_total", 0)
    roi_3m = resumo.get("roi_3m_pct_total")
    roi_6m = resumo.get("roi_6m_pct_total")
    roi_12m = resumo.get("roi_12m_pct_total")
    payback_medio = resumo.get("payback_medio")
    payback_mediano = resumo.get("payback_mediano")
    pct_payback_ate_6 = resumo.get("pct_payback_ate_6")
    ltv_medio = resumo.get("ltv_medio")
    ticket_medio = resumo.get("ticket_medio")

    # Múltiplo de retorno em 12 meses
    if invest_total > 0 and retorno_12m is not None:
        multiplo = retorno_12m / invest_total
        insights.append(
            f"Em 12 meses, cada R$ 1,00 investido em aquisição gera, em média, "
            f"~R$ {multiplo:,.2f} de lucro líquido. Isso define o quanto a "
            f"empresa pode escalar a verba de marketing sem pressionar caixa."
        )

    # Qualidade do ROI 12m
    if roi_12m is not None:
        if roi_12m >= 400:
            insights.append(
                f"O ROI de {roi_12m:,.0f}% em 12 meses está em um nível muito "
                f"atrativo para SaaS ERP. Em tese, há espaço para aumentar "
                f"investimento mantendo margens saudáveis."
            )
        elif roi_12m >= 200:
            insights.append(
                f"O ROI de {roi_12m:,.0f}% em 12 meses é bom. O foco agora deve ser "
                f"consolidar processos de aquisição e vendas para manter essa "
                f"performance à medida que o investimento aumenta."
            )
        else:
            insights.append(
                f"O ROI de {roi_12m:,.0f}% em 12 meses é baixo para um modelo de "
                f"recorrência. É importante revisar mix de canais, funil de vendas e "
                f"experiência de onboarding antes de escalar agressivamente."
            )

    # Comparação 3m x 12m (onde está o valor)
    if roi_3m is not None and roi_12m is not None:
        delta = roi_12m - roi_3m
        if delta > 150:
            insights.append(
                "Grande parte do valor gerado pelos clientes vem depois do 3º mês. "
                "Isso é típico de SaaS com boa retenção: é crítico proteger churn "
                "e lifetime value, não apenas o CAC imediato."
            )
        elif delta < 50:
            insights.append(
                "A maior parte do retorno acontece ainda nos primeiros 3 meses. "
                "Isso sugere um ciclo de payback curto, favorável para reinvestir "
                "caixa rapidamente, mas vale monitorar se o LTV não está sendo "
                "comprometido por churn antecipado."
            )

    # Payback
    if payback_medio is not None:
        if payback_medio <= 4:
            insights.append(
                f"O payback médio de ~{payback_medio:.1f} meses é excelente para SaaS. "
                f"Isso reduz a necessidade de capital externo para crescer."
            )
        elif payback_medio <= 8:
            insights.append(
                f"O payback médio de ~{payback_medio:.1f} meses é razoável. "
                f"Continua viável crescer, mas o planejamento de caixa precisa "
                f"considerar esse ciclo de retorno."
            )
        else:
            insights.append(
                f"O payback médio de ~{payback_medio:.1f} meses é longo. "
                f"Para crescer de forma segura, a empresa precisa de mais capital "
                f"ou de ganhos em eficiência (CAC, upsell, churn)."
            )

    if pct_payback_ate_6 is not None:
        insights.append(
            f"Cerca de {pct_payback_ate_6:.0f}% das coortes recuperam o investimento "
            f"em até 6 meses. Quanto maior esse percentual, mais previsível é a "
            f"reciclagem de caixa em aquisição."
        )

    # Relação LTV x ticket
    if ltv_medio is not None and ticket_medio is not None and ticket_medio > 0:
        multiples = ltv_medio / ticket_medio
        insights.append(
            f"O LTV médio equivale a aproximadamente {multiples:,.1f} vezes o "
            f"ticket médio mensal, consistente com um cliente que permanece na base "
            f"por vários anos. Isso apoia um CAC mais agressivo, desde que o churn "
            f"se mantenha controlado."
        )

    if not insights:
        insights.append(
            "Ainda não há dados suficientes para uma leitura robusta de ROI diluído. "
            "Recomenda-se acumular mais meses de histórico."
        )

    return insights


def render_tab_roi_receita(df_principal=None):
    """
    Aba de análise inteligente de ROI em Receita.

    df_principal: DataFrame principal do app (opcional),
                  usado para enriquecer os insights com LTV, Ticket Médio, etc.
    """
    st.header("Análise Inteligente de Receita, Investimento e ROI (12 meses)")
    st.write(
        "Envie a planilha de ROI diluído com a estrutura:\n\n"
        "- Mês\n"
        "- Receita web\n"
        "- Total Ads\n"
        "As colunas 1º MÊS, 2º MÊS etc. da planilha serão ignoradas para o cálculo,\n"
        "pois o ROI diluído será recalculado internamente pela fórmula:\n"
        "  - ROI_1 = Receita - Investimento\n"
        "  - ROI_n = ROI_{n-1} + Receita\n"
    )

    uploaded_file = st.file_uploader(
        "Selecione sua planilha de ROI em Receita", type=["xlsx", "xls", "csv"]
    )

    if not uploaded_file:
        return

    # --- LEITURA E PREPARAÇÃO DO DATAFRAME ---
    try:
        if uploaded_file.name.lower().endswith((".xlsx", ".xls")):
            df_raw = pd.read_excel(uploaded_file, engine="openpyxl", header=None)
        else:
            df_raw = pd.read_csv(uploaded_file, header=None)

        # Remove linhas/colunas totalmente vazias
        df_raw.dropna(axis="rows", how="all", inplace=True)
        df_raw.dropna(axis="columns", how="all", inplace=True)

        # Na sua planilha, a 1ª linha é decorativa ("CÁLCULO ROI DILUÍDO ...")
        # e a 2ª linha (índice 1) é o cabeçalho real: Mês, Receita web, Total Ads
        if len(df_raw) < 2:
            raise ValueError("Planilha não tem linhas suficientes para identificar o cabeçalho.")

        header_row = df_raw.iloc[1]
        df = df_raw.iloc[2:].copy()  # dados começam depois da linha de cabeçalho real
        df.columns = header_row

        # Remover colunas com nomes duplicados
        df = df.loc[:, ~df.columns.astype(str).duplicated()].copy()

        # Normalizar nomes de colunas: remover espaços, tratar NaN/vazios
        novas_cols = []
        for i, c in enumerate(df.columns):
            nome = str(c).strip()
            if nome == "" or nome.lower() in ("nan", "none"):
                nome = f"col_{i}"  # nome genérico para colunas sem título
            novas_cols.append(nome)
        df.columns = novas_cols

    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        st.warning(
            "Confirme que a segunda linha da planilha contém os cabeçalhos: "
            "Mês, Receita web, Total Ads."
        )
        return

    if df.empty:
        st.warning("A planilha está vazia ou não foi possível extrair dados.")
        return

    with st.expander("Pré-visualização dos dados carregados", expanded=False):
        st.dataframe(df.head())

    # --- VALIDAÇÃO DAS COLUNAS ESPERADAS ---
    col_mes = "Mês"
    col_receita = "Receita web"
    col_ads = "Total Ads"

    missing = [c for c in [col_mes, col_receita, col_ads] if c not in df.columns]
    if missing:
        st.error(
            "A planilha não contém as colunas obrigatórias: "
            + ", ".join(missing)
        )
        return

    # --- LIMPEZA E CÁLCULO DAS MÉTRICAS BÁSICAS ---
    df["periodo"] = pd.to_datetime(df[col_mes], errors="coerce")
    df.dropna(subset=["periodo"], inplace=True)

    if df.empty:
        st.error("Nenhum valor de data válido na coluna Mês.")
        return

    df["mes_ano_str"] = df["periodo"].dt.strftime("%Y-%m")

    # Numéricos de receita e investimento
    df["receita_web"] = clean_numeric_column(df[col_receita])
    df["total_ads"] = clean_numeric_column(df[col_ads])
    df.dropna(subset=["receita_web", "total_ads"], inplace=True)

    if df.empty:
        st.error("Sem dados numéricos válidos em Receita web e Total Ads.")
        return

    # ROI simples por mês
    df["roi_simples_pct"] = df.apply(
        lambda row: calcular_roi(row["receita_web"], row["total_ads"]), axis=1
    )

    # --- RECALCULAR ROI DILUÍDO DE 1 A 12 MESES (SEGUINDO SUA FÓRMULA) ---
    # ROI_1 = Receita - Investimento
    # ROI_n = ROI_{n-1} + Receita
    for n in range(1, 13):
        if n == 1:
            df[f"roi_{n}m_valor"] = df["receita_web"] - df["total_ads"]
        else:
            df[f"roi_{n}m_valor"] = df[f"roi_{n-1}m_valor"] + df["receita_web"]

    # ROI em % por coorte
    for n in range(1, 13):
        df[f"roi_{n}m_pct"] = (
            df[f"roi_{n}m_valor"] / df["total_ads"].replace(0, pd.NA)
        ) * 100

    # Payback por coorte
    df["payback_meses"] = df.apply(lambda row: encontrar_payback(row, 12), axis=1)

    # --- RESUMO GLOBAL PARA VISÃO EXECUTIVA ---
    invest_total = df["total_ads"].sum()
    receita_mes0_total = df["receita_web"].sum()

    resumo = {
        "invest_total": invest_total,
        "receita_mes0_total": receita_mes0_total,
        "retorno_3m_total": df["roi_3m_valor"].sum(),
        "retorno_6m_total": df["roi_6m_valor"].sum(),
        "retorno_12m_total": df["roi_12m_valor"].sum(),
    }

    if invest_total > 0:
        resumo["roi_3m_pct_total"] = (resumo["retorno_3m_total"] / invest_total) * 100
        resumo["roi_6m_pct_total"] = (resumo["retorno_6m_total"] / invest_total) * 100
        resumo["roi_12m_pct_total"] = (resumo["retorno_12m_total"] / invest_total) * 100
    else:
        resumo["roi_3m_pct_total"] = None
        resumo["roi_6m_pct_total"] = None
        resumo["roi_12m_pct_total"] = None

    # Payback agregado
    paybacks_validos = df["payback_meses"].dropna()
    if not paybacks_validos.empty:
        resumo["payback_medio"] = paybacks_validos.mean()
        resumo["payback_mediano"] = paybacks_validos.median()
        resumo["pct_payback_ate_6"] = (paybacks_validos <= 6).mean() * 100
    else:
        resumo["payback_medio"] = None
        resumo["payback_mediano"] = None
        resumo["pct_payback_ate_6"] = None

    # Integra com df_principal (LTV / Ticket Médio), se disponível
    if df_principal is not None and not df_principal.empty:
        if "LTV" in df_principal.columns:
            resumo["ltv_medio"] = df_principal["LTV"].mean()
        else:
            resumo["ltv_medio"] = None

        if "Ticket Médio" in df_principal.columns:
            resumo["ticket_medio"] = df_principal["Ticket Médio"].mean()
        else:
            resumo["ticket_medio"] = None
    else:
        resumo["ltv_medio"] = None
        resumo["ticket_medio"] = None

    # --- EXIBIÇÃO: KPI GERAL ---
    st.markdown("---")
    st.subheader("Visão Geral do Período (nível CEO / CFO)")

    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    col_k1.metric("Investimento Total em Ads", f"R$ {invest_total:,.2f}")
    col_k2.metric("Receita Web (Mês 0)", f"R$ {receita_mes0_total:,.2f}")
    col_k3.metric("Retorno Líquido em 12m", f"R$ {resumo['retorno_12m_total']:,.2f}")
    if resumo["roi_12m_pct_total"] is not None:
        col_k4.metric("ROI 12m (acumulado)", f"{resumo['roi_12m_pct_total']:,.1f}%")

    # --- ROI SIMPLES POR MÊS ---
    st.markdown("---")
    st.subheader("ROI Simples por Mês (Receita web x Total Ads)")

    df_ordered = df.sort_values("periodo")

    fig_roi_mensal = px.line(
        df_ordered,
        x="mes_ano_str",
        y="roi_simples_pct",
        markers=True,
        labels={"mes_ano_str": "Mês", "roi_simples_pct": "ROI (%)"},
        title="ROI Simples por Mês",
    )
    st.plotly_chart(fig_roi_mensal, use_container_width=True)

    fig_bar_receita_ads = px.bar(
        df_ordered,
        x="mes_ano_str",
        y=["receita_web", "total_ads"],
        barmode="group",
        labels={
            "mes_ano_str": "Mês",
            "value": "R$",
            "variable": "Métrica",
        },
        title="Receita web x Total Ads por Mês",
    )
    st.plotly_chart(fig_bar_receita_ads, use_container_width=True)

    # --- ROI DILUÍDO POR COORTE (3m, 6m, 12m) ---
    st.markdown("---")
    st.subheader("ROI Diluído por Coorte (3, 6 e 12 meses)")

    df_coorte = df_ordered[["mes_ano_str", "roi_3m_pct", "roi_6m_pct", "roi_12m_pct"]].copy()
    df_coorte = df_coorte.melt(
        id_vars="mes_ano_str",
        var_name="horizonte",
        value_name="roi_pct",
    )
    df_coorte["horizonte"] = df_coorte["horizonte"].map(
        {
            "roi_3m_pct": "3 meses",
            "roi_6m_pct": "6 meses",
            "roi_12m_pct": "12 meses",
        }
    )

    fig_roi_coorte = px.line(
        df_coorte,
        x="mes_ano_str",
        y="roi_pct",
        color="horizonte",
        markers=True,
        labels={
            "mes_ano_str": "Mês de investimento (coorte)",
            "roi_pct": "ROI (%)",
            "horizonte": "Horizonte",
        },
        title="ROI por Coorte e Horizonte (3m / 6m / 12m)",
    )
    st.plotly_chart(fig_roi_coorte, use_container_width=True)

    # --- PAYBACK ---
    st.markdown("---")
    st.subheader("Payback por Coorte (em meses relativos)")

    if not paybacks_validos.empty:
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Payback Médio", f"{resumo['payback_medio']:.1f} meses")
        col_p2.metric("Payback Mediano", f"{resumo['payback_mediano']:.1f} meses")
        col_p3.metric(
            "% Coortes com Payback ≤ 6 meses",
            f"{resumo['pct_payback_ate_6']:.0f}%",
        )

        with st.expander("Distribuição de Payback por coorte"):
            st.dataframe(
                df_ordered[["mes_ano_str", "payback_meses"]].rename(
                    columns={
                        "mes_ano_str": "Mês de investimento",
                        "payback_meses": "Payback (meses)",
                    }
                )
            )
    else:
        st.info("Não foi possível calcular payback (retornos nunca ficam positivos).")

    # --- MAPA DE CALOR DE COORTES (ROI %) ---
    st.markdown("---")
    st.subheader("Mapa de Calor: ROI (%) por Coorte x Mês Relativo")

    cols_roi_heat = [f"roi_{n}m_pct" for n in range(1, 13)]
    heat_matrix = df_ordered.set_index("mes_ano_str")[cols_roi_heat]

    fig_heat = px.imshow(
        heat_matrix,
        aspect="auto",
        color_continuous_scale="RdYlGn",
        origin="lower",
        labels={
            "x": "Mês relativo (1º, 2º, ...)",
            "y": "Mês de investimento (coorte)",
            "color": "ROI (%)",
        },
        title="ROI (%) por Coorte e Mês Relativo",
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # --- RESUMO EXECUTIVO EM TEXTO ---
    st.markdown("---")
    st.subheader("Resumo Executivo (SaaS ERP)")

    insights = gerar_insights_executivos_saas(resumo)
    for txt in insights:
        st.markdown(f"- {txt}")

    with st.expander("Ver tabela completa utilizada na análise"):
        st.dataframe(df_ordered)