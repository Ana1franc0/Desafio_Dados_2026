# CORRELAÇÃO - Quando uma coisa influencia outra, mostra se duas variáveis andam juntas (separa clientes por comportamento)
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Criar pasta de resultados
os.makedirs('resultados', exist_ok=True)

# Conectar ao banco
conexao = sqlite3.connect('dados/ecommerce.db')

# Carregar dados
df_vendas = pd.read_sql_query("SELECT * FROM vendas", conexao)

print("ANÁLISE DE CORRELAÇÃO")

# 1. MATRIZ DE CORRELAÇÃO
print("\nCalculando correlações...")

# Selecionar colunas numéricas
colunas_numericas = ['preco_total', 'quantidade']
if 'ano' in df_vendas.columns:
    colunas_numericas.append('ano')
if 'mes' in df_vendas.columns:
    colunas_numericas.append('mes')

df_corr = df_vendas[colunas_numericas].copy()
corr_matrix = df_corr.corr()

print("\nMatriz de Correlação:")
print(corr_matrix.round(4))

# 2. INTERPRETAÇÃO DA CORRELAÇÃO
print("\nInterpretação:")

correlacao = corr_matrix.loc['preco_total', 'quantidade']
print(f"\nCorrelação entre preço_total e quantidade: {correlacao:.4f}")

if correlacao > 0.7:
    print("   → Correlação FORTE POSITIVA")
    print("   → Significado: clientes que compram mais itens, gastam mais")
    print("   → Estratégia: Incentivar compra de múltiplos itens (combos, frete grátis acima de X itens)")
elif correlacao > 0.3:
    print("   → Correlação MODERADA POSITIVA")
    print("   → Significado: há alguma relação entre quantidade e valor")
    print("   → Estratégia: Vale a pena testar promoções de upsell")
elif correlacao > -0.3:
    print("   → Correlação FRACA ou inexistente")
    print("   → Significado: quantidade não influencia o valor do pedido")
    print("   → Estratégia: Focar em vender produtos de maior valor, não em quantidade")
elif correlacao > -0.7:
    print("   → Correlação MODERADA NEGATIVA")
    print("   → Significado: mais itens = pedidos mais baratos")
    print("   → Estratégia: Revisar política de descontos e combos")
else:
    print("   → Correlação FORTE NEGATIVA")
    print("   → Significado: quanto mais itens, mais barato fica o pedido")
    print("   → Estratégia: Analisar se há muitos produtos de baixo valor sendo comprados juntos")

print("\nCorrelação por status do pedido:")

for status in df_vendas['status_pedido'].unique():
    df_status = df_vendas[df_vendas['status_pedido'] == status]
    if len(df_status) > 1:
        corr_status = df_status['preco_total'].corr(df_status['quantidade'])
        print(f"   {status}: {corr_status:.4f}")

# 4. GERAR GRÁFICOS
print("\nGerando gráficos...")

# Criar figura com 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfico 1: Heatmap da correlação
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.3f', square=True, ax=axes[0])
axes[0].set_title('Matriz de Correlação')

# Gráfico 2: Scatter plot preço x quantidade
sns.scatterplot(x='quantidade', y='preco_total', data=df_vendas, alpha=0.5, ax=axes[1])
axes[1].set_title('Relação: Quantidade x Preço Total')
axes[1].set_xlabel('Quantidade de Itens')
axes[1].set_ylabel('Preço Total (R$)')

plt.tight_layout()
plt.savefig('resultados/analise_correlacao.png', dpi=150, bbox_inches='tight')
print("  Gráfico salvo: resultados/analise_correlacao.png")

# 5. SALVAR RESULTADOS

# Salvar matriz de correlação
corr_matrix.to_csv('resultados/matriz_correlacao.csv', encoding='utf-8-sig')
print("   Matriz salva: resultados/matriz_correlacao.csv")

# Salvar resumo em TXT
with open('resultados/resumo_correlacao.txt', 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("RESUMO DA ANÁLISE DE CORRELAÇÃO\n")
    f.write("="*60 + "\n\n")
    
    f.write("Matriz de Correlação:\n")
    f.write(corr_matrix.round(4).to_string())
    f.write("\n\n")
    
    f.write("Interpretação:\n")
    f.write(f"Correlação preço_total x quantidade: {correlacao:.4f}\n")
    
    if correlacao > 0.7:
        f.write("Classificação: FORTE POSITIVA\n")
        f.write("Conclusão: Clientes que compram mais itens gastam mais.\n")
        f.write("Ação sugerida: Criar promoções que incentivem compra de múltiplos itens.\n")
    elif correlacao > 0.3:
        f.write("Classificação: MODERADA POSITIVA\n")
        f.write("Conclusão: Há relação entre quantidade e valor.\n")
        f.write("Ação sugerida: Testar estratégias de upsell.\n")
    elif correlacao > -0.3:
        f.write("Classificação: FRACA\n")
        f.write("Conclusão: Quantidade não influencia o valor.\n")
        f.write("Ação sugerida: Focar em produtos de maior valor agregado.\n")
    else:
        f.write("Classificação: NEGATIVA\n")
        f.write("Conclusão: Mais itens = pedidos mais baratos.\n")
        f.write("Ação sugerida: Revisar política de descontos.\n")

print("   Resumo salvo: resultados/resumo_correlacao.txt")

# Fechar conexão
conexao.close()

print("ANÁLISE DE CORRELAÇÃO CONCLUÍDA!")
print("\nArquivos gerados:")
print("   - resultados/analise_correlacao.png")
print("   - resultados/matriz_correlacao.csv")
print("   - resultados/resumo_correlacao.txt")