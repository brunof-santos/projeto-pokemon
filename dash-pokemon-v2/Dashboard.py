import streamlit as st
import random
from dataframe import df_pokemon

st.title("Dashboard Pokémon")

# Gerando 6 números aleatórios entre 1 e 898
numeros_aleatorios = [random.randint(1, 898) for _ in range(6)]
nomes_aleatorios = []

# Criando URLs das imagens com base nos números aleatórios
urls_imagens = [f"https://pokejungle.net/sprites/normal/{str(numero).zfill(4)}.png" for numero in numeros_aleatorios]

# Obter nomes dos Pokémon usando os números aleatórios
nomes_aleatorios = []
for numero in numeros_aleatorios:
    df_nome = df_pokemon[df_pokemon['pokedex_number'] == numero]
    if not df_nome.empty:
        nome = df_nome['name'].values[0]
        nomes_aleatorios.append(nome)
    else:
        nomes_aleatorios.append("Desconhecido")

# Criando 6 colunas
colunas = st.columns(6)

# Adicionando uma imagem em cada coluna
for i, url in enumerate(urls_imagens):
    colunas[i].image(url, caption=nomes_aleatorios[i], use_column_width=True)

st.caption("Atualize a página e veja qual seria seu time :D")

st.header("")
st.header("Sites úteis:")

# Botões de páginas
st.link_button("Bulbapedia", "https://bulbapedia.bulbagarden.net/wiki/Main_Page")
st.link_button("Serebii", "https://www.serebii.net")
st.link_button("Pokéjungle", "https://pokejungle.net")