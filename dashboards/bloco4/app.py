import streamlit as st ##serve para criar aplicações
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression


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
df['Month_Year'] = df['Date'].dt.to_period('M')
df['Quarter'] = df['Date'].dt.quarter

# --- Criação das abas ---

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Metricas gerais", "Onde vendemos e ganhamos mais", "Análises Temporais", "Análises por vendedor", "Análises por produto", "Crescimento"])

warning = "Nenhum dado para exibir no gráfico de países."

# --- Barra Lateral (criação de filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
paises_disponiveis = sorted(df['Country'].unique())
paises_selecionados = st.sidebar.multiselect("Países", paises_disponiveis, default=paises_disponiveis)

vendedores_disponiveis = sorted(df['Sales Person'].unique())
vendedores_selecionados = st.sidebar.multiselect("Vendedores", vendedores_disponiveis, default=vendedores_disponiveis)

meses_disponiveis = sorted(df['Month_Year'].unique())
meses_selecionados = st.sidebar.multiselect("Meses", meses_disponiveis, default=meses_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['Country'].isin(paises_selecionados)) &
    (df['Sales Person'].isin(vendedores_selecionados)) &
    (df['Month_Year'].isin(meses_selecionados))
]

# Varáveis reutilizáveis

receita_trimestral = df_filtrado.groupby('Quarter')['Amount'].sum().reset_index()
meta_receita = 8_000_000

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
                    color_continuous_scale='portland',
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
                  color_continuous_scale='portland') 
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
                 color_continuous_scale='portland')
            st.plotly_chart(ticket_medio, use_container_width=True)
        else:
            st.write(warning)

    
with tab3:
    st.subheader("Análises por trimestre")

    col_graf6, col_graf7 = st.columns(2)

    with col_graf6:
        if not df_filtrado.empty:
            # df_filtrado['Quarter'] = df_filtrado['Date'].dt.quarter
            # receita_trimestral = df_filtrado.groupby('Quarter')['Amount'].sum().reset_index()
            receita_trimestral_total = px.bar(receita_trimestral,
                 x='Quarter',
                 y='Amount',
                 title='Receita geral por trimestre',
                 color='Amount',
                 color_continuous_scale='teal',
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
                 color_continuous_scale='Teal',
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
             color_continuous_scale='Portland',
             orientation='h',
             title='Receita por trimestre e por país',
             labels={'Quarter': 'Trimestre', 'Amount': 'Receita'})
        receita_trim_fixa.update_yaxes(tickvals=receita_trimestral_pais['Quarter'].unique())
        st.plotly_chart(receita_trim_fixa, use_container_width=True)
    else:
        st.write(warning)
    st.markdown("---")
    
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
                 labels={'Amount': 'USD', 'Sales Person': 'Vendedor'},
                 color='Amount',
                 color_continuous_scale='algae')
            st.plotly_chart(top_receita_vendedor, use_container_width=True)
        else:
            st.write(warning)
    
    with col_graf9:
        if not df_filtrado.empty:
            caixas_vendedor = df_filtrado.groupby('Sales Person')['Boxes Shipped'].sum().sort_values(ascending=False).head(5).reset_index()
            principal_vendedor = px.bar(
                caixas_vendedor,
                 x='Sales Person',
                 y='Boxes Shipped',
                 title='Top 5 vendedores com mais caixas vendidas',
                 labels={'Boxes Shipped': 'Caixas', 'Sales Person': 'Vendedor'},
                 color='Boxes Shipped',
                 color_continuous_scale='algae')
            st.plotly_chart(principal_vendedor, use_container_width=True)
        else:
            st.write(warning)
    
    if not df_filtrado.empty:
        salesperson_country_boxes = df_filtrado.groupby(['Sales Person', 'Country'])['Boxes Shipped'].sum().reset_index()
        top_country_by_salesperson = salesperson_country_boxes.loc[salesperson_country_boxes.groupby('Sales Person')['Boxes Shipped'].idxmax()].reset_index(drop=True)
        graf_top_boxes_person = px.bar(top_country_by_salesperson,
            x='Boxes Shipped',
            y='Sales Person',
            color='Country',
            title='País com Maior Número de Caixas Enviadas por Vendedor',
            labels={'Sales Person': 'Vendedor', 'Boxes Shipped': 'Total de Caixas Enviadas', 'Country': 'País'},
            color_discrete_sequence=px.colors.qualitative.Prism)
        # graf_top_boxes_person.update_layout(xaxis={'categoryorder':'total descending'}) # Order bars by total boxes shipped
        st.plotly_chart(graf_top_boxes_person, use_container_width=True)
    else:
        st.write(warning)
   
    if not df_filtrado.empty:
        salesperson_average_amount = df.groupby('Sales Person')['Amount'].mean().sort_values(ascending=False).reset_index()
        ticket_medio_vendedor = px.bar(salesperson_average_amount,
            x='Sales Person',
            y='Amount',
            title='Ticket Médio por Vendedor',
            labels={'Sales Person': 'Vendedor', 'Amount': 'USD'},
            color='Amount',
            color_continuous_scale='bugn') 
        ticket_medio_vendedor.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(ticket_medio_vendedor, use_container_width=True)
    else:
        st.write(warning)

            
