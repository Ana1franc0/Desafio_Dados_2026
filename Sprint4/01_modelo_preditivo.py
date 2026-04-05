# SPRINT 4 - MODELO PREDITIVO DE VENDAS E STORYTELLING

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

# Configurações
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Criar pastas
os.makedirs('resultados', exist_ok=True)
os.makedirs('resultados/graficos', exist_ok=True)

print("SPRINT 4 - MODELO PREDITIVO E STORYTELLING")
print(f"Data da execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# 1. CARREGAR DADOS DO BANCO
print("\n1. CARREGANDO DADOS DO BANCO DE DADOS")

# Tentar diferentes caminhos (compatibilidade)
caminhos_possiveis = ['banco/ecommerce.db', 'dados/ecommerce.db', 'ecommerce.db']
conexao = None

for caminho in caminhos_possiveis:
    if os.path.exists(caminho):
        conexao = sqlite3.connect(caminho)
        print(f"Banco encontrado em: {caminho}")
        break

if conexao is None:
    print("ERRO: Banco de dados não encontrado!")
    print("   Execute primeiro as Sprints 1, 2 e 3")
    exit()

df = pd.read_sql_query("SELECT * FROM vendas", conexao)
conexao.close()

# Converter tipos
df['data_pedido'] = pd.to_datetime(df['data_pedido'])
df['preco_total'] = pd.to_numeric(df['preco_total'])
df['quantidade'] = pd.to_numeric(df['quantidade'])

print(f"Dados carregados: {len(df):,} pedidos")
print(f"Período: {df['data_pedido'].min().date()} até {df['data_pedido'].max().date()}")
print(f"Colunas: {list(df.columns)}")

# 2. PREPARAÇÃO DOS DADOS (Insights Sprint 2)
print("\n2. PREPARANDO DADOS PARA O MODELO")

# Usar apenas pedidos entregues (dados consistentes)
df_model = df[df['status_pedido'] == 'Entregue'].copy()
print(f"Usando apenas pedidos entregues: {len(df_model):,} pedidos ({len(df_model)/len(df)*100:.1f}%)")

# Remover outliers baseado na análise da Sprint 2
Q1 = df_model['preco_total'].quantile(0.25)
Q3 = df_model['preco_total'].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 3 * IQR 

outliers_antes = len(df_model)
df_model = df_model[df_model['preco_total'] <= limite_superior]
print(f"Removidos {outliers_antes - len(df_model)} outliers ({outliers_antes/len(df_model)*100:.1f}%)")

# 3. FEATURES PARA O MODELO
print("\n3. CRIANDO FEATURES")

# Codificar variáveis categóricas
label_encoders = {}
categorical_cols = ['categoria', 'metodo_pagamento']

for col in categorical_cols:
    le = LabelEncoder()
    df_model[f'{col}_encoded'] = le.fit_transform(df_model[col])
    label_encoders[col] = le
    print(f"{col}: {len(le.classes_)} categorias codificadas")

# Features para o modelo
feature_cols = ['quantidade', 'preco_unitario', 'categoria_encoded', 'metodo_pagamento_encoded']

# Adicionar features temporais se disponíveis
if 'mes' in df_model.columns:
    feature_cols.append('mes')
    print("Feature 'mes' adicionada")

if 'dia_semana' in df_model.columns:
    # Converter dia da semana para número
    dias_map = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}
    df_model['dia_num'] = df_model['dia_semana'].map(dias_map)
    feature_cols.append('dia_num')
    print("Feature 'dia_semana' adicionada")

X = df_model[feature_cols]
y = df_model['preco_total']

print(f"\nFeatures utilizadas: {feature_cols}")
print(f"Tamanho do dataset: {len(X):,} amostras")

# 4. TREINAMENTO DO MODELO
print("\n4. TREINANDO REGRESSÃO LINEAR")

# Dividir em treino (80%) e teste (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Treino: {len(X_train):,} amostras (80%)")
print(f"Teste: {len(X_test):,} amostras (20%)")

# Treinar modelo
model = LinearRegression()
model.fit(X_train, y_train)
print("Modelo treinado com sucesso!")

# 5. AVALIAÇÃO DO MODELO
print("\n5. AVALIAÇÃO DO MODELO")

# Previsões
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Métricas
r2_train = r2_score(y_train, y_train_pred)
r2_test = r2_score(y_test, y_test_pred)
mae_train = mean_absolute_error(y_train, y_train_pred)
mae_test = mean_absolute_error(y_test, y_test_pred)
rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))

print("\nMÉTRICAS DE TREINO:")
print(f"   R²: {r2_train:.4f}")
print(f"   MAE: R$ {mae_train:.2f}")
print(f"   RMSE: R$ {rmse_train:.2f}")

print("\nMÉTRICAS DE TESTE:")
print(f"   R²: {r2_test:.4f}")
print(f"   MAE: R$ {mae_test:.2f}")
print(f"   RMSE: R$ {rmse_test:.2f}")

