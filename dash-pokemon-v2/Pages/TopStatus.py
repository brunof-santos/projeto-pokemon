import pandas as pd
import numpy as np
import streamlit as st
from graph_utils import best_status

st.title("Top 5 pokemon por status")

fig_best_status = best_status('hp')

def update_grafico_status(status):
    fig_best_status = best_status(status)
    return fig_best_status

# Widget para selecionar o status da primeira imagem
status = st.selectbox("Status", ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'])
fig_best_status = update_grafico_status(status)
st.plotly_chart(fig_best_status)