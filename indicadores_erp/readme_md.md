# 📊 Dashboard de Marketing - SaaS ERP

Dashboard interativo para análise de KPIs de marketing digital com benchmarks do setor de SaaS ERP.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🚀 Funcionalidades

- **Análise de KPIs**: Visualização completa de métricas de marketing (CAC, LTV, ROI, TC)
- **Benchmarks do Setor**: Comparação com padrões da indústria de SaaS ERP
- **Gráficos Interativos**: Visualizações dinâmicas com Plotly
- **Análise Temporal**: Acompanhamento da evolução das métricas ao longo do tempo
- **Recomendações Estratégicas**: Plano de ação baseado em dados

## 📈 Métricas Acompanhadas

- **Tráfego**: Sessões, Primeira Visita
- **Conversão**: Taxa de Conversão (Usuários → Leads → Vendas)
- **Financeiro**: CAC, LTV, ROI, Receita Web, Ticket Médio
- **Investimento**: Custos Meta Ads e Google Ads

## 🛠️ Tecnologias

- **Streamlit**: Framework para criação de aplicações web
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualizações interativas

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/dashboard-marketing-saas.git
cd dashboard-marketing-saas
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🚀 Como Executar

Execute o comando abaixo no terminal:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador padrão em `http://localhost:8501`

## 📊 Estrutura de Dados

Os dados são carregados diretamente no código e incluem:
- Período: Maio a Setembro 2025
- Métricas mensais de marketing e vendas
- Benchmarks da indústria de SaaS ERP

## 🎯 Benchmarks Utilizados

| Métrica | Benchmark |
|---------|-----------|
| TC Usuários → Leads | 8-15% |
| TC Leads → Vendas | 4.5-6% |
| CAC | R$ 250-500 |
| Relação CAC:LTV | 3-5:1 |
| ROI | 300-500% |
| Ticket Médio | R$ 120-200 |

## 📁 Estrutura do Projeto

```
dashboard-marketing-saas/
│
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências do projeto
├── README.md          # Documentação
├── .gitignore         # Arquivos ignorados pelo Git
└── LICENSE            # Licença do projeto
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

Desenvolvido para análise estratégica de marketing

## 📞 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Nota**: Este dashboard foi desenvolvido para análise de dados de marketing de empresas SaaS ERP. Os benchmarks são baseados em estudos de mercado e podem variar conforme o segmento específico.
