import streamlit as st
from graph_utils import box_plot_total_points

fig_box_plot = box_plot_total_points('Todas')

def update_grafico_box_plot(filtroGen):
    fig_box_plot = box_plot_total_points(filtroGen)
    return fig_box_plot

st.title("Box Plot dos Base Stats por tipo")

# Widget para selecionar a geração das outras imagens
filtroGen = st.selectbox("Geração", ['Todas', 1, 2, 3, 4, 5, 6, 7, 8])
fig_box_plot = update_grafico_box_plot(filtroGen)
st.plotly_chart(fig_box_plot)