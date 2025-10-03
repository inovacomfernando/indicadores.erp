"""
Módulo de utilitários e funções auxiliares
"""

from .calculations import (
    calcular_comissao,
    calcular_cac_ltv_ratio,
    calcular_roi,
    avaliar_metrica
)

from .charts import (
    criar_grafico_linha,
    criar_grafico_barras,
    criar_grafico_funil,
    criar_grafico_comparativo,
    criar_grafico_projecao
)

from .forecast import (
    prever_cenarios,
    calcular_metricas_qualidade
)

__all__ = [
    'calcular_comissao',
    'calcular_cac_ltv_ratio',
    'calcular_roi',
    'avaliar_metrica',
    'criar_grafico_linha',
    'criar_grafico_barras',
    'criar_grafico_funil',
    'criar_grafico_comparativo',
    'criar_grafico_projecao',
    'prever_cenarios',
    'calcular_metricas_qualidade'
]