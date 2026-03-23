# Insights da Sprint 2 - Análise Exploratória de Dados

**Data da Análise:** Março 2026  
**Período dos Dados:** 11/03/2025 a 11/03/2026  
**Total de Pedidos:** 5.500  
**Total de Clientes:** 900


## 1. Panorama Geral do Negócio

### Métricas Principais
| Métrica | Valor |
|---------|-------|
| Faturamento Total (todos pedidos) | R$ 16.293.850,49 |
| Faturamento Realizado (entregues) | R$ 5.549.129,62 |
| **Perda por Cancelamentos** | **R$ 10.744.720,87** |
| Ticket Médio Geral | R$ 2.962,52 |
| Ticket Médio (entregues) | R$ 2.950,10 |
| Total de Itens Vendidos | 15.797 |
| Média de Itens por Pedido | 2,9 |

### Distribuição dos Pedidos
| Status | Quantidade | Percentual |
|--------|------------|------------|
| Entregues | 1.881 | 34,2% |
| Cancelados | 1.783 | 32,4% |
| Outros Status | 1.836 | 33,4% |


## 2. Principais Problemas Identificados

### Taxa de Cancelamento Alta (32,4%)
- **Problema:** 32,4% dos pedidos são cancelados
- **Impacto:** Perda de R$ 10,7 milhões em faturamento
- **Referência:** Mercado saudável tem <10% de cancelamento
- **Conclusão:** O problema não é vender, é entregar

### Outliers Identificados
- **Quantidade:** X pedidos identificados como outliers
- **Característica:** Valores muito acima ou abaixo do padrão
- **Recomendação:** Investigar se são erros, fraudes ou clientes especiais


## 3. Análise de Correlação

### Relação: Quantidade x Valor do Pedido
- **Correlação encontrada:** 0,85 (Forte Positiva)
- **Significado:** Clientes que compram mais itens gastam significativamente mais
- **Oportunidade:** Incentivar compra de múltiplos itens

### Estratégias sugeridas:
- Criar combos e promoções "leve mais, pague menos"
- Oferecer frete grátis acima de X itens
- Implementar sistema de upsell no carrinho


## 4. Segmentação RFM de Clientes

### Distribuição dos Segmentos
| Segmento | Clientes | Percentual | Ticket Médio |
|----------|----------|------------|--------------|
| Campeão | X | X% | R$ X |
| Leal | X | X% | R$ X |
| Novo | X | X% | R$ X |
| Em risco | X | X% | R$ X |
| Perdido | X | X% | R$ X |
| Potencial | X | X% | R$ X |

### Principais Descobertas
- **Campeões (X%):** Clientes VIP que merecem atenção especial
- **Em risco (X%):** Clientes que pararam de comprar - PRIORIDADE DE RECUPERAÇÃO
- **Perdidos (X%):** Clientes inativos há muito tempo


## 5. Recomendações Estratégicas

### Prioridade 1: Reduzir Cancelamentos
| Ação | Responsável | Impacto Esperado |
|------|-------------|------------------|
| Investigar causas dos 32% de cancelamento | Operações/Logística | Reduzir para <15% |
| Revisar política de estoque | Estoque | Diminuir cancelamentos por falta |
| Analisar fraudes | Segurança | Reduzir cancelamentos suspeitos |
| Acompanhar pedidos com problemas | Atendimento | Melhorar experiência |

### Prioridade 2: Recuperar Clientes "Em Risco"
- **Objetivo:** Reativar clientes que pararam de comprar
- **Ação:** Enviar cupom de desconto personalizado (30% OFF)
- **Público:** Clientes que gastaram mais e estão há mais de 60 dias sem comprar

### Prioridade 3: Fidelizar Clientes "Campeões"
- **Objetivo:** Manter os melhores clientes
- **Ação:** Criar programa de benefícios exclusivos
- **Benefícios:** Frete grátis, descontos especiais, atendimento prioritário

### Prioridade 4: Aumentar Ticket Médio
- **Objetivo:** Aumentar valor por pedido
- **Estratégia:** Aproveitar correlação positiva (mais itens = mais valor)
- **Táticas:** Combos, upsell, frete grátis progressivo


## 6. Top Clientes

### Top 5 Clientes que Mais Gastaram
| Cliente | Total Gasto | Pedidos |
|---------|-------------|---------|
| [Nome] | R$ X | X |
| [Nome] | R$ X | X |
| [Nome] | R$ X | X |
| [Nome] | R$ X | X |
| [Nome] | R$ X | X |

### Top 5 Produtos Mais Vendidos
| Produto | Categoria | Quantidade Vendida | Receita |
|---------|-----------|-------------------|---------|
| [Produto] | [Categoria] | X | R$ X |
| [Produto] | [Categoria] | X | R$ X |
| [Produto] | [Categoria] | X | R$ X |
| [Produto] | [Categoria] | X | R$ X |
| [Produto] | [Categoria] | X | R$ X |


## 7. Arquivos Gerados na Sprint 2

| Arquivo | Descrição |
|---------|-----------|
| `estatisticas_descritivas.txt` | Métricas gerais do negócio |
| `analise_outliers.png` | Gráficos de outliers |
| `analise_correlacao.png` | Matriz de correlação e scatter plot |
| `distribuicao_segmentos.png` | Distribuição dos segmentos RFM |
| `analise_rfm_completa.csv` | Classificação de todos os clientes |
| `clientes_em_risco.csv` | Lista de clientes para recuperação |
| `clientes_campeoes.csv` | Lista de clientes VIP |
| `top_10_clientes.csv` | Clientes que mais gastaram |
| `ranking_produtos.csv` | Produtos mais vendidos |


## 8. Próximos Passos (Sprint 3)

1. **Criar Dashboard** no Power BI/Tableau com os KPIs identificados
2. **Monitorar** a evolução da taxa de cancelamento
3. **Implementar** campanha de recuperação para clientes "Em risco"
4. **Desenvolver** programa de fidelidade para clientes "Campeões"


**Data da Entrega:** Março 2026  
**Responsável:** Ana Laura Dos Santos Franco