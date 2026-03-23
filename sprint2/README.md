# Sprint 2 - Análise Exploratória de Dados (EDA)

## Sobre a Sprint

Esta sprint tem como objetivo realizar uma análise exploratória completa dos dados de e-commerce, gerando insights sobre o comportamento dos clientes, identificando problemas e oportunidades de negócio.

**Objetivos:**
- Extrair estatísticas descritivas dos dados
- Identificar outliers e analisar correlações
- Segmentar clientes usando metodologia RFM
- Gerar insights para tomada de decisão


## Estrutura do Projeto
sprint_2/
│
├── dados/
│ └── ecommerce.db # Banco de dados (feito Sprint 1)
│
├── scripts/
│ ├── 01_estatisticas_descritivas.py # Análise estatística básica
│ ├── 02_executar_consultas_sql.py # Consultas SQL avançadas
│ ├── 03_outliers.py # Análise de outliers
│ ├── 04_correlacao.py # Análise de correlação
│ └── 05_rfm.py # Segmentação RFM
│
├── resultados/
│ ├── estatisticas_descritivas.txt 
│ ├── analise_outliers.png 
| ├── analise_pagamento.csv
| ├── analise_status.csv
│ ├── analise_correlacao.png 
| ├── estatisticas_por_segmento.csv
| ├── matriz_correlacao.csv
│ ├── distribuicao_segmentos.png # Distribuição RFM
│ ├── analise_rfm_completa.csv # Classificação de clientes
│ ├── clientes_em_risco.csv # Clientes para recuperar
| ├── melhores_categorias.csv
| ├── outliers_lista.csv
│ ├── clientes_campeoes.csv 
│ ├── top_10_clientes.csv # Top clientes por gasto
│ ├── ranking_produtos.csv 
| ├── resumo_correlacao.txt
| ├── resumo_outliers.txt
| ├── resumo_rfm.txt
| ├── rfm_boxplot.png
│ └── crescimento_mensal.csv 
│
├── insights_sprint2.md
└── README.md # Este arquivo

## Tecnologias Utilizadas

Python 3.x - Linguagem principal 
Pandas - Manipulação e análise de dados 
SQLite3 - Conexão e consultas ao banco 
Matplotlib/Seaborn - Visualização de dados 
SQL - Consultas avançadas 


## Análises Realizadas

### 1. Estatísticas Descritivas
- Cálculo de métricas gerais (total pedidos, faturamento, ticket médio)
- Análise por status do pedido
- Distribuição de quantidades e valores

### 2. Análise de Outliers
- Identificação usando método IQR (Interquartile Range)
- Visualização via boxplots
- Análise de impacto financeiro

### 3. Análise de Correlação
- Matriz de correlação entre variáveis
- Heatmap para visualização
- Scatter plot para relação quantidade x valor

### 4. Segmentação RFM
- Cálculo de Recência, Frequência e Monetário por cliente
- Criação de scores (1 a 5)
- Classificação em 6 segmentos de clientes

### 5. Consultas SQL Avançadas
- Top clientes por gasto
- Ranking de produtos
- Crescimento mensal
- Análise por status e categoria

Ana Laura Dos Santos Franco - Março 2026