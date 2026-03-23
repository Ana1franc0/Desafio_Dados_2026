import sqlite3
import pandas as pd
import os

# Criar pasta de resultados
os.makedirs('resultados', exist_ok=True)

# Conectar ao banco
conexao = sqlite3.connect('dados/ecommerce.db')

print("EXECUTANDO CONSULTAS SQL AVANÇADAS")

# CONSULTA 1: Top 10 clientes que mais gastaram
print("\n1. TOP 10 CLIENTES QUE MAIS GASTARAM")
print("-"*50)

query1 = """
SELECT 
    id_cliente,
    nome_cliente,
    COUNT(DISTINCT id_pedido) as total_pedidos,
    SUM(preco_total) as gasto_total,
    ROUND(AVG(preco_total), 2) as ticket_medio
FROM vendas
WHERE status_pedido = 'Entregue'
GROUP BY id_cliente, nome_cliente
ORDER BY gasto_total DESC
LIMIT 10
"""

df1 = pd.read_sql_query(query1, conexao)
print(df1.to_string(index=False))
df1.to_csv('resultados/top_10_clientes.csv', index=False, encoding='utf-8-sig')
print("Salvo: resultados/top_10_clientes.csv")

# CONSULTA 2: Produtos mais vendidos
print("\n2. PRODUTOS MAIS VENDIDOS (TOP 10)")
print("-"*50)

query2 = """
SELECT 
    nome_produto,
    categoria,
    SUM(quantidade) as quantidade_vendida,
    ROUND(SUM(preco_total), 2) as receita,
    COUNT(DISTINCT id_pedido) as pedidos
FROM vendas
WHERE status_pedido = 'Entregue'
GROUP BY nome_produto, categoria
ORDER BY quantidade_vendida DESC
LIMIT 10
"""

df2 = pd.read_sql_query(query2, conexao)
print(df2.to_string(index=False))
df2.to_csv('resultados/ranking_produtos.csv', index=False, encoding='utf-8-sig')
print("Salvo: resultados/ranking_produtos.csv")

# CONSULTA 3: Crescimento mensal
print("\n3. CRESCIMENTO MENSAL DAS VENDAS")
print("-"*50)

query3 = """
SELECT 
    ano,
    mes,
    COUNT(DISTINCT id_pedido) as total_pedidos,
    ROUND(SUM(preco_total), 2) as receita
FROM vendas
WHERE status_pedido = 'Entregue'
GROUP BY ano, mes
ORDER BY ano, mes
"""

df3 = pd.read_sql_query(query3, conexao)
print(df3.to_string(index=False))
df3.to_csv('resultados/crescimento_mensal.csv', index=False, encoding='utf-8-sig')
print("Salvo: resultados/crescimento_mensal.csv")

# CONSULTA 4: Análise por status
print("\n4. ANÁLISE POR STATUS DO PEDIDO")
print("-"*50)

query4 = """
SELECT 
    status_pedido,
    COUNT(DISTINCT id_pedido) as total_pedidos,
    ROUND(SUM(preco_total), 2) as valor_total,
    ROUND(AVG(preco_total), 2) as ticket_medio,
    COUNT(DISTINCT id_cliente) as clientes
FROM vendas
GROUP BY status_pedido
ORDER BY valor_total DESC
"""

df4 = pd.read_sql_query(query4, conexao)
print(df4.to_string(index=False))
df4.to_csv('resultados/analise_status.csv', index=False, encoding='utf-8-sig')
print("Salvo: resultados/analise_status.csv")

# CONSULTA 5: Melhores categorias
print("\n5. MELHORES CATEGORIAS")
print("-"*50)

query5 = """
SELECT 
    categoria,
    COUNT(DISTINCT id_pedido) as pedidos,
    SUM(quantidade) as unidades_vendidas,
    ROUND(SUM(preco_total), 2) as receita
FROM vendas
WHERE status_pedido = 'Entregue'
GROUP BY categoria
ORDER BY receita DESC
LIMIT 10
"""

df5 = pd.read_sql_query(query5, conexao)
print(df5.to_string(index=False))
df5.to_csv('resultados/melhores_categorias.csv', index=False, encoding='utf-8-sig')
print("Salvo: resultados/melhores_categorias.csv")

# CONSULTA 6: Métodos de pagamento
print("\n6. MÉTODOS DE PAGAMENTO MAIS USADOS")
print("-"*50)

query6 = """
SELECT 
    metodo_pagamento,
    COUNT(DISTINCT id_pedido) as pedidos,
    ROUND(SUM(preco_total), 2) as valor_total,
    ROUND(AVG(preco_total), 2) as ticket_medio
FROM vendas
WHERE status_pedido = 'Entregue'
GROUP BY metodo_pagamento
ORDER BY valor_total DESC
"""

df6 = pd.read_sql_query(query6, conexao)
print(df6.to_string(index=False))
df6.to_csv('resultados/analise_pagamento.csv', index=False, encoding='utf-8-sig')
print("Salvo: resultados/analise_pagamento.csv")

# Fechar conexão
conexao.close()

print("TODAS AS CONSULTAS FORAM EXECUTADAS!")
print("\nARQUIVOS GERADOS NA PASTA 'resultados/':")
print("   1. top_10_clientes.csv")
print("   2. ranking_produtos.csv")
print("   3. crescimento_mensal.csv")
print("   4. analise_status.csv")
print("   5. melhores_categorias.csv")
print("   6. analise_pagamento.csv")