"""
Funções para previsão e análise estatística
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats
import sklearn.metrics as metrics


def prever_cenarios(df, coluna, num_previsoes=3):
    """
    Realiza previsão com intervalos de confiança
    
    Args:
        df: DataFrame com os dados históricos
        coluna: Nome da coluna a prever
        num_previsoes: Número de períodos para prever
    
    Returns:
        Dict com previsões e métricas
    """
    try:
        # Preparar dados
        n = len(df)
        X = np.arange(n).reshape(-1, 1)
        y = df[coluna].values
        
        # Treinar modelo
        modelo = LinearRegression()
        modelo.fit(X, y)
        
        # Previsão histórica
        y_pred = modelo.predict(X)
        
        # Previsão futura
        X_futuro = np.arange(n, n + num_previsoes).reshape(-1, 1)
        previsao_base = modelo.predict(X_futuro)
        
        # Calcular erro padrão
        residuos = y - y_pred
        erro_padrao = np.std(residuos)
        
        # Intervalo de confiança (95%)
        z_score = 1.96
        margem_erro = z_score * erro_padrao
        
        # Cenários
        otimista = previsao_base + margem_erro
        conservador = previsao_base - margem_erro
        
        # Métricas de qualidade
        metricas_calc = calcular_metricas_qualidade(y, y_pred)
        
        # Teste de tendência
        tau, p_valor = stats.kendalltau(range(len(y)), y)
        metricas_calc['Tendência (tau)'] = tau
        metricas_calc['P-valor tendência'] = p_valor
        
        return {
            'previsao': previsao_base,
            'otimista': otimista,
            'conservador': conservador,
            'metricas': metricas_calc,
            'modelo': modelo,
            'erro_padrao': erro_padrao
        }
    
    except Exception as e:
        print(f"Erro ao calcular previsões para {coluna}: {str(e)}")
        return None


def calcular_metricas_qualidade(y_real, y_pred):
    """
    Calcula métricas de qualidade da previsão
    
    Args:
        y_real: Valores reais
        y_pred: Valores preditos
    
    Returns:
        Dict com métricas
    """
    # R² (coeficiente de determinação)
    r2 = metrics.r2_score(y_real, y_pred)
    
    # RMSE (Root Mean Squared Error)
    rmse = np.sqrt(metrics.mean_squared_error(y_real, y_pred))
    
    # MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((y_real - y_pred) / y_real)) * 100
    
    # MAE (Mean Absolute Error)
    mae = metrics.mean_absolute_error(y_real, y_pred)
    
    return {
        'R²': r2,
        'RMSE': rmse,
        'MAPE': mape,
        'MAE': mae
    }


def avaliar_qualidade_previsao(r2, mape):
    """
    Avalia a qualidade da previsão baseado em R² e MAPE
    
    Args:
        r2: Coeficiente de determinação
        mape: Mean Absolute Percentage Error
    
    Returns:
        Tuple (status_r2, status_mape, status_geral)
    """
    # Avaliação R²
    if r2 > 0.8:
        status_r2 = "Excelente"
        emoji_r2 = "✅"
    elif r2 > 0.6:
        status_r2 = "Moderado"
        emoji_r2 = "⚠️"
    else:
        status_r2 = "Baixo"
        emoji_r2 = "❌"
    
    # Avaliação MAPE
    if mape < 10:
        status_mape = "Baixo"
        emoji_mape = "✅"
    elif mape < 20:
        status_mape = "Moderado"
        emoji_mape = "⚠️"
    else:
        status_mape = "Alto"
        emoji_mape = "❌"
    
    # Status geral
    if r2 > 0.8 and mape < 10:
        status_geral = "Confiável"
    elif r2 > 0.6 and mape < 20:
        status_geral = "Moderado"
    else:
        status_geral = "Baixa confiança"
    
    return {
        'r2': {'status': status_r2, 'emoji': emoji_r2},
        'mape': {'status': status_mape, 'emoji': emoji_mape},
        'geral': status_geral
    }


def interpretar_tendencia(tau, p_valor, threshold=0.05):
    """
    Interpreta o teste de tendência Mann-Kendall
    
    Args:
        tau: Estatística tau
        p_valor: P-valor do teste
        threshold: Limiar de significância
    
    Returns:
        Dict com interpretação
    """
    significante = p_valor < threshold
    
    if significante:
        if tau > 0:
            direcao = "crescente"
            emoji = "📈"
            interpretacao = "Tendência significativa de crescimento"
        else:
            direcao = "decrescente"
            emoji = "📉"
            interpretacao = "Tendência significativa de declínio"
    else:
        direcao = "sem tendência"
        emoji = "➖"
        interpretacao = "Não há tendência significativa"
    
    return {
        'direcao': direcao,
        'emoji': emoji,
        'interpretacao': interpretacao,
        'significante': significante
    }


def calcular_intervalo_confianca(valores, confianca=0.95):
    """
    Calcula intervalo de confiança para uma série de valores
    
    Args:
        valores: Array de valores
        confianca: Nível de confiança (padrão 95%)
    
    Returns:
        Tuple (limite_inferior, limite_superior)
    """
    media = np.mean(valores)
    erro_padrao = stats.sem(valores)
    intervalo = stats.t.interval(confianca, len(valores)-1, loc=media, scale=erro_padrao)
    
    return intervalo


def detectar_outliers(valores, metodo='iqr', threshold=1.5):
    """
    Detecta outliers em uma série de valores
    
    Args:
        valores: Array de valores
        metodo: Método de detecção ('iqr' ou 'zscore')
        threshold: Limiar para detecção
    
    Returns:
        Dict com índices e valores dos outliers
    """
    valores_array = np.array(valores)
    
    if metodo == 'iqr':
        q1 = np.percentile(valores_array, 25)
        q3 = np.percentile(valores_array, 75)
        iqr = q3 - q1
        
        limite_inferior = q1 - (threshold * iqr)
        limite_superior = q3 + (threshold * iqr)
        
        outliers_mask = (valores_array < limite_inferior) | (valores_array > limite_superior)
    
    elif metodo == 'zscore':
        z_scores = np.abs(stats.zscore(valores_array))
        outliers_mask = z_scores > threshold
    
    else:
        raise ValueError("Método deve ser 'iqr' ou 'zscore'")
    
    indices_outliers = np.where(outliers_mask)[0]
    valores_outliers = valores_array[outliers_mask]
    
    return {
        'indices': indices_outliers.tolist(),
        'valores': valores_outliers.tolist(),
        'quantidade': len(indices_outliers)
    }


def calcular_crescimento(valores):
    """
    Calcula taxa de crescimento entre períodos
    
    Args:
        valores: Array de valores
    
    Returns:
        Dict com análise de crescimento
    """
    valores_array = np.array(valores)
    
    # Crescimento absoluto
    crescimento_abs = np.diff(valores_array)
    
    # Crescimento percentual
    crescimento_pct = (crescimento_abs / valores_array[:-1]) * 100
    
    # Estatísticas
    crescimento_medio = np.mean(crescimento_pct)
    crescimento_total = ((valores_array[-1] - valores_array[0]) / valores_array[0]) * 100
    
    return {
        'absoluto': crescimento_abs.tolist(),
        'percentual': crescimento_pct.tolist(),
        'medio_pct': crescimento_medio,
        'total_pct': crescimento_total,
        'primeiro_valor': valores_array[0],
        'ultimo_valor': valores_array[-1]
    }


def suavizar_serie(valores, janela=3, metodo='media'):
    """
    Aplica suavização em uma série temporal
    
    Args:
        valores: Array de valores
        janela: Tamanho da janela de suavização
        metodo: Método de suavização ('media' ou 'mediana')
    
    Returns:
        Array com valores suavizados
    """
    valores_array = np.array(valores)
    n = len(valores_array)
    suavizados = np.zeros(n)
    
    for i in range(n):
        inicio = max(0, i - janela//2)
        fim = min(n, i + janela//2 + 1)
        
        if metodo == 'media':
            suavizados[i] = np.mean(valores_array[inicio:fim])
        elif metodo == 'mediana':
            suavizados[i] = np.median(valores_array[inicio:fim])
    
    return suavizados.tolist()