"""
Funções para previsão e análise estatística
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import stats
import sklearn.metrics as metrics


def prever_cenarios(df, coluna, num_previsoes=3):
    """
    Realiza previsão com intervalos de confiança
    
    Args:
        df: DataFrame com os dados históricos (apenas dados apurados)
        coluna: Nome da coluna a prever
        num_previsoes: Número de períodos para prever
    
    Returns:
        Dict com previsões e métricas (como pandas Series)
    """
    try:
        # Filtra apenas valores válidos (não zeros e não nulos)
        df_valido = df[df[coluna] > 0].copy()
        
        if len(df_valido) < 3:
            print(f"Dados insuficientes para previsão de {coluna}")
            return None
        
        # Preparar dados
        n = len(df_valido)
        X = np.arange(n).reshape(-1, 1)
        y = df_valido[coluna].values
        
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
        
        # Garantir valores não negativos
        conservador = np.maximum(conservador, 0)
        
        # Métricas de qualidade
        metricas_calc = calcular_metricas_qualidade(y, y_pred)
        
        # Teste de tendência (Mann-Kendall)
        tau, p_valor = stats.kendalltau(range(len(y)), y)
        metricas_calc['Tendência (tau)'] = tau
        metricas_calc['P-valor tendência'] = p_valor
        
        # Retorna como pandas Series para facilitar manipulação
        return {
            'previsao': pd.Series(previsao_base),
            'otimista': pd.Series(otimista),
            'conservador': pd.Series(conservador),
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
    try:
        # R² (coeficiente de determinação)
        r2 = metrics.r2_score(y_real, y_pred)
        
        # RMSE (Root Mean Squared Error)
        rmse = np.sqrt(metrics.mean_squared_error(y_real, y_pred))
        
        # MAPE (Mean Absolute Percentage Error)
        # Evita divisão por zero
        mask = y_real != 0
        if np.sum(mask) > 0:
            mape = np.mean(np.abs((y_real[mask] - y_pred[mask]) / y_real[mask])) * 100
        else:
            mape = 0
        
        # MAE (Mean Absolute Error)
        mae = metrics.mean_absolute_error(y_real, y_pred)
        
        return {
            'R²': r2,
            'RMSE': rmse,
            'MAPE': mape,
            'MAE': mae
        }
    except Exception as e:
        print(f"Erro ao calcular métricas: {str(e)}")
        return {
            'R²': 0,
            'RMSE': 0,
            'MAPE': 0,
            'MAE': 0
        }


def avaliar_qualidade_previsao(r2, mape):
    """
    Avalia a qualidade da previsão baseado em R² e MAPE
    
    Args:
        r2: Coeficiente de determinação
        mape: Mean Absolute Percentage Error
    
    Returns:
        Dict com avaliações
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
            direcao = "Crescente"
            emoji = "📈"
            interpretacao = "Tendência significativa de crescimento"
        else:
            direcao = "Decrescente"
            emoji = "📉"
            interpretacao = "Tendência significativa de declínio"
    else:
        direcao = "Estável"
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
    try:
        valores_array = np.array(valores)
        valores_validos = valores_array[valores_array > 0]
        
        if len(valores_validos) < 2:
            return (0, 0)
        
        media = np.mean(valores_validos)
        erro_padrao = stats.sem(valores_validos)
        intervalo = stats.t.interval(
            confianca, 
            len(valores_validos)-1, 
            loc=media, 
            scale=erro_padrao
        )
        
        return intervalo
    except Exception as e:
        print(f"Erro ao calcular intervalo de confiança: {str(e)}")
        return (0, 0)


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
    try:
        valores_array = np.array(valores)
        valores_validos = valores_array[valores_array > 0]
        
        if len(valores_validos) < 4:
            return {
                'indices': [],
                'valores': [],
                'quantidade': 0
            }
        
        if metodo == 'iqr':
            q1 = np.percentile(valores_validos, 25)
            q3 = np.percentile(valores_validos, 75)
            iqr = q3 - q1
            
            limite_inferior = q1 - (threshold * iqr)
            limite_superior = q3 + (threshold * iqr)
            
            outliers_mask = (valores_array < limite_inferior) | (valores_array > limite_superior)
        
        elif metodo == 'zscore':
            z_scores = np.abs(stats.zscore(valores_validos))
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
    except Exception as e:
        print(f"Erro ao detectar outliers: {str(e)}")
        return {
            'indices': [],
            'valores': [],
            'quantidade': 0
        }


