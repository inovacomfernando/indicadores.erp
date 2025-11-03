"""
Configurações centralizadas do projeto
"""

BENCHMARKS = {
    'TC Usuários (%)': {'min': 8, 'max': 15, 'ideal': 10.5},
    'TC Leads (%)': {'min': 4.5, 'max': 6, 'ideal': 5.25},
    'CAC': {'min': 250, 'max': 500, 'ideal': 350},
    'CAC:LTV': {'min': 3, 'max': 7, 'ideal': 4, 'critico': 3},
    'ROI (%)': {'min': 300, 'max': 500, 'ideal': 400},
    'Ticket Médio': {'min': 120, 'max': 200, 'ideal': 150}
}

PLANOS = {
    'MEI': 84.90,
    'Simples Nacional': 154.90,
    'Lucro Real/Presumido': 199.90
}

EXTENSOES = {
    'Controle de Estoque': 15.99,
    'Controle Financeiro': 15.99,
    'Emissão de Boleto Bancário': 15.99,
    'Comissão de Vendedores': 15.99,
    'Nota Fiscal de Serviço': 39.90,
    'PDV': 39.90,
    'Força de Vendas': 39.90
}

CUSTOS_LEAD = {
    'min': 25,
    'max': 50,
    'medio': 37.5
}

PAGE_CONFIG = {
    'page_title': "Dashboard Marketing - SaaS ERP",
    'page_icon': "📊",
    'layout': "wide",
    'initial_sidebar_state': "expanded"

}
