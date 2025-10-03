"""
Módulo de configuração do Dashboard Marketing SaaS ERP
"""

from .settings import (
    BENCHMARKS,
    PLANOS,
    EXTENSOES,
    CUSTOS_LEAD,
    PAGE_CONFIG
)

from .styles import get_custom_css

__all__ = [
    'BENCHMARKS',
    'PLANOS',
    'EXTENSOES',
    'CUSTOS_LEAD',
    'PAGE_CONFIG',
    'get_custom_css'
]