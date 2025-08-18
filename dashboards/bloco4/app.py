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

df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)

# --- Criação das abas ---

tab1, tab2, tab3, tab4 = st.tabs(["Metricas gerais", "Onde vendemos e ganhamos mais", "Análises Trimestrais", "Análises por vendedor"])

warning = "Nenhum dado para exibir no gráfico de países."

# --- Barra Lateral (criação de filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
paises_disponiveis = sorted(df['Country'].unique())
paises_selecionados = st.sidebar.multiselect("Países", paises_disponiveis, default=paises_disponiveis)

vendedores_disponiveis = sorted(df['Sales Person'].unique())
vendedores_selecionados = st.sidebar.multiselect("Vendedores", vendedores_disponiveis, default=vendedores_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['Country'].isin(paises_selecionados)) &
    (df['Sales Person'].isin(vendedores_selecionados))
]

# --- Conteúdo Principal ---

with tab1:
    st.title("🎲 Dashboard de Análise Geográfica das vendas da Gatolate") ## cria o titulo do dash
    st.markdown("Explore os dados das vendas de chacolates da Gatolate na perspectiva geográfica nos primeiros 3 trimestres de 2022. Utilize os filtros à esquerda para refinar sua análise.")

    # --- Métricas Principais (KPIs) ---
    st.subheader("Métricas gerais")

    if not df_filtrado.empty:
        qnt_vendas = df_filtrado['Boxes Shipped'].sum()
        pais_compra_mais = df_filtrado['Country'].mode()[0]
        chocolate_mais_vendido = df_filtrado['Product'].max()
        valor_total_arrecadado = df_filtrado['Amount'].sum()
        pessoa_vende_mais = df_filtrado['Sales Person'].max()
        ticket_medio_total = df_filtrado['Amount'].mean()
    else:
        qnt_vendas, pais_compra_mais, chocolate_mais_vendido, valor_total_arrecadado = 0, 0, 0, ""

    col1, col2 = st.columns(2) ## divide as informações em colunas na página
    col1.metric("Quantidade total de caixas vendidas", qnt_vendas)
    col2.metric("País que mais compra", pais_compra_mais)

    col3, col4 = st.columns(2)
    col3.metric("Valor total arrecadado (em USD)", f"${valor_total_arrecadado:,.0f}")
    col4.metric("Chocolate mais vendido", chocolate_mais_vendido)
    
    col5, col6 = st.columns(2)
    col5.metric("Ticket médio (USD)", f"${ticket_medio_total:,.0f}")
    col6.metric("Top vendedor", pessoa_vende_mais)

# st.markdown("---")

# --- Análises Visuais com Plotly ---

with tab2:

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
        st.write(warning)        

    col_graf2, col_graf3 = st.columns(2)


    with col_graf2:
        if not df_filtrado.empty:
            receita_pais = df.groupby('Country')['Amount'].sum().sort_values(ascending=True).reset_index()
            grafico_receita_pais = px.bar(
                  receita_pais,
                  x='Amount',
                  y='Country',
                  # orientation='h',
                  title='Receita por país (USD)',
                  labels={'Amount': 'USD', 'Country': 'País'},
                  color='Amount',
                  color_continuous_scale='rdylgn') 
            grafico_receita_pais.update_layout(title_x=0.1)
            st.plotly_chart(grafico_receita_pais, use_container_width=True)
        else:
            st.write(warning)

    with col_graf3:
        if not df_filtrado.empty:
            country_mean = df.groupby('Country')['Amount'].mean().sort_values(ascending=True).reset_index()
            ticket_medio = px.bar(
                country_mean,
                 x='Amount',
                 y='Country',
                 title='Ticket Médio por país (USD)',
                 labels={'Amount': 'USD', 'Country': 'País'},
                 color='Amount',
                 color_continuous_scale='rdylgn')
            st.plotly_chart(ticket_medio, use_container_width=True)
        else:
            st.write(warning)

    col_graf4, col_graf5 = st.columns(2)

    with col_graf4:
        if not df_filtrado.empty:
            product_qnt = df_filtrado.groupby('Product')['Boxes Shipped'].sum().sort_values(ascending=False).head(5).reset_index()
            qnt_por_pais = px.bar(product_qnt,
                 x='Product',
                 y='Boxes Shipped',
                 title='Top 5 Produtos mais vendidos',
                 labels={'Product': 'Produto', 'Boxes Shipped': 'Caixas'},
                 color='Boxes Shipped',
                 color_continuous_scale='Greens')
            st.plotly_chart(qnt_por_pais, use_container_width=True)
        else:
            st.write(warning)
     
    with col_graf5:
        if not df_filtrado.empty:
            product_amount = df_filtrado.groupby('Product')['Amount'].sum().sort_values(ascending=False).head(5).reset_index()
            amount_por_pais = px.bar(
                product_amount,
                 x='Product',
                 y='Amount',
                 title='Top 5 Produtos que geram mais receita (USD)',
                 labels={'Amount': 'USD', 'Product': 'Produto'},
                 color='Amount',
                 color_continuous_scale='Greens')
            st.plotly_chart(amount_por_pais, use_container_width=True)
        else:
            st.write(warning)

