"""
Módulo de componentes reutilizáveis do dashboard
"""

from .header import render_header, render_sidebar
from .metrics import render_main_metrics
from .alerts import render_main_alerts

__all__ = [
    'render_header',
    'render_sidebar',
    'render_main_metrics',
    'render_main_alerts'
]