with tab5:
    if not df_filtrado.empty:
        caixas_produto_enviadas = df.groupby('Product')['Boxes Shipped'].sum().reset_index()
        valores_produto_enviado = df.groupby('Product')['Amount'].sum().reset_index()
        media_caixa_valor = pd.merge(valores_produto_enviado, caixas_produto_enviadas, on='Product')
        
        media_caixa_valor['Valor_medio_produto'] = media_caixa_valor['Amount'] / media_caixa_valor['Boxes Shipped']
        valor_medio_caixa_produto = px.bar(media_caixa_valor,
             x='Product',
             y='Valor_medio_produto',
             title='Valor Médio por caixa de cada produto',
             labels={'Product': 'Produto', 'Valor_medio_produto': 'USD'},
             color='Valor_medio_produto',
             color_continuous_scale='temps')
        st.plotly_chart(valor_medio_caixa_produto, use_container_width=True)
    else:
        st.write(warning)
    
    col_graf10, col_graf11 = st.columns(2)
    
    if not df_filtrado.empty:
        product_summary = df.groupby('Product').agg({
            'Boxes Shipped': 'sum',
            'Amount': 'sum' }).reset_index()
        fig = px.scatter(product_summary,
                 x='Boxes Shipped',
                 y='Amount',
                 title='Relação entre o total de caixas e a receita total por produto',
                 labels={'Boxes Shipped': 'Total de Caixas Enviadas', 'Amount': 'Valor Total da Venda'},
                 color='Product',
                 color_continuous_scale='Inferno',
                 size='Amount',
                 hover_data=['Product'],
                 color_discrete_sequence=px.colors.qualitative.Pastel) # Show product name on hover

        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
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
                 color_continuous_scale='sunset')
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
                 color_continuous_scale='sunset')
            st.plotly_chart(amount_por_pais, use_container_width=True)
        else:
            st.write(warning)

    if not df_filtrado.empty:
        # df['Month_Year'] = df['Date'].dt.to_period('M')
        monthly_product_sales = df_filtrado.groupby(['Month_Year', 'Product'])['Amount'].sum().reset_index()
        monthly_product_sales['Month_Year'] = monthly_product_sales['Month_Year'].astype(str)
        receita_mensal_produto = px.bar(monthly_product_sales,
              x='Product',
              y='Amount',
              color='Month_Year',
              title='Receita mensal por produto',
              labels={'Product': 'Produto', 'Amount': 'Receita'},
              color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(receita_mensal_produto, use_container_width=True)
    else:
        st.write(warning)
        
with tab6:
    df_filtrado['Year'] = df['Date'].dt.year
    receita_anual = df_filtrado.groupby('Year')['Amount'].sum().reset_index()
    receita_atual = receita_anual['Amount'].sum()
    receita_faltante = meta_receita - receita_atual
    
    
    # Create a DataFrame for plotting
    df_meta_comparacao = pd.DataFrame({
        'Category': ['Receita Atual', 'Falta para a Meta'],
        'Amount': [receita_atual, receita_faltante],
        'Color': ['Current', 'Remaining'] # Helper column for coloring
    })
    
    st.markdown(f"### A meta anual de receita é ${meta_receita} USD")
        
    if not df_filtrado.empty:
        # novas variáveis e dataframes essenciais para esse calculo preditivo
        x = receita_trimestral['Quarter'].values.reshape(-1, 1)
        y = receita_trimestral['Amount'].values
        model = LinearRegression()
        model.fit(x, y)
        next_quarter = np.array([[receita_trimestral['Quarter'].max() + 1]])
        predicted_revenue = model.predict(next_quarter)
        predicted_df = pd.DataFrame({
            'Quarter': [next_quarter[0][0]],
            'Amount': [predicted_revenue[0]],
            'Type': ['Previsão']
        })
        # Calculate total historical revenue
        total_historical_revenue = receita_trimestral['Amount'].sum()
        # Get the predicted revenue for the next quarter
        predicted_next_quarter_revenue = predicted_df['Amount'].iloc[0]
        # Calculate the total revenue including the prediction
        total_revenue_with_prediction = total_historical_revenue + predicted_next_quarter_revenue
        # Create DataFrames for plotting
        # Quarterly data for historical and predicted revenue
        quarterly_plot_df = pd.concat([receita_trimestral.assign(Type='Histórico'), predicted_df], ignore_index=True)
        # Data for Projected Total Revenue - we will associate this with the last quarter for plotting simplicity
        projected_data = pd.DataFrame({
            'Quarter': [quarterly_plot_df['Quarter'].max()],
            'Amount': [total_revenue_with_prediction],
            'Type': ['Receita Projetada']
        })
        # Combine historical, predicted, and projected data for plotting
        all_plot_df = pd.concat([quarterly_plot_df, projected_data], ignore_index=True)
        # Create the line chart
        receita_prevista = px.line(all_plot_df,
                  x='Quarter',
                  y='Amount',
                  color='Type',
                  title='Receita Trimestral (Histórico, Previsão e Projetada) com Meta Anual',
                  labels={'Quarter': 'Trimestre', 'Amount': 'Receita (USD)', 'Type': 'Tipo'},
                  markers=True, # Add markers for data points
                  color_discrete_sequence=px.colors.qualitative.Bold)
                    #   color_discrete_map={'Histórico': 'blue', 'Previsão': 'red', 'Receita Projetada': 'orange'})
        # Add a horizontal line for the annual goal
        receita_prevista.add_shape(type="line",
                      x0=all_plot_df['Quarter'].min(), y0=meta_receita, x1=all_plot_df['Quarter'].max(), y1=meta_receita,
                      line=dict(color="green", width=2, dash="dash"),
                      name='Meta Anual')
        # Add annotations for the annual goal line
        receita_prevista.add_annotation(
            x=all_plot_df['Quarter'].max(),
            y=meta_receita,
            text=f'Meta Anual: ${meta_receita:,.0f}',
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            bgcolor="white",
            opacity=0.8
        )
        receita_prevista.update_xaxes(tickvals=all_plot_df['Quarter'].unique())
        receita_prevista.update_traces(mode='lines+markers', marker=dict(size=18))
        st.plotly_chart(receita_prevista, use_container_width=True)
    else:
        st.write(warning)
            
    col_graf12, col_graf13 = st.columns(2)
    
    with col_graf12:
        if not df_filtrado.empty:
            receita_comparada = px.pie(df_meta_comparacao,
                         names='Category',
                         values='Amount',
                         color='Color',
                         color_discrete_sequence=px.colors.qualitative.Safe,
                        #  color_discrete_map={'Current': 'pink', 'Remaining': 'purple'},
                         title='Receita Anual vs. Meta')
            st.plotly_chart(receita_comparada, use_container_width=True)
        else:
            st.write(warning)

        

         
