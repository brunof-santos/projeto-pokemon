import streamlit as st
from graph_utils import dispersao

fig_dispersao = dispersao('Todos')

def update_grafico_dispersao(filtroTipo):
    fig_dispersao = dispersao(filtroTipo)
    return fig_dispersao

st.title("Peso X Altura - por tipo")

# Widget para selecionar o tipo das duas imagens
filtroTipo = st.selectbox("Tipo", ['Todos', 'Grass', 'Fire', 'Water', 'Electric', 'Ice', 'Steel', 'Rock', 'Ground', 'Bug', 'Normal', 'Dark', 'Ghost', 'Psychic', 'Fairy', 'Dragon', 'Flying', 'Fighting', 'Poison'])
fig_dispersao = update_grafico_dispersao(filtroTipo)

st.plotly_chart(fig_dispersao)