def calcular_crescimento(valores):
    """
    Calcula taxa de crescimento entre períodos
    
    Args:
        valores: Array de valores
    
    Returns:
        Dict com análise de crescimento
    """
    try:
        valores_array = np.array(valores)
        valores_validos = valores_array[valores_array > 0]
        
        if len(valores_validos) < 2:
            return {
                'absoluto': [],
                'percentual': [],
                'medio_pct': 0,
                'total_pct': 0,
                'primeiro_valor': 0,
                'ultimo_valor': 0
            }
        
        # Crescimento absoluto
        crescimento_abs = np.diff(valores_validos)
        
        # Crescimento percentual
        crescimento_pct = (crescimento_abs / valores_validos[:-1]) * 100
        
        # Estatísticas
        crescimento_medio = np.mean(crescimento_pct)
        crescimento_total = ((valores_validos[-1] - valores_validos[0]) / valores_validos[0]) * 100
        
        return {
            'absoluto': crescimento_abs.tolist(),
            'percentual': crescimento_pct.tolist(),
            'medio_pct': crescimento_medio,
            'total_pct': crescimento_total,
            'primeiro_valor': valores_validos[0],
            'ultimo_valor': valores_validos[-1]
        }
    except Exception as e:
        print(f"Erro ao calcular crescimento: {str(e)}")
        return {
            'absoluto': [],
            'percentual': [],
            'medio_pct': 0,
            'total_pct': 0,
            'primeiro_valor': 0,
            'ultimo_valor': 0
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
    try:
        valores_array = np.array(valores)
        n = len(valores_array)
        
        if n < janela:
            return valores
        
        suavizados = np.zeros(n)
        
        for i in range(n):
            inicio = max(0, i - janela//2)
            fim = min(n, i + janela//2 + 1)
            
            janela_valores = valores_array[inicio:fim]
            janela_validos = janela_valores[janela_valores > 0]
            
            if len(janela_validos) > 0:
                if metodo == 'media':
                    suavizados[i] = np.mean(janela_validos)
                elif metodo == 'mediana':
                    suavizados[i] = np.median(janela_validos)
                else:
                    suavizados[i] = valores_array[i]
            else:
                suavizados[i] = valores_array[i]
        
        return suavizados.tolist()
    except Exception as e:
        print(f"Erro ao suavizar série: {str(e)}")
        return valores


def validar_dados_previsao(df, coluna):
    """
    Valida se os dados são adequados para previsão
    
    Args:
        df: DataFrame com os dados
        coluna: Nome da coluna a validar
    
    Returns:
        Dict com status de validação
    """
    try:
        valores_validos = df[df[coluna] > 0][coluna]
        
        status = {
            'valido': False,
            'quantidade_pontos': len(valores_validos),
            'minimo_necessario': 3,
            'tem_variacao': False,
            'mensagem': ''
        }
        
        if len(valores_validos) < 3:
            status['mensagem'] = f"Dados insuficientes: {len(valores_validos)} pontos (mínimo 3)"
            return status
        
        # Verifica se há variação nos dados
        if np.std(valores_validos) > 0:
            status['tem_variacao'] = True
            status['valido'] = True
            status['mensagem'] = "Dados válidos para previsão"
        else:
            status['mensagem'] = "Dados sem variação (valores constantes)"
        
        return status
    except Exception as e:
        return {
            'valido': False,
            'quantidade_pontos': 0,
            'minimo_necessario': 3,
            'tem_variacao': False,
            'mensagem': f"Erro na validação: {str(e)}"
        }
