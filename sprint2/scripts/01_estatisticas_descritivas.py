# Estatísticas descritivas 
# Cacular números básicos que contam a história do negócio 
# Como está a "saúde" do sistema (o negócio está bem ou mal?). Valor típico de um pedido, menor e maior pedido, se os valores são todos parecidos ou não (o quanto variam)
import sqlite3
import pandas as pd
import os
from datetime import datetime

# Criar pasta de resultados
os.makedirs('resultados', exist_ok=True)

# Conectar ao banco
conexao = sqlite3.connect('dados/ecommerce.db')
df_vendas = pd.read_sql_query("SELECT * FROM vendas", conexao)

# Converter data
df_vendas['data_pedido'] = pd.to_datetime(df_vendas['data_pedido'])

df_vendas['mes_ano'] = df_vendas['data_pedido'].dt.strftime('%Y-%m')

# Filtrar por status
df_entregues = df_vendas[df_vendas['status_pedido'] == 'Entregue']
df_cancelados = df_vendas[df_vendas['status_pedido'] == 'Cancelado']

# Abrir o arquivo para escrever tudo

with open('resultados/estatisticas_descritivas.txt', 'w', encoding='utf-8') as f:
    
    # Cabeçalho
    f.write("ESTATÍSTICAS DESCRITIVAS - ANÁLISE COMPLETA\n")
    f.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    
    # 1. INFORMAÇÕES GERAIS
    f.write("1. INFORMAÇÕES GERAIS DO BANCO\n")
    f.write("-"*50 + "\n")
    f.write(f"Total de registros no banco: {len(df_vendas):,}\n")
    f.write(f"Período dos dados: {df_vendas['data_pedido'].min().date()} até {df_vendas['data_pedido'].max().date()}\n")
    f.write(f"Dias de operação: {(df_vendas['data_pedido'].max() - df_vendas['data_pedido'].min()).days}\n")
    f.write(f"Clientes únicos: {df_vendas['id_cliente'].nunique():,}\n")
    f.write(f"Produtos únicos: {df_vendas['id_produto'].nunique():,}\n")
    f.write(f"Categorias únicas: {df_vendas['categoria'].nunique()}\n")
    f.write(f"Métodos de pagamento: {df_vendas['metodo_pagamento'].nunique()}\n\n")
    
    # 2. ANÁLISE POR STATUS DO PEDIDO
    f.write("2. ANÁLISE POR STATUS DO PEDIDO\n")
    f.write("-"*50 + "\n")
    
    status_counts = df_vendas['status_pedido'].value_counts()
    for status, qtd in status_counts.items():
        percentual = qtd / len(df_vendas) * 100
        f.write(f"{status}: {qtd:,} pedidos ({percentual:.1f}%)\n")
    f.write("\n")
    
    # 3. ANÁLISE FINANCEIRA
    f.write("3. ANÁLISE FINANCEIRA\n")
    f.write("-"*50 + "\n")
    f.write(f"Faturamento total (todos pedidos): R$ {df_vendas['preco_total'].sum():,.2f}\n")
    f.write(f"Faturamento (apenas entregues): R$ {df_entregues['preco_total'].sum():,.2f}\n")
    f.write(f"Faturamento (cancelados): R$ {df_cancelados['preco_total'].sum():,.2f}\n")
    f.write(f"PERDA POR CANCELAMENTO: R$ {df_cancelados['preco_total'].sum():,.2f}\n")
    f.write(f"Ticket médio (todos pedidos): R$ {df_vendas['preco_total'].mean():,.2f}\n")
    f.write(f"Ticket médio (entregues): R$ {df_entregues['preco_total'].mean():,.2f}\n")
    f.write(f"Ticket médio (cancelados): R$ {df_cancelados['preco_total'].mean():,.2f}\n")
    f.write(f"Pedido mais caro: R$ {df_vendas['preco_total'].max():,.2f}\n")
    f.write(f"Pedido mais barato: R$ {df_vendas['preco_total'].min():,.2f}\n")
    f.write(f"Desvio padrão dos valores: R$ {df_vendas['preco_total'].std():,.2f}\n\n")
    
    # 4. ANÁLISE DE QUANTIDADES
    f.write("4. ANÁLISE DE QUANTIDADES\n")
    f.write("-"*50 + "\n")
    f.write(f"Total de itens vendidos: {df_vendas['quantidade'].sum():,}\n")
    f.write(f"Média de itens por pedido: {df_vendas['quantidade'].mean():.2f}\n")
    f.write(f"Máximo de itens em um pedido: {df_vendas['quantidade'].max()}\n")
    f.write(f"Mínimo de itens em um pedido: {df_vendas['quantidade'].min()}\n\n")
    
    # 5. ESTATÍSTICAS DETALHADAS (PANDAS)
    f.write("5. ESTATÍSTICAS DETALHADAS (PANDAS)\n")
    f.write("-"*50 + "\n")
    f.write(str(df_vendas[['preco_total', 'quantidade']].describe()))
    f.write("\n\n")
    
    # 6. TOP 10 CLIENTES 
    f.write("6. TOP 10 CLIENTES QUE MAIS GASTARAM\n")
    f.write("-"*50 + "\n")
    top_clientes = df_entregues.groupby(['id_cliente', 'nome_cliente'])['preco_total'].sum().reset_index()
    top_clientes = top_clientes.sort_values('preco_total', ascending=False).head(10)
    for i, row in top_clientes.iterrows():
        f.write(f"{row['nome_cliente']}: R$ {row['preco_total']:,.2f}\n")
    f.write("\n")
    
    # 7. TOP 10 PRODUTOS MAIS VENDIDOS
    f.write("7. TOP 10 PRODUTOS MAIS VENDIDOS\n")
    f.write("-"*50 + "\n")
    top_produtos = df_entregues.groupby('nome_produto')['quantidade'].sum().reset_index()
    top_produtos = top_produtos.sort_values('quantidade', ascending=False).head(10)
    for i, row in top_produtos.iterrows():
        f.write(f"{row['nome_produto']}: {row['quantidade']} unidades\n")
    f.write("\n")
    
    # 8. ANÁLISE POR CATEGORIA
    f.write("8. ANÁLISE POR CATEGORIA (Top 5 por faturamento)\n")
    f.write("-"*50 + "\n")
    top_categorias = df_entregues.groupby('categoria').agg({
        'preco_total': 'sum',
        'quantidade': 'sum',
        'id_pedido': 'count'
    }).rename(columns={'id_pedido': 'pedidos'}).sort_values('preco_total', ascending=False).head(5)
    for categoria, row in top_categorias.iterrows():
        f.write(f"{categoria}:\n")
        f.write(f"   Faturamento: R$ {row['preco_total']:,.2f}\n")
        f.write(f"   Unidades vendidas: {row['quantidade']:,}\n")
        f.write(f"   Pedidos: {row['pedidos']:,}\n\n")
    
    # 9. ANÁLISE POR MÊS
    f.write("9. ANÁLISE MENSAL DE VENDAS\n")
    f.write("-"*50 + "\n")
    df_vendas['mes_ano'] = df_vendas['data_pedido'].dt.strftime('%Y-%m')
    vendas_mensais = df_entregues.groupby('mes_ano').agg({
        'preco_total': 'sum',
        'id_pedido': 'count'
    }).rename(columns={'id_pedido': 'pedidos'})
    for mes, row in vendas_mensais.iterrows():
        f.write(f"{mes}: {row['pedidos']} pedidos - R$ {row['preco_total']:,.2f}\n")
    f.write("\n")
    
    # 10. ANÁLISE POR MÉTODO DE PAGAMENTO
    f.write("10. ANÁLISE POR MÉTODO DE PAGAMENTO\n")
    f.write("-"*50 + "\n")
    pagamentos = df_entregues.groupby('metodo_pagamento')['preco_total'].agg(['sum', 'count', 'mean']).round(2)
    for metodo, row in pagamentos.iterrows():
        f.write(f"{metodo}:\n")
        f.write(f"   Total: R$ {row['sum']:,.2f}\n")
        f.write(f"   Pedidos: {row['count']:,}\n")
        f.write(f"   Ticket médio: R$ {row['mean']:,.2f}\n\n")
    
    # 11. PRINCIPAIS INSIGHTS
    f.write("11. PRINCIPAIS INSIGHTS IDENTIFICADOS\n")
    f.write("-"*50 + "\n")
    
    # Calcular alguns insights automaticamente
    taxa_cancelamento = len(df_cancelados) / len(df_vendas) * 100
    ticket_medio = df_vendas['preco_total'].mean()
    perc_perda = df_cancelados['preco_total'].sum() / df_vendas['preco_total'].sum() * 100
    
    f.write(f"ALERTA: Taxa de cancelamento de {taxa_cancelamento:.1f}% - muito acima do mercado (ideal <10%)\n")
    f.write(f"PERDA FINANCEIRA: R$ {df_cancelados['preco_total'].sum():,.2f} ({perc_perda:.1f}% do faturamento potencial)\n")
    f.write(f"OPORTUNIDADE: Reduzir cancelamentos para 10% aumentaria faturamento em R$ {df_cancelados['preco_total'].sum() * 0.7:,.2f}\n")
    f.write(f"CLIENTES VIP: {len(top_clientes)} clientes concentram parte significativa da receita\n")
    
    f.write("FIM DA ANÁLISE\n")

print("\nArquivo COMPLETO salvo em: resultados/estatisticas_descritivas.txt")

conexao.close()