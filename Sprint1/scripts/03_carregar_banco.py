# Sempre fazer 'del banco\ecommerce.db' se quiser rodar esse código denovo, se  já tiver rodade uma vez, para não dar erro
import pandas as pd  # -> Manipulação da dataframes
import sqlite3  # -> Comunicação com o banco de dados
import os

print("=" * 50)
print("CARREGANDO DADOS PARA O BANCO DE DADOS")
print("=" * 50)

# Verificação para ver se o arquivo com dados limpos existe
if not os.path.exists('dados/ecom_data_limpo.csv'):
    print("ERRO: Arquivo 'dados/ecom_data_limpo.csv' não encontrado!")
    print("Execute  primeiro o script 02_limpeza_dados.py")
    exit()  # -> Encerra o script

# Carregar os dados limpos
print("Carregando dados limpos...")
df = pd.read_csv('dados/ecom_data_limpo.csv')
print(f"Dados carregados: {len(df)} linhas")

# Criar pasta para o banco de dados (se não existir)
if not os.path.exists('banco'):
    os.makedirs('banco')
    print("Pasta 'banco' criada com sucesso!")

# Conectar ao banco de dados SQLite (criar um arquivo .db -database)
print("\nConectando ao banco de dados...")
conexao = sqlite3.connect('banco/ecommerce.db')  # Se o arquivo ecommerce.db não existir, ele é criado automaticamente
cursor = conexao.cursor()  #
print("Conexão estabalecida!")

# Criar a tabela
print("\nCriando tabela 'vendas'...")
# PRIMARY KEY - identificador único (não vai haver duplicatas de id_pedido)
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
               id_pedido TEXT PRIMARY KEY,
               data_pedido TEXT,
               id_cliente TEXT,
               nome_cliente TEXT,
               email_cliente TEXT,
               cidade_cliente TEXT,
               estado_cliente TEXT,
               id_produto TEXT,
               nome_produto TEXT,
               categoria TEXT,
               quantidade INT,
               preco_unitario REAL,
               preco_total REAL,
               metodo_pagamento TEXT,
               status_pedido TEXT,
               ano INT,
               mes INT,
               dia_semana TEXT
)
''')
print("Tabela criada/verificada!")

# Inserir dados
print(f"\nInserindo {len(df)} registros no banco...")

# Em lotes para não travar
tamanho_lote = 500
total_linhas = len(df)

for i in range(0, total_linhas, tamanho_lote):  # vai de 0 ao total de linhas e pula de 500 a 500
    lote_atual = df.iloc[i:i+tamanho_lote]  # iloc[] -> index location, acessa linhas e colunas pelo indice delas. i(índice inicial) :(até) i+tamanho_lote(índice final-não incluso) ex: de 0 a 499
    lote_atual.to_sql('vendas', conexao, if_exists='append', index=False)  # inserir o dataframe na tabela sql, e se a tabela existir, não vai substituir os dados, só adicionar

    linhas_processadas = min(i+tamanho_lote, total_linhas)
    print(f"{linhas_processadas} linhas inseridas de {total_linhas} linhas...")

# Verificar se deu certo
print("\nVERIFICANDO BANCO DE DADOS:")

# Contar os registros
query = "SELECT COUNT(*) as total FROM vendas"  # Dando o nome da coluna que vai mostar a quantidade de registros de 'total'
resultado = pd.read_sql(query, conexao)
print(f"Total de registros no banco: {resultado['total'][0]}")  # pega o valor da primeira linha da coluna 'total'

# Mostrar os primeiros registros
query = "SELECT id_pedido, data_pedido, nome_cliente, preco_total FROM vendas LIMIT 5"
primeiros = pd.read_sql(query, conexao)
print("\nPrimeiros 5 registros:")
print(primeiros)

# Estatísticas
# COUNT(DISTINCT...): Conta os valores únicos que existem na coluna
query = """
SELECT
    COUNT(DISTINCT id_cliente) as total_clientes,
    COUNT(DISTINCT id_produto) as total_produtos,
    SUM(preco_total) as valor_total,
    AVG(preco_total) as valor_medio_pedido
FROM vendas
"""
statisticas = pd.read_sql(query, conexao)
print("\nEstatísticas do banco:")
print(f"Clientes únicos: {statisticas['total_clientes'][0]}")
print(f"Produtos únicos: {statisticas['total_produtos'][0]}")
print(f"Valor total: R$ {statisticas['valor_total'][0]:,.2f}")
print(f"Valor médio gasto por pedido: R$ {statisticas['valor_medio_pedido'][0]:,.2f}")  # valor total de pedidos / número de pedidos

# Fechar conexão
conexao.close()
print("\nBanco de dados fechado com sucesso!")
print("Arquivo do banco: banco/ecommerce.db")