# - Geração do dataset simulado (ecom-data.csv com +5000 linhas).
# Esse código vai gerar mais de 5000 linhas com erros propositais 
# Documentações utilizadas:
# Faker: https://fakerjs.dev/guide/

# Importando bibliotecas 
import pandas as pd # Manipulação de dados(tabelas)
from faker import Faker # Gerador de dados falsos
import numpy as np  # Para operações numéricas
import random       # Gera números aleatórios 
from datetime import datetime, timedelta # Datas e contas com datas (importar a classe datetime e timedelta da biblioteca datetime)

# criar a pasta dados se ainda não existir (para evitar erro no código)
import os  # Interage com o sistema operacional

if not os.path.exists('dados'):
    os.makedirs('dados')
    print("Pasta 'dados' criada!")

fake = Faker('pt_BR')   # Criar um objeto fake e colocar o idioma em português 
random.seed(42)         # Geralmente quando o faker gera dados falsos, eles mudam toda a vez que executa o código, então essa linha vai fixar a sequência aleatória e fazer o Faker gerar os mesmos dados na mesma ordem toda vez
np.random.seed(42)      # Parecido com random.seed() mas para números

# Listas de dados que vão ser sorteados aleatoriamente
categorias = ['Eletrônicos', 'Roupas', 'Calçados', 'Livros', 'Casa e Decoração', 'Esportes', 'Beleza'] # Lista com 7 categorias 

produtos = {
    'Eletrônicos': ['Smartphone', 'Notebook', 'Fone de ouvido', 'Tablet', 'Carregador', 'Smartwatch', 'Monitor', 
                    'Caixa de som', 'Câmera digital', 'SSD', 'Mouse gamer', 'Webcam', 'Smart TV', 'Roteador Wi-Fi',
                     'Adaptador USB', 'Controle de videogame', 'HD externo'],
    'Roupas': ['Camiseta', 'Calça Jeans', 'Vestido', 'Blusa', 'Jaqueta', 'Moletom','Camisa social', 'Vestido', 
               "Calça de moletom", 'Saia', 'Shorts', 'Blusa de frio', 'Regata', 'Pijama', 'Roupa íntima', 'Meias', 
               'Casaco', 'Bikinis'],
    'Calçados': ['Tênis esportivo', 'Tênis casual', 'Bota', 'Sandália', 'Chinelo', 'Sapato social', 'Sapatilha', 'Scarpin',
                 'Tênis de corrida', 'Tênis de academia', 'Coturno'],
    'Livros': ['Livros de romance', 'Livros de ficção científica', 'Livros de fantasia', 'Livros de programação',
               'Livros de distopia', 'Livros de negócios', 'Livros de desenvolvimento pessoal', 'Mangás',
               'Livros de histórias', 'Livros infantis', 'Livros de mistério', 'Livros de drama', 'Histórias em quadrinho'],
    'Casa e Decoração': ['Luminária', 'Abajur', 'Quadro decorativo', 'Espelho decorativo', 'Almofada', 'Tapete', 'Cortina',
                         'Vaso de planta', 'Planta artificial', 'Porta-retratos', 'Velas aromáticas', 'Relógio de parede',
                         'Organizador de mesa', 'Estante', 'Prateleira'],
    'Esportes': ['Bola de futebol', 'Bola de basquete', 'Bola de vôlei', 'Halteres', 'Corda de pular', 'Tapete de yoga',
                 'Faixa elástica de treino', 'Luvas de academia', 'Garrafa térmica esportiva', 'Skate', 'Luvas de academia',
                 'Mochila esportiva', 'Raquete de tênis', 'Capacete para ciclismo'],
    'Beleza': ['Shampoo', 'Condicionador', 'Creme hidratante', 'Protetor solar', 'Perfume', 'Desodorante', 'Base de maquiagem',
               'Batom', 'Gloss', 'Lipliner', 'Máscara de cílios', 'Extensão de cílios', 'Paleta de maquiagem', 'Esmalte',
               'Removedor de esmalte', 'Removedor de maquiagem', 'Óleo de cabelo', 'Escova de cabelo', 'Secador de cabelo']
}

metodos_pagamento = ['Cartão de crédito', 'Boleto', 'Pix', 'Cartão de Débito', 'Transferência']
status = ['Entregue', 'Processando', 'Cancelado']

print('Gerando +5000 pedidos...') 
dados = []  # Lista "dados" vazia que vai receber os pedidos gerados

