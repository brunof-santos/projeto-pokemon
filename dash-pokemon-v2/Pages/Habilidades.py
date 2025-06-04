import streamlit as st
from graph_utils import histograma_habilidades

fig_hist = histograma_habilidades('Todos')

def update_grafico_habilidade(filtroTipo):
    fig_hist = histograma_habilidades(filtroTipo)
    return fig_hist

st.title("Quantidade de habilidades por tipo")

# Widget para selecionar o tipo das duas imagens
filtroTipo = st.selectbox("Tipo", ['Todos', 'Grass', 'Fire', 'Water', 'Electric', 'Ice', 'Steel', 'Rock', 'Ground', 'Bug', 'Normal', 'Dark', 'Ghost', 'Psychic', 'Fairy', 'Dragon', 'Flying', 'Fighting', 'Poison'])
fig_hist = update_grafico_habilidade(filtroTipo)
st.plotly_chart(fig_hist)