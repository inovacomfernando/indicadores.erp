"""
Funções de cálculo reutilizáveis
"""

def calcular_comissao(valor_base, percentual):
    """Calcula comissão sobre um valor base"""
    return valor_base * percentual

def calcular_cac_ltv_ratio(ltv, cac):
    """Calcula a relação CAC:LTV"""
    if cac == 0:
        return 0
    return ltv / cac

def calcular_roi(receita, investimento):
    """Calcula ROI em percentual"""
    if investimento == 0:
        return 0
    return ((receita - investimento) / investimento) * 100

def avaliar_metrica(valor, benchmark):
    """Avalia se uma métrica está dentro do benchmark"""
    if valor < benchmark['min']:
        return 'baixo', '🔴'
    elif valor > benchmark['max']:
        return 'alto', '🔴'
    elif benchmark['min'] <= valor <= benchmark['max']:
        return 'ideal', '🟢'
    return 'fora_range', '⚪'