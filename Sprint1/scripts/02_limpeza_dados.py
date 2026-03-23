# - Limpeza dos dados gerados

# Importando as bibliotecas
import pandas as pd  # Para trabalhar com os dados em tabela
import numpy as np  # Para operações numéricas
import sqlite3  # Banco de dados SQLite
import os  # Interage com o sistema operacional, para verificar se algum arquivo existe, etc.
from datetime import datetime  # Trabalhar com data e horas

print("INICIANDO LIMPEZA DOS DADOS")

# Verificar se o arquivo existe
if not os.path.exists('dados/ecom_data_bruto.csv'):
    print("Erro: Arquivo 'dados/ecom_data_bruto.csv' não encontrado!")
    print("Execute primeiro o script '01_gerar_dados.py'")
    exit()  # -> Encerra o script

# Ler o arquivo e carregá-lo em uma tabela 
print("Carregando dados brutos...")
df = pd.read_csv('dados/ecom_data_bruto.csv')
print(f"Linhas carregadas: {len(df)}")

print("\nPROBLEMAS ENCONTRADOS:")
print(f"Linhas totais: {len(df)}")
print(f"Valores nulos:\n{df.isnull().sum()}")  # quando for nulo = True(1) e quando não for é igual a False(0), soma todos os True
print(f"Duplicatas em id_pedido: {df.duplicated('id_pedido').sum()}")  # Verifica em cada linha o valor na coluna id_pedido já apareceu antes e retorna True ou False, soma os True

# Remover as duplicatas (pandas)
# Pega a coluna 'id_pedido', mantem só a primeira ocorrência das duplicatas e deleta as outras 
df = df.drop_duplicates(subset=['id_pedido'], keep='first')
print(f"\nQuantidade de linhas depois da remoção das duplicatas: {len(df)} linhas")

# Tratar os valores nulos
# Remover todas as linhas de valores nulos na coluna de 'id_pedido'
df = df.dropna(subset=['id_pedido'])
print(f"Após dropna em id_pedido: {len(df)} linhas")

# A função fillna preenche os valores nulos de uma coluna com o valor que damos para eles (Nesse caso, None por texto padrão) 
df['nome_cliente'] = df['nome_cliente'].fillna('Cliente não informado')
df['email_cliente'] = df['email_cliente'].fillna('email@naoinformado.com')
df['cidade_cliente'] = df['cidade_cliente'].fillna('Cidade não informada')
df['estado_cliente'] = df['estado_cliente'].fillna('XX')

df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')  # converte os valores da quantidade para números e se não puder ser convertido transforma em nulo
print(f"Após converter quantidade: {len(df)} linhas")
df['quantidade'] = df['quantidade'].fillna(1)  # Depois de converter os valores inválidos/nulos vão ser preenchidos com 1
df.loc[df['quantidade'] <= 0, 'quantidade'] = 1  # Atribui o valor 1 para as quantidades que são menores ou iguais a 0, para não ter 0 e nem quantidades negativas

# Como na quantidade, converte os valores dos preços para números e se não puder ser convertido transforma em nulo
df['preco_unitario'] = pd.to_numeric(df['preco_unitario'], errors='coerce')
df['preco_total'] = pd.to_numeric(df['preco_total'], errors='coerce')
print(f"Após converter preço: {len(df)} linhas")

print("n\\Corrigindo preço total...")
df['preco_total_calculado'] = df['quantidade'] * df['preco_unitario']  # Calcular o preço total correto
df['preco_total'] = df['preco_total_calculado']  # Substituir os valores da coluna preco_total antiga para os valores da nova com o calculo correto do preço total 
df = df.drop(columns=['preco_total_calculado'])  # Apagar a coluna preco_total_calculado porque não precisamos mais dela, já que os valores dela já foram substituídos na coluna preco_total
print(f"Após corrigir preços: {len(df)} linhas")

print("\nApós tratar os valores nulos:")
print(f"Nulos restantes:\n{df.isnull().sum()}")
print(f"Total de linhas agora: {len(df)}")

# Padronizar as datas
print("\nPadronizando datas...")
df['data_pedido'] = pd.to_datetime(df['data_pedido'], errors='coerce')  # Converter a coluna da data do pedido e se for inválida, transforma em nula
print(f"Após converter datas: {len(df)} linhas")

