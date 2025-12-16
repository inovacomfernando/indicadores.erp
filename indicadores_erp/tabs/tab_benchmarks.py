"""
Tab 4: Comparação com Benchmarks + Análise Preditiva
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error


def _safe_mean(df: pd.DataFrame, col: str):
    if col not in df.columns or df[col].dropna().empty:
        return np.nan
    return df[col].mean()


def _status_vs_interval(valor, minimo=None, maximo=None, maior_melhor=True):
    """
    Compara um valor com um intervalo de benchmark.

    - Para métricas de 'quanto maior melhor' (ex: ROI, TC): maior_melhor=True.
    - Para métricas de 'quanto menor melhor' (ex: CAC): maior_melhor=False.
    """
    if valor is None or np.isnan(valor):
        return "⚪ Sem dados"

    if minimo is not None and maximo is not None:
        # está dentro da faixa
        if minimo <= valor <= maximo:
            return "🟢 Dentro do benchmark"
        # fora da faixa – decide se é bom ou ruim pelo maior_melhor
        if maior_melhor:
            if valor > maximo:
                return "🟢 Acima do benchmark (melhor)"
            else:
                return "🔴 Abaixo do benchmark"
        else:
            if valor < minimo:
                return "🟢 Abaixo do benchmark (melhor)"
            else:
                return "🔴 Acima do benchmark"
    else:
        # só mínimo definido (ex: CAC:LTV ≥ 3)
        if minimo is not None:
            if maior_melhor:
                if valor >= minimo:
                    return "🟢 Acima do mínimo"
                else:
                    return "🔴 Abaixo do mínimo"
            else:
                if valor <= minimo:
                    return "🟢 Abaixo do máximo"
                else:
                    return "🔴 Acima do máximo"

    return "⚪ N/A"


def _parse_caclvt_mean(df: pd.DataFrame, col: str = "CAC:LTV"):
    """
    CAC:LTV vem como '3.5:1'. Vamos pegar só o número antes dos dois pontos.
    """
    if col not in df.columns:
        return np.nan

    def _to_float(x):
        if pd.isna(x):
            return np.nan
        s = str(x).split(":")[0].replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return np.nan

    vals = df[col].apply(_to_float)
    if vals.dropna().empty:
        return np.nan
    return vals.mean()


def render_tab_benchmarks(df_filtered: pd.DataFrame, benchmarks: dict):
    """
    Renderiza a tab de benchmarks + análise preditiva.

    Args:
        df_filtered: DataFrame filtrado (dados reais)
        benchmarks: Dict com benchmarks (pode ser ignorado se não estiver usando)
    """
    st.subheader("Comparação com Benchmarks SaaS ERP (Avançado)")

    if df_filtered is None or df_filtered.empty:
        st.info("Sem dados filtrados para comparar com benchmarks.")
        return

    # ==========================
    # 1. Cálculo das suas médias
    # ==========================
    tc_usuarios = _safe_mean(df_filtered, "TC Usuários (%)")
    tc_leads = _safe_mean(df_filtered, "TC Leads (%)")
    cac = _safe_mean(df_filtered, "CAC")
    caclvt = _parse_caclvt_mean(df_filtered, "CAC:LTV")
    roi = _safe_mean(df_filtered, "ROI (%)")
    ticket = _safe_mean(df_filtered, "Ticket Médio")

    # ================================
    # 2. Definição dos benchmarks-alvo
    # ================================

    # você pode no futuro buscar isso de 'benchmarks' (dict), se quiser parametrizar
    bench = {
        "TC Usuários (%)":  {"min": 8.0,   "max": 15.0,  "maior_melhor": True,  "label": "8-15%"},
        "TC Leads (%)":     {"min": 4.5,   "max": 6.0,   "maior_melhor": True,  "label": "4,5-6%"},
        "CAC":              {"min": 250.0, "max": 500.0, "maior_melhor": False, "label": "R$ 250-500"},
        "CAC:LTV":          {"min": 3.0,   "max": None,  "maior_melhor": True,  "label": "≥3:1 (ideal 4-7:1)"},
        "ROI (%)":          {"min": 300.0, "max": 500.0, "maior_melhor": True,  "label": "300-500%"},
        "Ticket Médio":     {"min": 120.0, "max": 200.0, "maior_melhor": True,  "label": "R$ 120-200"},
    }

    # status vs benchmark
    status_tc_users = _status_vs_interval(tc_usuarios,
                                          bench["TC Usuários (%)"]["min"],
                                          bench["TC Usuários (%)"]["max"],
                                          bench["TC Usuários (%)"]["maior_melhor"])
    status_tc_leads = _status_vs_interval(tc_leads,
                                          bench["TC Leads (%)"]["min"],
                                          bench["TC Leads (%)"]["max"],
                                          bench["TC Leads (%)"]["maior_melhor"])
    status_cac = _status_vs_interval(cac,
                                     bench["CAC"]["min"],
                                     bench["CAC"]["max"],
                                     bench["CAC"]["maior_melhor"])
    status_caclvt = _status_vs_interval(caclvt,
                                        bench["CAC:LTV"]["min"],
                                        bench["CAC:LTV"]["max"],
                                        bench["CAC:LTV"]["maior_melhor"])
    status_roi = _status_vs_interval(roi,
                                     bench["ROI (%)"]["min"],
                                     bench["ROI (%)"]["max"],
                                     bench["ROI (%)"]["maior_melhor"])
    status_ticket = _status_vs_interval(ticket,
                                        bench["Ticket Médio"]["min"],
                                        bench["Ticket Médio"]["max"],
                                        bench["Ticket Médio"]["maior_melhor"])

    benchmark_data = pd.DataFrame({
        'Métrica': [
            'TC Usuários → Leads',
            'TC Leads → Vendas',
            'CAC',
            'CAC:LTV',
            'ROI',
            'Ticket Médio'
        ],
        'Sua Média': [
            f"{tc_usuarios:.2f}%" if not np.isnan(tc_usuarios) else "—",
            f"{tc_leads:.2f}%" if not np.isnan(tc_leads) else "—",
            f"R$ {cac:,.2f}" if not np.isnan(cac) else "—",
            f"{caclvt:.1f}:1" if not np.isnan(caclvt) else "—",
            f"{roi:,.1f}%" if not np.isnan(roi) else "—",
            f"R$ {ticket:,.2f}" if not np.isnan(ticket) else "—",
        ],
        'Benchmark': [
            bench["TC Usuários (%)"]["label"],
            bench["TC Leads (%)"]["label"],
            bench["CAC"]["label"],
            bench["CAC:LTV"]["label"],
            bench["ROI (%)"]["label"],
            bench["Ticket Médio"]["label"],
        ],
        'Status': [
            status_tc_users,
            status_tc_leads,
            status_cac,
            status_caclvt,
            status_roi,
            status_ticket,
        ]
    })

    st.markdown("#### Visão Geral vs Benchmarks")
    st.dataframe(benchmark_data, use_container_width=True, hide_index=True)

    # ==============================
    # 3. Série temporal vs benchmarks
    # ==============================
    st.markdown("---")
    st.markdown("#### Evolução no Tempo vs Benchmarks")

    # tentar descobrir a coluna de data/mês
    col_data = "Mês" if "Mês" in df_filtered.columns else ("Data" if "Data" in df_filtered.columns else None)
    if col_data is not None:
        df_ts = df_filtered.copy()
        df_ts[col_data] = pd.to_datetime(df_ts[col_data], errors="coerce")
        df_ts = df_ts.dropna(subset=[col_data])
        df_ts = df_ts.sort_values(col_data)
        df_ts["mes_ano_str"] = df_ts[col_data].dt.strftime("%Y-%m")

        col_opts = {
            "TC Usuários (%)": "TC Usuários (%)",
            "TC Leads (%)": "TC Leads (%)",
            "CAC": "CAC",
            "ROI (%)": "ROI (%)",
            "Ticket Médio": "Ticket Médio",
        }
        metric_choice = st.selectbox(
            "Escolha uma métrica para comparar no tempo:",
            list(col_opts.keys()),
            index=0
        )
        metric_col = col_opts[metric_choice]

        if metric_col in df_ts.columns:
            fig_ts = px.line(
                df_ts,
                x="mes_ano_str",
                y=metric_col,
                markers=True,
                labels={"mes_ano_str": "Mês", metric_col: metric_choice},
                title=f"Evolução de {metric_choice} vs Benchmark"
            )

            # adicionar faixas de benchmark como linhas horizontais, se aplicável
            info_bench = bench.get(metric_col) or bench.get(metric_choice)
            if info_bench is not None:
                ymin = info_bench["min"]
                ymax = info_bench["max"]
                if ymin is not None:
                    fig_ts.add_hline(
                        y=ymin,
                        line_dash="dot",
                        line_color="orange",
                        annotation_text="Mín. benchmark",
                        annotation_position="bottom left"
                    )
                if ymax is not None:
                    fig_ts.add_hline(
                        y=ymax,
                        line_dash="dot",
                        line_color="green",
                        annotation_text="Máx. benchmark",
                        annotation_position="top left"
                    )

            st.plotly_chart(fig_ts, use_container_width=True)
        else:
            st.info(f"A coluna '{metric_col}' não está disponível no DataFrame.")
    else:
        st.info("Não foi possível identificar a coluna de data/mês para análise temporal.")

    # ===================================
    # 4. Análise preditiva com scikit-learn
    # ===================================
    st.markdown("---")
    st.markdown("#### Análise Preditiva (scikit-learn)")

    st.write(
        "Aqui usamos um modelo de regressão (RandomForest) para estimar o **ROI (%)** "
        "com base em variáveis como CAC, taxas de conversão e ticket médio. "
        "Isso NÃO substitui benchmarks, mas ajuda a entender para onde você está indo "
        "se mantiver o comportamento atual."
    )

    # Features e target para predição de ROI
    feature_cols = []
    for c in ["CAC", "TC Usuários (%)", "TC Leads (%)", "Ticket Médio"]:
        if c in df_filtered.columns:
            feature_cols.append(c)

    target_col = "ROI (%)" if "ROI (%)" in df_filtered.columns else None

    if not feature_cols or target_col is None:
        st.info(
            "Não há colunas suficientes para treinar um modelo preditivo de ROI. "
            "Certifique-se de ter CAC, TC Usuários (%), TC Leads (%) e ROI (%)."
        )
        return

    df_ml = df_filtered.copy()
    df_ml = df_ml[feature_cols + [target_col]].dropna()

    if df_ml.shape[0] < 20:
        st.info("Histórico insuficiente (menos de 20 linhas) para treinar um modelo robusto.")
        return

    X = df_ml[feature_cols]
    y = df_ml[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=6,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    col_m1, col_m2 = st.columns(2)
    col_m1.metric("R² (explicação do modelo)", f"{r2:.2f}")
    col_m2.metric("Erro Absoluto Médio (p.p. de ROI)", f"{mae:.1f}")

    st.write(
        "Valores típicos: R² próximo de 1 indica que o modelo explica bem a variação do ROI. "
        "Um MAE baixo (por ex. < 30 p.p.) indica boa precisão prática."
    )

    # Importância das variáveis
    importances = pd.DataFrame({
        "feature": feature_cols,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    st.markdown("##### Variáveis que mais explicam o ROI (%)")
    fig_imp = px.bar(
        importances,
        x="feature",
        y="importance",
        labels={"feature": "Variável", "importance": "Importância relativa"},
        title="Importância das variáveis no modelo de ROI (%)",
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    # =======================================
    # 5. Simulador preditivo (cenário futuro)
    # =======================================
    st.markdown("##### Simulador: prever ROI (%) em um cenário futuro")

    with st.form("form_predicao_roi"):
        cols_inputs = st.columns(len(feature_cols))
        valores_input = {}
        for i, feat in enumerate(feature_cols):
            col_i = cols_inputs[i]
            media_feat = float(df_ml[feat].mean())
            min_feat = float(df_ml[feat].min())
            max_feat = float(df_ml[feat].max())

            if "TC " in feat or "ROI" in feat:
                step = 0.1
            else:
                step = (max_feat - min_feat) / 100 if max_feat != min_feat else 1.0

            valores_input[feat] = col_i.number_input(
                label=feat,
                value=round(media_feat, 2),
                min_value=float(min_feat),
                max_value=float(max_feat * 1.5 if max_feat > 0 else max_feat + 1),
                step=step,
            )

        submitted = st.form_submit_button("Prever ROI (%)")

    if submitted:
        X_new = pd.DataFrame([valores_input])
        roi_prev = float(model.predict(X_new)[0])

        st.success(f"ROI previsto para o cenário simulado: **{roi_prev:,.1f}%**")

        # Comparação com benchmark de ROI
        info_bench_roi = bench["ROI (%)"]
        status_previsto = _status_vs_interval(
            roi_prev,
            info_bench_roi["min"],
            info_bench_roi["max"],
            info_bench_roi["maior_melhor"],
        )
        st.write(f"Status em relação ao benchmark de ROI: {status_previsto}")