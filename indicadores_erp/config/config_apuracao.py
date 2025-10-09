"""
Configuração de Meses Apurados

IMPORTANTE: Este arquivo controla quais meses são considerados "apurados" 
para fins de forecast e análises estatísticas.

REGRA DE APURAÇÃO:
==================
Os dados de um mês são apurados no PRIMEIRO DIA ÚTIL do mês seguinte.

Exemplo:
- Dados de SET/25 → Apurados no primeiro dia útil de OUT/25
- Dados de OUT/25 → Apurados no primeiro dia útil de NOV/25
- Dados de NOV/25 → Apurados no primeiro dia útil de DEZ/25

COMO ATUALIZAR:
===============
Quando um novo mês for apurado:

1. Adicione o mês na lista MESES_APURADOS abaixo
2. Salve o arquivo
3. O dashboard atualizará automaticamente

Exemplo de atualização (quando OUT/25 for apurado):
MESES_APURADOS = [
    'Mai/25', 
    'Jun/25', 
    'Jul/25', 
    'Ago/25', 
    'Set/25',
    'Out/25'  # <- Adicionar aqui
]

"""

# ============================================================================
# LISTA DE MESES APURADOS - ATUALIZE AQUI APÓS CADA APURAÇÃO
# ============================================================================

MESES_APURADOS = [
    'Mai/25',
    'Jun/25', 
    'Jul/25',
    'Ago/25',
    'Set/25' # ← Último mês oficialmente apurado
    # Adicione novos meses apurados abaixo desta linha
    # Exemplo: 'Out/25' (após apuração em Nov/25)
]

# ============================================================================
# INFORMAÇÕES COMPLEMENTARES
# ============================================================================

# Data da última atualização (para referência)
ULTIMA_ATUALIZACAO = "Set/25"  # Último mês apurado

# Próximo mês esperado para apuração
PROXIMO_MES_APURACAO = "Out/25"  # Será apurado no primeiro dia útil de Nov/25

# Data estimada de apuração do próximo mês
DATA_ESTIMADA_APURACAO = "Primeiro dia útil de Nov/25"


def get_meses_apurados():
    """
    Retorna a lista de meses apurados
    
    Returns:
        list: Lista de meses oficialmente apurados
    """
    return MESES_APURADOS.copy()


def is_mes_apurado(mes):
    """
    Verifica se um mês está apurado
    
    Args:
        mes: String do mês (ex: 'Set/25')
    
    Returns:
        bool: True se o mês está apurado, False caso contrário
    """
    return mes in MESES_APURADOS


def get_ultimo_mes_apurado():
    """
    Retorna o último mês apurado
    
    Returns:
        str: String do último mês apurado
    """
    if MESES_APURADOS:
        return MESES_APURADOS[-1]
    return None


def get_info_apuracao():
    """
    Retorna informações sobre a apuração
    
    Returns:
        dict: Informações sobre apuração
    """
    return {
        'ultimo_mes': get_ultimo_mes_apurado(),
        'proximo_mes': PROXIMO_MES_APURACAO,
        'data_estimada': DATA_ESTIMADA_APURACAO,
        'total_meses': len(MESES_APURADOS),
        'meses': MESES_APURADOS
    }


# Validação automática
if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURAÇÃO DE APURAÇÃO")
    print("=" * 60)
    print(f"\nÚltimo mês apurado: {get_ultimo_mes_apurado()}")
    print(f"Total de meses apurados: {len(MESES_APURADOS)}")
    print(f"Próximo mês a apurar: {PROXIMO_MES_APURACAO}")
    print(f"Data estimada: {DATA_ESTIMADA_APURACAO}")
    print(f"\nMeses apurados:")
    for mes in MESES_APURADOS:
        print(f"  ✓ {mes}")
    print("\n" + "=" * 60)
