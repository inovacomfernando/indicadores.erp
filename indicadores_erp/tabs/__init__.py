"""
Módulo com todas as tabs do dashboard
"""

from .tab_evolucao import render_tab_evolucao
from .tab_financeiro import render_tab_financeiro
from .tab_conversao import render_tab_conversao
from .tab_benchmarks import render_tab_benchmarks
from .tab_recomendacoes import render_tab_recomendacoes
from .tab_forecast import render_tab_forecast
from .tab_contador import render_tab_contador

__all__ = [
    'render_tab_evolucao',
    'render_tab_financeiro',
    'render_tab_conversao',
    'render_tab_benchmarks',
    'render_tab_recomendacoes',
    'render_tab_forecast',
    'render_tab_contador'
]