with tab3:
    st.subheader("Análises por trimestre")

    col_graf6, col_graf7 = st.columns(2)

    with col_graf6:
        if not df_filtrado.empty:
            df_filtrado['Quarter'] = df_filtrado['Date'].dt.quarter
            receita_trimestral = df_filtrado.groupby('Quarter')['Amount'].sum().reset_index()
            receita_trimestral_total = px.bar(receita_trimestral,
                 x='Quarter',
                 y='Amount',
                 title='Receita geral por trimestre',
                 color='Amount',
                 color_continuous_scale='Blues',
                 labels={'Quarter': 'Trimestre', 'Amount': 'USD'})
            receita_trimestral_total.update_xaxes(tickvals=receita_trimestral['Quarter'])
            st.plotly_chart(receita_trimestral_total, use_container_width=True)
        else:
            st.write(warning)
    
    with col_graf7:
        if not df_filtrado.empty:
            df_filtrado['Quarter'] = df_filtrado['Date'].dt.quarter
            qnt_caixas_trimestral = df_filtrado.groupby('Quarter')['Boxes Shipped'].sum().reset_index()
            caixas_trimestral_total = px.bar(qnt_caixas_trimestral,
                 x='Quarter',
                 y='Boxes Shipped',
                 title='Quantidade de caixas vendidas (por trimestre)',
                 color='Boxes Shipped',
                 color_continuous_scale='Blues',
                 labels={'Quarter': 'Trimestre'})
            caixas_trimestral_total.update_xaxes(tickvals=qnt_caixas_trimestral['Quarter'])
            st.plotly_chart(caixas_trimestral_total, use_container_width=True)
        else:
            st.write(warning)

    
    if not df_filtrado.empty:
        df_filtrado['Quarter'] = df_filtrado['Date'].dt.quarter
        receita_trimestral_pais = df_filtrado.groupby(['Country', 'Quarter'])['Amount'].sum().reset_index()
        receita_trim_fixa = px.bar(receita_trimestral_pais,
             x='Amount',
             y='Quarter',
             color='Country',
             orientation='h',
             title='Receita por trimestre e por país',
             labels={'Quarter': 'Trimestre', 'Amount': 'Receita'})
        receita_trim_fixa.update_yaxes(tickvals=receita_trimestral_pais['Quarter'].unique())
        st.plotly_chart(receita_trim_fixa, use_container_width=True)
    else:
        st.write(warning)

with tab4:
    col_graf8, col_graf9 = st.columns(2)
    
    with col_graf8:
        if not df_filtrado.empty:
            receita_vendedor = df_filtrado.groupby('Sales Person')['Amount'].sum().sort_values(ascending=False).head(5).reset_index()
            top_receita_vendedor = px.bar(
                receita_vendedor,
                 x='Sales Person',
                 y='Amount',
                 title='Top 5 vendedores que geram mais receita (USD)',
                 labels={'Amount': 'USD', 'Vendedor': 'Produto'},
                 color='Amount',
                 color_continuous_scale='reds')
            st.plotly_chart(top_receita_vendedor, use_container_width=True)
        else:
            st.write(warning)
    
    with col_graf9:
        if not df_filtrado.empty:
            caixas_vendedor = df_filtrado.groupby('Sales Person')['Boxes Shipped'].sum().sort_values(ascending=False).head(5).reset_index()
            top_caixas_vendedor = px.bar(
                caixas_vendedor,
                 x='Sales Person',
                 y='Boxes Shipped',
                 title='Top 5 vendedores que venderam mais produtos',
                 labels={'Boxes Shipped': 'USD', 'Vendedor': 'Produto'},
                 color='Boxes Shipped',
                 color_continuous_scale='reds')
            st.plotly_chart(top_caixas_vendedor, use_container_width=True)
        else:
            st.write(warning)
            
    
    





