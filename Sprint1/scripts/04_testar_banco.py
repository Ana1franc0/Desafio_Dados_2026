import sqlite3
import pandas as pd
import os

print("TESTANDO O BANCO DE DADOS")

# Verificando se o banco existe
if not os.path.exists('banco/ecommerce.db'):
    print("ERRO: Banco de dados não encontrado!")
    print("Execute primeiro o script 03_carregar_banco.py")
    exit()

# conectar ao banco
conexao = sqlite3.connect('banco/ecommerce.db')

print("\nTESTE 1: Contar registros")
query1 = "SELECT COUNT() as total FROM vendas"
total = pd.read_sql(query1, conexao)
print(f"Total de registros no banco: {total['total'][0]}")

print("\nTESTE 2: Primeiros 5 registros")
query2 = "SELECT id_pedido, data_pedido, nome_cliente, preco_total FROM vendas LIMIT 5"
primeiros = pd.read_sql(query2, conexao)
print(primeiros)

print("\nTESTE 3: Estatísticas básicas")
query3 = """
SELECT
    COUNT(DISTINCT id_cliente) as total_clientes,
    COUNT(DISTINCT id_produto) as total_produtos,
    COUNT(DISTINCT categoria) as total_categorias,
    SUM(preco_total) as valor_total,
    AVG(preco_total) as valor_medio_pedido,
    MIN(preco_total) as menor_pedido,
    MAX(preco_total) as maior_pedido
FROM vendas
"""

statisticas = pd.read_sql(query3, conexao)
print(f"Clientes únicos: {statisticas['total_clientes'][0]}")
print(f"Produtos únicos: {statisticas['total_produtos'][0]}")
print(f"Categorias: {statisticas['total_categorias'][0]}")
print(f"Valor total: R$ {statisticas['valor_total'][0]:,.2f}")
print(f"Valor médio gasto por pedido: R$ {statisticas['valor_medio_pedido'][0]:,.2f}")
print(f"Menor pedido: R$ {statisticas['menor_pedido'][0]:,.2f}")
print(f"Maior pedido: R$ {statisticas['maior_pedido'][0]:,.2f}")

print("\nTESTE 4: Vendas por categoria")
query4 = """
SELECT
    categoria,
    COUNT(*) as quantidade,
    SUM(preco_total) as valor_total,
    AVG(preco_total) as alor_medio_pedido
FROM vendas
GROUP BY categoria
ORDER BY valor_total DESC
"""

categorias = pd.read_sql(query4, conexao)
print(categorias)

print("\nTESTE 5: Vendas por mês")
query5 = """
SELECT
    ano,
    mes,
    COUNT(*) as quantidade,
    SUM(preco_total) as valor_total
FROM vendas
GROUP BY ano, mes
ORDER BY ano, mes 
"""
meses = pd.read_sql(query5, conexao)
print(meses)

print("\nTESTE 6: Verificar valores nulos (não pode haver)")
query6 = """
SELECT
    SUM(CASE WHEN id_pedido IS NULL THEN 1 ELSE 0 END) as nulos_id_pedido,
    SUM(CASE WHEN nome_cliente = 'cliente não encontrado' IS NULL THEN 1 ELSE 0 END) as clientes_padrao,
    SUM(CASE WHEN preco_total IS NULL THEN 1 ELSE 0 END) as nulos_preco
FROM vendas
"""
nulos = pd.read_sql(query6, conexao)
print(f"ID pedido nulos: {nulos['nulos_id_pedido'][0]}")
print(f"Clientes com nome padrão: {nulos['clientes_padrao'][0]}")
print(f"Preço nulo: {nulos['nulos_preco'][0]}")

conexao.close

print("TESTES CONCLUÍDOS COM SUCESSO!")