# Se alguma não tiver convertido, vai preencher com datas aleatórias
datas_nulas = df['data_pedido'].isnull().sum()  # Contar quantas datas são inválidas
if datas_nulas > 0:  # Se datas nulas for maior que 0/ se elas existirem:
    print("Corrigindo {datas_nulas} datas inválidas...") 
    datas_validas = df['data_pedido'].dropna()  # O dropna() pega a coluna data_pedido no dataframe original, cria uma cópia removendo os valores nulos e guarda a copia na varivél datas_validas
    if len(datas_validas) > 0:  # Verifica se tem datas validas no dataframe e se sim usa elas como referência para:
        data_min = datas_validas.min()  # Encontrar a data mais antiga
        data_max = datas_validas.max()  # Encontrar a data mais recente
        datas_aleatorias = pd.date_range(start=data_min, end=data_max, periods=datas_nulas)  # Gerar uma sequência de datas, entre a data mais antiga e a mais recente, pega as datas inválidas
        df.loc[df['data_pedido'].isnull(), 'data_pedido'] = datas_aleatorias  # e substitui as datas nulas dentro da quantidade de datas inválidas. Ex: Se no period der 3 datas inválidas, vai gerar 3 novas datas válidas
    else:
        df['data_pedido'] = pd.date_range(start='2024-01-01', periods=len(df))  # Se não tiver nenhuma data válida no dataframe, criamos um intervalo de datas que começa em 2024-01-01 com o mesmo número de linhas que tem no dataframe
print(f"Após corrigir datas: {len(df)} linhas")

# Extrair o ano, mês e dia da semana
df['ano'] = df['data_pedido'].dt.year
df['mes'] = df['data_pedido'].dt.month
df['dia_semana'] = df['data_pedido'].dt.day_name()

# Padronização dos textos
# .str.title() -> Faz a primeira letra de cada palavra começar maiúscula e o resto minúscula
# .str.upper() -> Converte todas as letras para maiúscula
# .str[:2] -> Pega só os dois primeiros caracteres da string, para ficar com duas letras nos estados
print("\nPadronizando textos...")
df['cidade_cliente'] = df['cidade_cliente'].str.title()
df['estado_cliente'] = df['estado_cliente'].str.upper().str[:2]
df['categoria'] = df['categoria'].str.title()
df['metodo_pagamento'] = df['metodo_pagamento'].str.title()
df['status_pedido'] = df['status_pedido'].str.title()
print(f"Após padronizar textos: {len(df)} linhas")

# Remover espaços extras (para evitar erros como: "São Paulo" != "São Paulo ")
for col in df.select_dtypes(include=['object', 'string']).columns:  # Selecionar todas as colunas do dataframe que são do tipo 'object' (de texto), pegar os nomes dessas colunas, iterar sobre cada uma dessas colunas de texto
    df[col] = df[col].str.strip()  # Remove os espaços em branco (.strip()) extras, no início e no final de cada string 
print(f"Após strip: {len(df)} linhas")

# Resumo final do dataframe limpo
print("\nDADOS LIMPOS COM SUCESSO!")
print(f"Total final: {len(df)} linhas")
print(f"Colunas: {list(df.columns)}")
print(f"Período: {df['data_pedido'].min()} até {df['data_pedido'].max()}")

# Salvar o CSV limpo
# index = False para remover a coluna que mostra os índices da tabela
df.to_csv('dados/ecom_data_limpo.csv', index=False)
print("\nDados salvos em: dados/ecom_data_limpo.csv")

# .nunique -> Conta quantos valores únicos tem
# .sum() -> Soma os valores da coluna
# .mean() -> Calcula a média
print("\nESTATÍSTICAS FINAIS:")
print(f"Total de pedidos: {len(df)}")
print(f"Total de clientes únicos: {df['id_cliente'].nunique()}")
print(f"Total de produtos únicos: {df['nome_produto'].nunique()}")
print(f"Categorias: {df['categoria'].nunique()}")
print(f"Valor total vendido: R$ {df['preco_total'].sum():,.2f}")
print(f"Média por pedido: {df['preco_total'].mean():,.2f}")
print(f"Pedido mais caro: {df['preco_total'].max():,.2f}")
print(f"Pedido mais barato: {df['preco_total'].min():,.2f}")

# .head() -> Pega as primeiras 5 linhas do resultado
print("\nPrimeiras 5 linhas dos dados limpos:")
print(df[['id_pedido', 'data_pedido', 'nome_cliente', 'preco_total']].head())