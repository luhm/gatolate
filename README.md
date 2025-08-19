# Gatolate

Gatolate é uma loja (fictícia) de venda de chocolates. O CEO, Willy Wonka, solicitou à área de dados que providenciasse uma visão geral aprofundada da situação da empresa.

Após uma conversa extensa, foram definidos alguns [blocos e KPIs](https://github.com/luhm/gatolate/blob/main/informacoes_gerais/kpis.md) de essenciais da análise.

No decorrer do processo de análise e conversas da equipe com Willy Wonka, ficou decidido uma mudança na estrutura do dashboard. Assim, um mesmo dash poderia mostrar diferentes abas com os gráficos necessários para compreensão e tomada de decisões de negócio. Nesse momento, foi construído um novo documento com [blocos e KPIs]()

Para que toda a equipe tenha acesso e acompanhe o desenvolvimento desse projeto, este repositório foi criado com a seguinte estrutura:

- Na pasta `data` é possível encontrar os dados em formato csv puro e já limpo.
- Na pasta `análises` é possível encontrar os códigos utilizados nas análises e os relatórios finais.
- Na pasta `dashboards` é possível encontrar o código completo do deploy do dashboard no streamlit.
- Na pasta `informacoes_gerais` é possível ver o documentos construídos durante as conversas com stakeholders.
---
Anteriormente, faríamos um dashboard para cada bloco; na nova estrutura, será um dashboard com as seguintes abas:

- Metricas gerais
- Onde vendemos e ganhamos mais
- Análises Temporais
- Análises por vendedor
- Análises por produto


## EDA

O documento `.ypinb` demonstra as ações descritas abaixo.

- exploração inicial com métodos como `head()`, `info()` e `describe()`
- identificação de dados ausentes com `isnull()`
- identificação de outliers com `boxplot`
- exploração de colunas específicas, com métodos como `value_counts()`, `unique()`
- limpeza dos dados: troca de tipos com `astype()` e `to_datetime()`, ajuste de caracteres das células com `replace()`

