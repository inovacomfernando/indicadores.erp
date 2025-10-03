"""
Funções para criação de gráficos Plotly
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def criar_grafico_linha(df, x_col, y_cols, names, colors, title="", height=400):
    """
    Cria um gráfico de linha
    
    Args:
        df: DataFrame com os dados
        x_col: Nome da coluna X
        y_cols: Lista de nomes das colunas Y
        names: Lista de nomes para as linhas
        colors: Lista de cores
        title: Título do gráfico
        height: Altura do gráfico
    
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    for y_col, name, color in zip(y_cols, names, colors):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=name,
            line=dict(color=color, width=3),
            marker=dict(size=10)
        ))
    
    fig.update_layout(
        title=title,
        height=height,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def criar_grafico_barras(df, x_col, y_cols, names, colors, title="", height=400, barmode='group'):
    """
    Cria um gráfico de barras
    
    Args:
        df: DataFrame com os dados
        x_col: Nome da coluna X
        y_cols: Lista de nomes das colunas Y
        names: Lista de nomes para as barras
        colors: Lista de cores
        title: Título do gráfico
        height: Altura do gráfico
        barmode: Modo de exibição ('group', 'stack', etc)
    
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    for y_col, name, color in zip(y_cols, names, colors):
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[y_col],
            name=name,
            marker_color=color
        ))
    
    fig.update_layout(
        title=title,
        height=height,
        barmode=barmode
    )
    
    return fig


def criar_grafico_barras_com_texto(df, x_col, y_col, color, title="", height=400, formato="R$ {:.0f}"):
    """
    Cria um gráfico de barras com valores exibidos
    
    Args:
        df: DataFrame com os dados
        x_col: Nome da coluna X
        y_col: Nome da coluna Y
        color: Cor das barras
        title: Título do gráfico
        height: Altura do gráfico
        formato: Formato do texto (string format)
    
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df[x_col],
        y=df[y_col],
        marker_color=color,
        text=df[y_col].apply(lambda x: formato.format(x)),
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        height=height,
        showlegend=False
    )
    
    return fig


def criar_grafico_funil(labels, values, colors=None, title="", height=400):
    """
    Cria um gráfico de funil
    
    Args:
        labels: Lista de labels
        values: Lista de valores
        colors: Lista de cores (opcional)
        title: Título do gráfico
        height: Altura do gráfico
    
    Returns:
        Figura Plotly
    """
    if colors is None:
        colors = ['#073763', '#3b82f6', '#8b5cf6', '#10b981']
    
    fig = go.Figure(go.Funnel(
        y=labels,
        x=values,
        textinfo="value+percent initial",
        marker=dict(color=colors)
    ))
    
    fig.update_layout(
        title=title,
        height=height
    )
    
    return fig


def criar_grafico_area(df, x_col, y_col, color, title="", height=400, benchmark_line=None):
    """
    Cria um gráfico de área com fill
    
    Args:
        df: DataFrame com os dados
        x_col: Nome da coluna X
        y_col: Nome da coluna Y
        color: Cor da linha
        title: Título do gráfico
        height: Altura do gráfico
        benchmark_line: Dict com configuração de linha de benchmark (opcional)
    
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color=color, width=3),
        marker=dict(size=12)
    ))
    
    if benchmark_line:
        fig.add_hline(
            y=benchmark_line['value'],
            line_dash="dash",
            line_color=benchmark_line.get('color', 'green'),
            annotation_text=benchmark_line.get('text', 'Benchmark')
        )
    
    fig.update_layout(
        title=title,
        height=height
    )
    
    return fig


def criar_grafico_comparativo(categorias, valores, colors, texts, title="", height=400):
    """
    Cria um gráfico de barras comparativo simples
    
    Args:
        categorias: Lista de categorias
        valores: Lista de valores
        colors: Lista de cores
        texts: Lista de textos para exibir
        title: Título do gráfico
        height: Altura do gráfico
    
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categorias,
        y=valores,
        marker_color=colors,
        text=texts,
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        height=height,
        showlegend=False
    )
    
    return fig


def criar_grafico_projecao(meses_historico, valores_historico, meses_previsao, 
                          valores_previsao, valores_otimista, valores_conservador,
                          title="", height=400):
    """
    Cria um gráfico de projeção com intervalos de confiança
    
    Args:
        meses_historico: Lista de meses históricos
        valores_historico: Valores históricos
        meses_previsao: Lista de meses de previsão
        valores_previsao: Valores previstos
        valores_otimista: Valores do cenário otimista
        valores_conservador: Valores do cenário conservador
        title: Título do gráfico
        height: Altura do gráfico
    
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    # Dados históricos
    fig.add_trace(go.Scatter(
        x=meses_historico,
        y=valores_historico,
        name="Histórico",
        mode="lines+markers",
        line=dict(color='#3b82f6', width=3)
    ))
    
    # Previsão
    fig.add_trace(go.Scatter(
        x=meses_previsao,
        y=valores_previsao,
        name="Previsão",
        mode="lines+markers",
        line=dict(color='#10b981', width=3, dash='dot')
    ))
    
    # Intervalos de confiança
    fig.add_trace(go.Scatter(
        x=meses_previsao,
        y=valores_otimista,
        name="IC Superior (95%)",
        mode="lines",
        line=dict(color='rgba(16, 185, 129, 0.3)', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=meses_previsao,
        y=valores_conservador,
        name="IC Inferior (95%)",
        mode="lines",
        line=dict(color='rgba(239, 68, 68, 0.3)', dash='dash'),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title=title,
        height=height
    )
    
    return fig


def criar_grafico_subplots(titulos, dados_list, height=600):
    """
    Cria um gráfico com múltiplos subplots
    
    Args:
        titulos: Lista de títulos dos subplots
        dados_list: Lista de dicts com dados para cada subplot
        height: Altura do gráfico
    
    Returns:
        Figura Plotly
    """
    num_plots = len(titulos)
    
    fig = make_subplots(
        rows=num_plots, cols=1,
        subplot_titles=titulos,
        vertical_spacing=0.15
    )
    
    for i, dados in enumerate(dados_list, 1):
        fig.add_trace(
            go.Bar(
                x=dados['x'],
                y=dados['y'],
                name=dados.get('name', f'Subplot {i}'),
                marker_color=dados.get('color', '#3b82f6'),
                text=dados.get('text', None),
                textposition='outside'
            ),
            row=i, col=1
        )
    
    fig.update_layout(
        height=height,
        showlegend=False
    )
    
    return fig


def criar_grafico_linha_com_benchmark(df, x_col, y_col, color, benchmark_min, 
                                      benchmark_max, title="", height=400):
    """
    Cria um gráfico de linha com área de benchmark
    
    Args:
        df: DataFrame com os dados
        x_col: Nome da coluna X
        y_col: Nome da coluna Y
        color: Cor da linha
        benchmark_min: Valor mínimo do benchmark
        benchmark_max: Valor máximo do benchmark
        title: Título do gráfico
        height: Altura do gráfico
    
    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=10)
    ))
    
    fig.add_hrect(
        y0=benchmark_min,
        y1=benchmark_max,
        fillcolor="green",
        opacity=0.1,
        annotation_text="Benchmark",
        annotation_position="top left"
    )
    
    fig.update_layout(
        title=title,
        height=height
    )
    
    return fig