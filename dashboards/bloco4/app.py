import streamlit as st ##serve para criar aplicações
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Venda de chocolate por país", ## cria o titulo da pagina, que fica na barrinha la em cima
    page_icon="🍫",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/luhm/gatolate/refs/heads/main/data/chocolate_sales.csv")

