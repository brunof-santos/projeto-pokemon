import streamlit as st
from graph_utils import quant_types

fig_quant_types = quant_types('Todas')

def update_grafico_quant_types(filtroGen):
    fig_quant_types = quant_types(filtroGen)
    return fig_quant_types

st.title("Quantidade de Pokémon por tipo")

# Widget para selecionar a geração das outras imagens
filtroGen = st.selectbox("Geração", ['Todas', 1, 2, 3, 4, 5, 6, 7, 8])
fig_quant_types = update_grafico_quant_types(filtroGen)
st.plotly_chart(fig_quant_types)