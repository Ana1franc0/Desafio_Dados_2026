# streamlit run 01_dashboard.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard E-commerce", page_icon="📊")
st.title("Dashboard E-commerce - Sprint 3")

# Conectar ao banco
conn = sqlite3.connect('banco/ecommerce.db')

# Carregar dados
vendas = pd.read_sql_query("SELECT * FROM vendas", conn)
vendas['data_pedido'] = pd.to_datetime(vendas['data_pedido'])

# Calcular métricas
diario = vendas.groupby('data_pedido')['preco_total'].sum().reset_index()
diario.columns = ['data', 'faturamento']

vendas['mes'] = vendas['data_pedido'].dt.strftime('%Y-%m')
mensal = vendas.groupby('mes')['preco_total'].sum().reset_index()
mensal.columns = ['mes', 'faturamento']

conn.close()

# ========== FILTROS NA LATERAL ==========
st.sidebar.title("Filtros")

# Filtro de categoria
categorias = vendas['categoria'].unique().tolist()
categoria_selecionada = st.sidebar.multiselect(
    "Selecione as Categorias",
    categorias,
    default=categorias  # Começa com todas as categorias selecionadas
)

# Filtro de status
status_opcoes = vendas['status_pedido'].unique().tolist()
status_selecionado = st.sidebar.multiselect(
    "Selecione os Status",
    status_opcoes,
    default=status_opcoes 
)

# Aplicar os filtros
vendas_filtradas = vendas[
    vendas['categoria'].isin(categoria_selecionada) &
    vendas['status_pedido'].isin(status_selecionado)
]

# Recalcular métricas com filtro
diario_filtrado = vendas_filtradas.groupby('data_pedido')['preco_total'].sum().reset_index()
diario_filtrado.columns = ['data', 'faturamento']

mensal_filtrado = vendas_filtradas.groupby('mes')['preco_total'].sum().reset_index()
mensal_filtrado.columns = ['mes', 'faturamento']

# Mostrar resumo do filtro
st.sidebar.markdown("---")
st.sidebar.info(f"Mostrando {len(vendas_filtradas):,} pedidos")

# ========== KPIs ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Faturamento Total", f"R$ {vendas_filtradas['preco_total'].sum():,.2f}")

with col2:
    st.metric("Ticket Médio", f"R$ {vendas_filtradas['preco_total'].mean():,.2f}")

with col3:
    st.metric("Total de Pedidos", f"{len(vendas_filtradas):,}")

with col4:
    data_ref = vendas_filtradas['data_pedido'].max()
    data_limite = data_ref - pd.Timedelta(days=90)
    clientes_ativos = vendas_filtradas[vendas_filtradas['data_pedido'] >= data_limite]['id_cliente'].nunique()
    total_clientes = vendas_filtradas['id_cliente'].nunique()
    churn = 1 - (clientes_ativos / total_clientes) if total_clientes > 0 else 0
    st.metric("Churn Rate", f"{churn:.1%}")

st.markdown("---")

# ========== GRÁFICOS COLORIDOS ==========
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Faturamento Diário")
    fig1 = px.line(diario_filtrado, x='data', y='faturamento', 
                   title="Evolução Diária",
                   line_shape='spline',
                   color_discrete_sequence=['#2E86AB'])
    fig1.update_traces(line=dict(width=3))
    st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    st.subheader("Sazonalidade Mensal")
    fig2 = px.bar(mensal_filtrado, x='mes', y='faturamento',
                  title="Faturamento por Mês",
                  color='faturamento',
                  color_continuous_scale='Viridis')
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico de categorias - CADA CATEGORIA COM UMA COR DIFERENTE
st.subheader("Categorias que mais vendem")
top_categorias = vendas_filtradas.groupby('categoria')['preco_total'].sum().sort_values(ascending=False).head(10).reset_index()

# Paleta de cores personalizada
cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7B05E', '#B56576', '#6C91B2']

fig3 = px.bar(top_categorias, 
              x='preco_total', 
              y='categoria', 
              orientation='h',
              title="Top Categorias por Faturamento",
              color='categoria',
              color_discrete_sequence=cores,
              text='preco_total')
fig3.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
fig3.update_layout(height=450, showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

# Gráfico de status - cores diferentes
st.subheader("Distribuição por Status")
status_count = vendas_filtradas['status_pedido'].value_counts().reset_index()
status_count.columns = ['status', 'quantidade']

cores_status = {'Entregue': '#2ECC71', 'Processando': '#F39C12', 'Cancelado': '#E74C3C'}

fig4 = px.pie(status_count, 
              values='quantidade', 
              names='status',
              title="Pedidos por Status",
              color='status',
              color_discrete_map=cores_status,
              hole=0.4)
fig4.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig4, use_container_width=True)

# Gráfico de métodos de pagamento - colorido
st.subheader("Métodos de Pagamento")
pagamentos = vendas_filtradas['metodo_pagamento'].value_counts().reset_index()
pagamentos.columns = ['metodo', 'quantidade']

fig5 = px.bar(pagamentos, 
              x='metodo', 
              y='quantidade',
              title="Preferência por Método de Pagamento",
              color='metodo',
              color_discrete_sequence=px.colors.qualitative.Set2,
              text='quantidade')
fig5.update_traces(textposition='outside')
st.plotly_chart(fig5, use_container_width=True)

# ========== FILTROS ATIVOS ==========
st.sidebar.markdown("---")
st.sidebar.subheader("Filtros ativos:")
st.sidebar.write(f"Categorias: {len(categoria_selecionada)} selecionadas")
st.sidebar.write(f"Status: {len(status_selecionado)} selecionados")