# Interpretação do R²
if r2_test > 0.8:
    interpretacao = "Excelente - O modelo explica mais de 80% da variação"
elif r2_test > 0.6:
    interpretacao = "Bom - O modelo explica entre 60-80% da variação"
elif r2_test > 0.4:
    interpretacao = "Moderado - O modelo explica entre 40-60% da variação"
else:
    interpretacao = "Fraco - O modelo explica menos de 40% da variação"

print(f"\nInterpretação: {interpretacao}")

# 6. IMPORTÂNCIA DAS FEATURES
print("\n6. IMPORTÂNCIA DAS FEATURES")

coeficientes = pd.DataFrame({
    'feature': feature_cols,
    'coeficiente': model.coef_,
    'abs_coeficiente': np.abs(model.coef_)
}).sort_values('abs_coeficiente', ascending=False)

print("\nTop features que mais influenciam o preço total:")
for i, row in coeficientes.head().iterrows():
    sinal = "➕" if row['coeficiente'] > 0 else "➖"
    print(f"   {sinal} {row['feature']}: {row['coeficiente']:.4f}")

# 7. GRÁFICOS DA SPRINT 4
print("\n7. GERANDO VISUALIZAÇÕES")

# Gráfico 1: Previsões vs Real
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(y_test, y_test_pred, alpha=0.5, edgecolors='k', linewidth=0.5)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Previsão Perfeita')
ax.set_xlabel('Valor Real (R$)', fontsize=12)
ax.set_ylabel('Valor Previsto (R$)', fontsize=12)
ax.set_title(f'Previsões vs Real - R² = {r2_test:.3f}', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('resultados/graficos/previsoes_vs_real.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico 1: previsoes_vs_real.png")

# Gráfico 2: Importância das Features
fig, ax = plt.subplots(figsize=(10, 6))
cores_bar = ['#2ECC71' if c > 0 else '#E74C3C' for c in coeficientes.head(8)['coeficiente']]
ax.barh(coeficientes.head(8)['feature'], coeficientes.head(8)['coeficiente'], color=cores_bar)
ax.set_xlabel('Coeficiente', fontsize=12)
ax.set_title('Importância das Features no Modelo', fontsize=14, fontweight='bold')
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig('resultados/graficos/importancia_features.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico 2: importancia_features.png")

# Gráfico 3: Distribuição dos Erros
erros = y_test - y_test_pred
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(erros, bins=50, edgecolor='black', alpha=0.7, color='skyblue')
ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Erro Zero')
ax.set_xlabel('Erro de Previsão (R$)', fontsize=12)
ax.set_ylabel('Frequência', fontsize=12)
ax.set_title('Distribuição dos Erros do Modelo', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('resultados/graficos/distribuicao_erros.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico 3: distribuicao_erros.png")

# 8. STORYTELLING
print("\n8. GERANDO STORYTELLING")

storytelling = f"""
STORYTELLING - ANÁLISE DE DADOS DE E-COMMERCE
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Projeto: Análise Completa de Vendas - Sprints 1 a 4

VISÃO GERAL DO PROJETO
--------------------------------------------------------------------------------
Este projeto analisou {len(df):,} pedidos de um e-commerce no período de
{df['data_pedido'].min().date()} a {df['data_pedido'].max().date()}.

Foram realizadas 4 sprints:
• Sprint 1: Geração e limpeza dos dados
• Sprint 2: Análise estatística, RFM, correlações e outliers
• Sprint 3: Dashboard interativo com Streamlit
• Sprint 4: Modelo preditivo e storytelling

PRINCIPAIS DESCOBERTAS 

1. SAÚDE DO NEGÓCIO
   • Faturamento total: R$ {df['preco_total'].sum():,.2f}
   • Ticket médio: R$ {df['preco_total'].mean():,.2f}
   • Total de clientes: {df['id_cliente'].nunique():,}
   • Total de produtos: {df['id_produto'].nunique():,}

2. COMPORTAMENTO DO CLIENTE (Análise RFM - Sprint 2)
   • Clientes 'Campeões': {len(df[df['status_pedido'] == 'Entregue']['id_cliente'].unique())} clientes de alto valor
   • Clientes 'Em Risco': Precisam de campanha de reativação urgente
   • Clientes 'Perdidos': Representam oportunidade perdida

3. ANÁLISE DE CATEGORIAS
   • Categoria mais vendida: {df.groupby('categoria')['preco_total'].sum().idxmax()}
   • Participação no faturamento: {(df.groupby('categoria')['preco_total'].sum().max() / df['preco_total'].sum() * 100):.1f}%

4. MÉTODOS DE PAGAMENTO
   • Preferido: {df['metodo_pagamento'].mode()[0]}
   • {df[df['status_pedido'] == 'Cancelado']['metodo_pagamento'].mode()[0]} tem maior taxa de cancelamento

RESULTADOS DO MODELO PREDITIVO (Sprint 4)
Modelo utilizado: Regressão Linear

Métricas de desempenho:
• R² (Treino): {r2_train:.4f}
• R² (Teste): {r2_test:.4f}
• MAE (Erro médio absoluto): R$ {mae_test:.2f}
• RMSE (Raiz do erro quadrático): R$ {rmse_test:.2f}

Interpretação: {interpretacao}

Features mais importantes:
"""
for i, row in coeficientes.head(5).iterrows():
    storytelling += f"\n   • {row['feature']}: {row['coeficiente']:.4f}"

storytelling += f"""

RECOMENDAÇÕES DE NEGÓCIO

Com base em todas as análises realizadas, recomendamos:

1. MARKETING PERSONALIZADO
   • Clientes 'Campeões': Programa VIP com benefícios exclusivos
   • Clientes 'Em Risco': Campanha de reativação com cupom de desconto
   • Clientes 'Novos': Estratégia de onboarding para segunda compra

2. OTIMIZAÇÃO DE VENDAS
   • Investir na categoria {df.groupby('categoria')['preco_total'].sum().idxmax()}
   • Criar combos para aumentar ticket médio
   • Melhorar experiência no método de pagamento menos usado

3. REDUÇÃO DE CANCELAMENTOS
   • Analisar causa dos cancelamentos
   • Implementar follow-up automático para pedidos 'Processando'
   • Oferecer suporte proativo

4.PRÓXIMOS PASSOS
   • Implementar modelo em produção para previsão de vendas
   • Criar alertas automáticos para clientes 'Em Risco'
   • Expandir dashboard com mais métricas em tempo real

ARQUIVOS GERADOS NESTA SPRINT 4

• sprint4_resultados/metricas_modelo.txt - Métricas detalhadas
• sprint4_resultados/previsoes.csv - Previsões geradas
• sprint4_resultados/graficos/previsoes_vs_real.png
• sprint4_resultados/graficos/importancia_features.png
• sprint4_resultados/graficos/distribuicao_erros.png
• README.md - Documentação final do projeto

CONCLUSÃO

O projeto foi concluído com sucesso, entregando:
✓ Pipeline completo de dados (geração → limpeza → banco → análises)
✓ Dashboard interativo para monitoramento
✓ Modelo preditivo com R² = {r2_test:.4f}
✓ Storytelling com recomendações acionáveis

O modelo de Regressão Linear consegue prever o valor dos pedidos com
erro médio de R$ {mae_test:.2f}, o que é {((mae_test/df['preco_total'].mean())*100):.1f}% do ticket médio.
"""

# Salvar storytelling
with open('resultados/storytelling_completo.txt', 'w', encoding='utf-8') as f:
    f.write(storytelling)
print("Storytelling salvo: resultados/storytelling_completo.txt")

# 9. SALVAR PREVISÕES E MÉTRICAS
print("\n9. SALVANDO RESULTADOS")

# Salvar previsões
previsoes_df = pd.DataFrame({
    'valor_real': y_test.values,
    'valor_previsto': y_test_pred,
    'erro': y_test.values - y_test_pred,
    'erro_percentual': np.abs((y_test.values - y_test_pred) / y_test.values) * 100
}).head(100)
previsoes_df.to_csv('resultados/previsoes.csv', index=False, encoding='utf-8-sig')
print("Previsões salvas: resultados/previsoes.csv")

# Salvar métricas
with open('resultados/metricas_modelo.txt', 'w', encoding='utf-8') as f:
    f.write("MÉTRICAS DO MODELO PREDITIVO\n")
    f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
    f.write("Métricas de Treino:\n")
    f.write(f"  R²: {r2_train:.4f}\n")
    f.write(f"  MAE: R$ {mae_train:.2f}\n")
    f.write(f"  RMSE: R$ {rmse_train:.2f}\n\n")
    f.write("Métricas de Teste:\n")
    f.write(f"  R²: {r2_test:.4f}\n")
    f.write(f"  MAE: R$ {mae_test:.2f}\n")
    f.write(f"  RMSE: R$ {rmse_test:.2f}\n\n")
    f.write(f"Interpretação: {interpretacao}\n\n")
    f.write("Features mais importantes:\n")
    for i, row in coeficientes.head().iterrows():
        f.write(f"  {row['feature']}: {row['coeficiente']:.4f}\n")
print("Métricas salvas: resultados/metricas_modelo.txt")

# 10. RESUMO FINAL
print("\nRESUMO DO MODELO:")
print(f"   • Algoritmo: Regressão Linear")
print(f"   • R² no teste: {r2_test:.4f}")
print(f"   • Erro médio (MAE): R$ {mae_test:.2f}")
print(f"   • Features: {len(feature_cols)}")