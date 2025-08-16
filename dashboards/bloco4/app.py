import streamlit as st ##serve para criar aplicações
import pandas as pd
import numpy as np
import plotly.express as px


# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Venda de chocolate por país", ## cria o titulo da pagina, que fica na barrinha la em cima
    page_icon="🍫",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/luhm/gatolate/refs/heads/main/data/chocolate_sales_cleaned.csv")


# --- Barra Lateral (criação de filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
paises_disponiveis = sorted(df['Country'].unique())
paises_selecionados = st.sidebar.multiselect("Países", paises_disponiveis, default=paises_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['Country'].isin(paises_selecionados))
]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise Geográfica das vendas da Gatolate") ## cria o titulo do dash
st.markdown("Explore os dados das vendas de chacolates da Gatolate na perspectiva geográfica nos primeiros 3 trimestres de 2022. Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais (Vendas gerais)")

if not df_filtrado.empty:
    total_vendas = df_filtrado['Boxes Shipped'].sum()
    pais_compra_mais = df_filtrado['Country'].mode()[0]
    chocolate_mais_vendido = df_filtrado['Product'].max()
    valor_total_arrecadado = df_filtrado["Amount"].sum()
else:
    total_vendas, media_de_vendas, chocolate_mais_vendido, valor_total_arrecadado = 0, 0, 0, ""

col1, col2 = st.columns(2) ## divide as informações em colunas na página
col1.metric("Total de Vendas", f"${total_vendas:,.0f}")
col2.metric("País que mais compra", pais_compra_mais)

col3, col4 = st.columns(2)
col3.metric("Valor total arrecadad (em USD)", valor_total_arrecadado)
col4.metric("Chocolate mais vendido", chocolate_mais_vendido)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")


if not df_filtrado.empty:
    country_sales = df_filtrado.groupby('Country_iso3')['Amount'].sum().sort_values(ascending=True).reset_index()
    grafico_paises = px.choropleth(country_sales,
                locations='Country_iso3',
                color='Amount',
                hover_name='Country_iso3',
                color_continuous_scale='rdylgn',
                title='Onde estamos vendendo mais? (valores absolutos)') # Added a color scale
    grafico_paises.update_layout(title_x=0.1)
    st.plotly_chart(grafico_paises, use_container_width=True)
else:
    st.warning("Nenhum dado para exibir no gráfico de países.")        

col_graf2, col_graf3 = st.columns(2)


with col_graf2:
    if not df_filtrado.empty:
        grafico_receita_pais = px.bar(country_sales,
                    x='Amount',
                    y='Country_iso3',
                    orientation='h',
                    title='Receita por país (USD)',
                    color='Amount',
                    color_continuous_scale='rdylgn') 
        grafico_receita_pais.update_layout(title_x=0.1)
        st.plotly_chart(grafico_receita_pais, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

with col_graf3:
    if not df_filtrado.empty:
        country_mean = df.groupby('Country')['Amount'].mean().sort_values(ascending=True).reset_index()
        ticket_medio = px.bar(
            country_mean,
             x='Amount',
             y='Country',
             title='Ticket Médio por país (USD)',
             color='Amount',
             color_continuous_scale='rdylgn')
        st.plotly_chart(ticket_medio, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

  

