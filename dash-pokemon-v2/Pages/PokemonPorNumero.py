import pandas as pd
import numpy as np
import streamlit as st
from graph_utils import image_pokemon

st.title("Pokemon por número")

# Função para atualizar imagens/gráficos
def update_imagem_pokemon(numero):
    fig_pokemon = image_pokemon(numero)
    return fig_pokemon

# Widget para selecionar o número do pokémon e aparecer a imagem dele
numero = st.slider("Escolha um número:",1,898)
fig_pokemon = update_imagem_pokemon(numero)
st.plotly_chart(fig_pokemon)