# Gerar +5000 pedidos
for i in range(5500):
    # Margem de erro dos dados
    erro = random.random() <0.05 # A variável erro terá 5% de chance de ser verdadeira então aproximadamente 5% dos dados virão com erro
    
    # Dados do pedido
    id_pedido = f"PEDIDO-{i+1000}" # Quando i = 0 -> PEDIDO-1000, i = 999 -> PEDIDO-1999, etc...
    # Gerar data
    data_pedido = fake.date_between(start_date='-1y', end_date='today') # Gera uma data aleatória entre um ano atrás e hoje
    
    # Dados do cliente
    id_cliente = f"CLIENTE-{random.randint(100,999)}"  # Gera número aleatório entre 100-999
    # Lógica: Se tiver erro, pode vir nulo em alguns desses campos
    nome_cliente = fake.name() if not erro or random.random() > 0.3 else None  # Gera um nome falso e na maioria das vezes vai vir com nome mas em alguns casos com erro não vem nada
    email_cliente = fake.email() if not erro or random.random() > 0.3 else None
    cidade_cliente = fake.city() if not erro or random.random() > 0.3 else None
    estado_cliente = fake.estado_sigla() if not erro or random.random() > 0.3 else None

    categoria = random.choice(categorias) # Escolhe uma categoria da lista de categorias
    id_produto = f"PRODUTO-{random.randint(1000, 9999)}"
    nome_produto = random.choice(produtos[categoria])  # Pega a lista de produtos dentro da categoria escolhida e sorteia um

    # Dados da venda
    quantidade = random.randint(1, 5) if not erro else random.choice([0, -1, None])  # Se não tiver erro gera uma quantidade entre 1 e 5, mas se tiver erro gera um valor errado ex: 0, -1, ou nenhum valor
    if quantidade is None:  # Prevenir erro na linha 78 do código
        quantidade = 1
    preco_unitario = round(random.uniform(50, 2000), 2)  # Gera um número decimal entre 50 e 2000 e arredonda para duas casas decimais 
    
    if erro and random.random() < 0.3: # 1.5% (5% * 30%) dos pedidos virão com erro
        preco_total = preco_unitario * quantidade + 100  # Soma 100 a mais no total (para dar inconsistência)
    else: 
        preco_total = preco_unitario * quantidade if quantidade and quantidade > 0 else preco_unitario  # se a quantidade é maior que 0, calcula total correto mas se for inválido usa só o preço unitário

    # Finalizar o pedido
    # Escolhe método e status aleatórios da lista
    metodo_pagamento = random.choice(metodos_pagamento)
    status_pedido = random.choice(status)

    # Adiciona uma nova linha na lista "dados"
    dados.append([
        id_pedido, data_pedido, id_cliente, nome_cliente, email_cliente, cidade_cliente, estado_cliente, id_produto,
        nome_produto, categoria, quantidade, preco_unitario, preco_total, metodo_pagamento, status_pedido
    ])

# Criar lista com os nomes das colunas para dar nome para cada campo
colunas = ['id_pedido', 'data_pedido', 'id_cliente', 'nome_cliente', 'email_cliente', 'cidade_cliente', 'estado_cliente', 
           'id_produto', 'nome_produto', 'categoria', 'quantidade', 'preco_unitario', 'preco_total', 'metodo_pagamento', 
           'status_pedido']

# Criar planilha do pandas. "dados" = linhas da tabela e a "coluna" o cabeçalho 
df = pd.DataFrame(dados , columns=colunas)

# Criar lista de 0 a 5499 e escolher 50 números dessa lista aleatoriamente
dup_indices = random.sample(range(5500), 50)

# Seleciona os 50 pedidos que vão ser duplicados e faz uma cópia
df_duplicatas = df.iloc[dup_indices].copy()

# Junta o Dataframe original com as duplicatas (agora tem 5550 linhas) e renumera os índices de 0 até 5549 para evitar índices repitidos
df = pd.concat([df, df_duplicatas], ignore_index=True)

# Mostra na tela quantas linhas tem o dataframe
print(f"Dataset gerado com {len(df)} linhas")

# Salve como arquivo csv (excel), cria a pasta dados e o arquivo dentro dela e index = false para não salvar os números nas linhas (senão ficaria uma coluna extra)
df.to_csv('dados/ecom_data_bruto.csv', index=False)


print(f"Total de linhas: {len(df)}")
print(f"Colunas: {list(df.columns)}")  # Mostra as colunas
print(f"Valores nulos: {df.isnull().sum().sum()}")  # Conta os nulos por coluna e soma eles todos
print(f"Duplicatas (id_pedido): {df.duplicated('id_pedido').sum()}")  # Conta quantos ids de pedidos estão duplicados