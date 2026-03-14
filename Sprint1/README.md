# Sprint 1 - Ingestão e ETL

## Descrição do projeto
Este projeto faz parte do desafio de dados do Projeto Desenvolve. A sprint 1 consiste na criação de um dataset simulado de e-commerce, limpeza dos dados e carregamento do banco SQLite.

## Tecnologias utilizadas
- **Python** 
- **Pandas** - Biblioteca para manipulação de dados
- **Numpy** - Biblioteca para operações numéricas
- **Faker** - Biblioteca para geração de dados falsos
- **SQLite3** - Banco de dados relacional
- **Git/Github** - Para o versionamento

## Estrutura
Sprint1/
├── dados/ # CSVs (bruto e limpo)
├── banco/ # Banco SQLite
├── scripts/ # Códigos Python
└── README.md

## Como executar

# 1. Criar ambiente
python -m venv venv
.\venv\Scripts\activate

# 2. Instalar o necessário
pip install pandas numpy faker

# 3. Executar em ordem
python scripts/01_gerar_dados.py
python scripts/02_limpeza_dados.py
python scripts/03_carregar_banco.py
python scripts/04_testar_banco.py