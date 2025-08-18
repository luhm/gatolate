# import streamlit as st

# # Títulos das abas
# tab1, tab2 = st.tabs(["Aba 1", "Aba 2"])

# # Conteúdo da aba 1
# with tab1:
#     st.header("Conteúdo da Aba 1")
#     st.write("Aqui você pode colocar qualquer conteúdo, como textos, gráficos, imagens, etc.")
#     # Exemplo:
#     st.line_chart([1, 5, 2, 6, 3, 7])


# # Conteúdo da aba 2
# with tab2:
#     st.header("Conteúdo da Aba 2")
#     st.write("Outro conteúdo diferente na segunda aba.")
#     # Exemplo:
#     st.bar_chart([1, 5, 2, 6, 3, 7])

import streamlit as st
import pandas as pd

# Dados de exemplo (substitua com seus próprios dados)
data = {'Categoria': ['A', 'A', 'B', 'B', 'C', 'C'],
        'Valor': [10, 20, 15, 25, 22, 18],
        'Data': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06'])}
df = pd.DataFrame(data)

# Título do dashboard
st.title('Dashboard Interativo com Duas Abas')

# Criação das abas
tab1, tab2 = st.tabs(["Aba 1", "Aba 2"])

# Filtros
with st.sidebar:
    st.header("Filtros")
    categoria_selecionada = st.selectbox("Selecione a Categoria:", options=['Todas'] + list(df['Categoria'].unique()))
    data_inicio = st.date_input("Data Início:", value=df['Data'].min())
    data_fim = st.date_input("Data Fim:", value=df['Data'].max())

# Função para aplicar os filtros
def aplicar_filtros(dataframe, categoria, inicio, fim):
    if categoria != 'Todas':
        dataframe = dataframe[dataframe['Categoria'] == categoria]
    dataframe = dataframe[(dataframe['Data'] >= pd.to_datetime(inicio)) & (dataframe['Data'] <= pd.to_datetime(fim))]
    return dataframe

# Aplica os filtros aos dados
df_filtrado = aplicar_filtros(df.copy(), categoria_selecionada, data_inicio, data_fim)

# Conteúdo da Aba 1
with tab1:
    st.header("Gráfico na Aba 1")
    st.line_chart(df_filtrado.set_index('Data')[['Valor']])
    st.write("Tabela:")
    st.dataframe(df_filtrado)

# Conteúdo da Aba 2
with tab2:
    st.header("Gráfico na Aba 2")
    st.bar_chart(df_filtrado.set_index('Data')[['Valor']])
    st.write("Tabela:")
    st.dataframe(df_filtrado)
    