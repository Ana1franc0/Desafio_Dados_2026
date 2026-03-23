# OUTLIERS - Casos estranhos que fogem do padrão. Outliers são dados que destoam do resto. Exemplos: 
# - Quase todos pedidos são R$ 50-200, mas alguém comprou R$ 10.000
# - Cliente que compra todo dia (enquanto outros compram 1x por mês)
# Evita tomar decisões erradas baseadas em casos raros
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

print("ANÁLISE DE OUTLIERS")

# 1. ESTATÍSTICAS BÁSICAS
print("\nEstatísticas dos valores dos pedidos:")
print(f"   Média: R$ {df_vendas['preco_total'].mean():,.2f}")
print(f"   Mediana: R$ {df_vendas['preco_total'].median():,.2f}")
print(f"   Mínimo: R$ {df_vendas['preco_total'].min():,.2f}")
print(f"   Máximo: R$ {df_vendas['preco_total'].max():,.2f}")
print(f"   Desvio padrão: R$ {df_vendas['preco_total'].std():,.2f}")

# 2. IDENTIFICAR OUTLIERS (Método IQR)
print("\nIdentificando outliers pelo método IQR...")

Q1 = df_vendas['preco_total'].quantile(0.25)
Q3 = df_vendas['preco_total'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df_vendas[(df_vendas['preco_total'] < limite_inferior) | 
                     (df_vendas['preco_total'] > limite_superior)]

print(f"\nResultados:")
print(f"   Q1 (25%): R$ {Q1:,.2f}")
print(f"   Q3 (75%): R$ {Q3:,.2f}")
print(f"   IQR (amplitude): R$ {IQR:,.2f}")
print(f"   Limite inferior: R$ {limite_inferior:,.2f}")
print(f"   Limite superior: R$ {limite_superior:,.2f}")
print(f"   Outliers encontrados: {len(outliers):,} pedidos")
print(f"   Percentual de outliers: {len(outliers)/len(df_vendas)*100:.2f}%")

if len(outliers) > 0:
    print(f"\nImpacto dos outliers:")
    print(f"   Valor total dos outliers: R$ {outliers['preco_total'].sum():,.2f}")
    print(f"   Ticket médio dos outliers: R$ {outliers['preco_total'].mean():,.2f}")
    print(f"   Percentual do faturamento: {outliers['preco_total'].sum()/df_vendas['preco_total'].sum()*100:.2f}%")

# 3. OUTLIERS POR STATUS
print("\nOutliers por status do pedido:")

for status in df_vendas['status_pedido'].unique():
    df_status = df_vendas[df_vendas['status_pedido'] == status]
    outliers_status = df_status[(df_status['preco_total'] < limite_inferior) | 
                                 (df_status['preco_total'] > limite_superior)]
    if len(df_status) > 0:
        print(f"   {status}: {len(outliers_status)} outliers ({len(outliers_status)/len(df_status)*100:.1f}%)")

# 4. GERAR GRÁFICOS
print("\nGerando gráficos...")

# Criar figura com 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Gráfico 1: Boxplot geral
sns.boxplot(y=df_vendas['preco_total'], ax=axes[0])
axes[0].set_title('Outliers - Valor dos Pedidos')
axes[0].set_ylabel('Valor do Pedido (R$)')

# Gráfico 2: Boxplot por status
sns.boxplot(x='status_pedido', y='preco_total', data=df_vendas, ax=axes[1])
axes[1].set_title('Outliers por Status')
axes[1].tick_params(axis='x', rotation=45)

# Gráfico 3: Histograma com destaque para outliers
axes[2].hist(df_vendas['preco_total'], bins=50, alpha=0.7, label='Todos pedidos')
if len(outliers) > 0:
    axes[2].hist(outliers['preco_total'], bins=20, alpha=0.7, color='red', label='Outliers')
axes[2].set_title('Distribuição dos Valores')
axes[2].set_xlabel('Valor do Pedido (R$)')
axes[2].set_ylabel('Frequência')
axes[2].legend()

plt.tight_layout()
plt.savefig('resultados/analise_outliers.png', dpi=150, bbox_inches='tight')
print("   Gráfico salvo: resultados/analise_outliers.png")

# 5. SALVAR RESULTADOS

# Salvar lista de outliers
outliers.to_csv('resultados/outliers_lista.csv', index=False, encoding='utf-8-sig')
print("   Lista de outliers salva: resultados/outliers_lista.csv")

# Salvar resumo em TXT
with open('resultados/resumo_outliers.txt', 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("RESUMO DA ANÁLISE DE OUTLIERS\n")
    f.write("="*60 + "\n\n")
    
    f.write(f"Total de pedidos analisados: {len(df_vendas):,}\n")
    f.write(f"Outliers identificados: {len(outliers):,} ({len(outliers)/len(df_vendas)*100:.2f}%)\n\n")
    
    f.write("Estatísticas dos outliers:\n")
    f.write(f"  Valor mínimo: R$ {outliers['preco_total'].min():,.2f}\n")
    f.write(f"  Valor máximo: R$ {outliers['preco_total'].max():,.2f}\n")
    f.write(f"  Valor médio: R$ {outliers['preco_total'].mean():,.2f}\n")
    f.write(f"  Valor total: R$ {outliers['preco_total'].sum():,.2f}\n\n")
    
    f.write("Limites de detecção:\n")
    f.write(f"  Limite inferior: R$ {limite_inferior:,.2f}\n")
    f.write(f"  Limite superior: R$ {limite_superior:,.2f}\n")

print("   Resumo salvo: resultados/resumo_outliers.txt")

# Fechar conexão
conexao.close()

print("ANÁLISE DE OUTLIERS CONCLUÍDA!")
print("\nArquivos gerados:")
print("   - resultados/analise_outliers.png")
print("   - resultados/outliers_lista.csv")
print("   - resultados/resumo_outliers.txt")