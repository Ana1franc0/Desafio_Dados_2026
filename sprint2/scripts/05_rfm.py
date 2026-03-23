# RFM - SEGMENTAÇÃO DE CLIENTES 
# R de Recência -> Quando comprou pela última vez?
# F de Frequência -> Quantas vezes comprou?
# M de Monetário -> Quanto gastou no total?
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
df_vendas['data_pedido'] = pd.to_datetime(df_vendas['data_pedido'])

print("SEGMENTAÇÃO RFM - CLIENTES")

# 1. CALCULAR MÉTRICAS RFM
print("\nCalculando métricas RFM...")

# Data de referência (última data do banco + 1 dia)
data_ref = df_vendas['data_pedido'].max() + pd.Timedelta(days=1)

# Calcular RFM por cliente
rfm = df_vendas.groupby('id_cliente').agg({
    'data_pedido': lambda x: (data_ref - x.max()).days,  # Recência
    'id_pedido': 'nunique',  # Frequência (pedidos únicos)
    'preco_total': 'sum'  # Monetário
}).reset_index()

rfm.columns = ['id_cliente', 'recencia', 'frequencia', 'monetario']

# Adicionar nome do cliente
nomes_clientes = df_vendas[['id_cliente', 'nome_cliente']].drop_duplicates()
rfm = rfm.merge(nomes_clientes, on='id_cliente', how='left')

print(f"Total de clientes analisados: {len(rfm):,}")
print(f"   Recência média: {rfm['recencia'].mean():.0f} dias")
print(f"   Frequência média: {rfm['frequencia'].mean():.1f} pedidos")
print(f"   Monetário médio: R$ {rfm['monetario'].mean():,.2f}")

# 2. CRIAR SCORES (1 a 5)
print("\nCriando scores RFM...")

# Recência: quanto menor, melhor (score 5 para quem comprou ontem)
rfm['R_score'] = pd.qcut(rfm['recencia'].rank(method='first'), 5, labels=[5,4,3,2,1])

# Frequência: quanto maior, melhor
rfm['F_score'] = pd.qcut(rfm['frequencia'].rank(method='first'), 5, labels=[1,2,3,4,5])

# Monetário: quanto maior, melhor
rfm['M_score'] = pd.qcut(rfm['monetario'].rank(method='first'), 5, labels=[1,2,3,4,5])

# Converter para inteiro
rfm['R_score'] = rfm['R_score'].astype(int)
rfm['F_score'] = rfm['F_score'].astype(int)
rfm['M_score'] = rfm['M_score'].astype(int)

print(f"   R_score (Recência) - média: {rfm['R_score'].mean():.1f}")
print(f"   F_score (Frequência) - média: {rfm['F_score'].mean():.1f}")
print(f"   M_score (Monetário) - média: {rfm['M_score'].mean():.1f}")

# 3. CLASSIFICAR CLIENTES
print("\nClassificando clientes...")

def classificar_cliente(row):
    r = row['R_score']
    f = row['F_score']
    m = row['M_score']
    
    if r >= 4 and f >= 4 and m >= 4:
        return 'Campeão'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Leal'
    elif r >= 4 and f <= 2:
        return 'Novo'
    elif r <= 2 and f >= 3:
        return 'Em risco'
    elif r <= 2 and f <= 2:
        return 'Perdido'
    else:
        return 'Potencial'

rfm['segmento'] = rfm.apply(classificar_cliente, axis=1)

# 4. ESTATÍSTICAS POR SEGMENTO
print("\nEstatísticas por segmento:")

segmentos = rfm['segmento'].value_counts()
print("\nDistribuição:")
for segmento, quantidade in segmentos.items():
    percentual = quantidade / len(rfm) * 100
    monetario_medio = rfm[rfm['segmento'] == segmento]['monetario'].mean()
    recencia_media = rfm[rfm['segmento'] == segmento]['recencia'].mean()
    frequencia_media = rfm[rfm['segmento'] == segmento]['frequencia'].mean()
    
    print(f"\n   {segmento}:")
    print(f"      Quantidade: {quantidade} clientes ({percentual:.1f}%)")
    print(f"      Ticket médio: R$ {monetario_medio:,.2f}")
    print(f"      Recência média: {recencia_media:.0f} dias")
    print(f"      Frequência média: {frequencia_media:.1f} pedidos")

# 5. CLIENTES PRIORITÁRIOS

# Clientes "Em risco" que mais gastaram (prioridade para recuperar)
clientes_risco = rfm[rfm['segmento'] == 'Em risco'].sort_values('monetario', ascending=False).head(10)

if len(clientes_risco) > 0:
    print("\nTOP 10 CLIENTES 'EM RISCO' (prioridade para recuperação):")
    for i, row in clientes_risco.iterrows():
        print(f"   {row['nome_cliente']}: R$ {row['monetario']:,.2f} - {row['recencia']} dias sem comprar")

# Clientes "Campeões" (clientes VIP)
clientes_campeoes = rfm[rfm['segmento'] == '👑 Campeão'].sort_values('monetario', ascending=False).head(10)

if len(clientes_campeoes) > 0:
    print("\nTOP 10 CLIENTES 'CAMPEÕES' (clientes VIP):")
    for i, row in clientes_campeoes.iterrows():
        print(f"   {row['nome_cliente']}: R$ {row['monetario']:,.2f} - {row['frequencia']} pedidos")

# 6. GERAR GRÁFICOS
print("\nGerando gráficos...")

# Gráfico 1: Distribuição dos segmentos
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico de barras
segmentos.plot(kind='bar', ax=axes[0], color=['gold', 'green', 'blue', 'orange', 'red', 'gray'])
axes[0].set_title('Distribuição dos Segmentos de Clientes')
axes[0].set_xlabel('Segmento')
axes[0].set_ylabel('Número de Clientes')
axes[0].tick_params(axis='x', rotation=45)

# Gráfico de pizza
cores = ['gold', 'green', 'blue', 'orange', 'red', 'gray']
axes[1].pie(segmentos.values, labels=segmentos.index, autopct='%1.1f%%', colors=cores[:len(segmentos)])
axes[1].set_title('Proporção por Segmento')

plt.tight_layout()
plt.savefig('resultados/distribuicao_segmentos.png', dpi=150, bbox_inches='tight')
print("   Gráfico salvo: resultados/distribuicao_segmentos.png")

# Gráfico 2: Boxplot por segmento (monetário)
plt.figure(figsize=(12, 6))
sns.boxplot(x='segmento', y='monetario', data=rfm, order=segmentos.index)
plt.title('Distribuição do Valor Gasto por Segmento')
plt.xlabel('Segmento')
plt.ylabel('Valor Gasto (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('resultados/rfm_boxplot.png', dpi=150, bbox_inches='tight')
print("   Gráfico salvo: resultados/rfm_boxplot.png")

# 7. SALVAR RESULTADOS

# Salvar RFM completo
rfm.to_csv('resultados/analise_rfm_completa.csv', index=False, encoding='utf-8-sig')
print("   RFM completo salvo: resultados/analise_rfm_completa.csv")

# Salvar estatísticas por segmento
estatisticas_segmentos = rfm.groupby('segmento').agg({
    'monetario': ['sum', 'mean', 'count'],
    'frequencia': 'mean',
    'recencia': 'mean',
    'R_score': 'mean',
    'F_score': 'mean',
    'M_score': 'mean'
}).round(2)

estatisticas_segmentos.to_csv('resultados/estatisticas_por_segmento.csv', encoding='utf-8-sig')
print("   Estatísticas salvas: resultados/estatisticas_por_segmento.csv")

# Salvar clientes prioritários
clientes_risco.to_csv('resultados/clientes_em_risco.csv', index=False, encoding='utf-8-sig')
clientes_campeoes.to_csv('resultados/clientes_campeoes.csv', index=False, encoding='utf-8-sig')
print("   Clientes prioritários salvos")

# Salvar resumo em TXT
with open('resultados/resumo_rfm.txt', 'w', encoding='utf-8') as f:
    f.write("RESUMO DA ANÁLISE RFM\n")
    
    f.write(f"Total de clientes analisados: {len(rfm):,}\n\n")
    
    f.write("DISTRIBUIÇÃO DOS SEGMENTOS:\n")
    for segmento, quantidade in segmentos.items():
        percentual = quantidade / len(rfm) * 100
        f.write(f"  {segmento}: {quantidade} clientes ({percentual:.1f}%)\n")
    
    f.write("\n\nRECOMENDAÇÕES POR SEGMENTO:\n")
    f.write("-"*40 + "\n")
    f.write("CAMPEÕES: Manter como VIP, benefícios exclusivos, pedir indicações\n")
    f.write("LEAL: Programa de fidelidade, cupons para aumentar ticket\n")
    f.write("NOVO: Nutrir com conteúdo, segunda compra com desconto\n")
    f.write("EM RISCO: Campanha de reativação URGENTE, cupom forte\n")
    f.write("PERDIDO: Tentar reativar 1x, depois focar em novos\n")
    f.write("POTENCIAL: Estratégia de engajamento e conversão\n")

print("   Resumo salvo: resultados/resumo_rfm.txt")

# Fechar conexão
conexao.close()

print("ANÁLISE RFM CONCLUÍDA!")
print("\nArquivos gerados:")
print("   - resultados/distribuicao_segmentos.png")
print("   - resultados/rfm_boxplot.png")
print("   - resultados/analise_rfm_completa.csv")
print("   - resultados/estatisticas_por_segmento.csv")
print("   - resultados/clientes_em_risco.csv")
print("   - resultados/clientes_campeoes.csv")
print("   - resultados/resumo_rfm.txt")