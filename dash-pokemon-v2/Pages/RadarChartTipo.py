import streamlit as st
from graph_utils import radar_chart_status, histograma_habilidades, dispersao, quant_types, box_plot_total_points

fig_radar_chart = radar_chart_status('Todas')

def update_grafico_radar_chart(filtroGen):
    fig_radar_chart = radar_chart_status(filtroGen)
    return fig_radar_chart

st.title("Radar Chart de Base Stats Por Tipo")

# Widget para selecionar a geração das outras imagens
filtroGen = st.radio("Geração", ['Todas', 1, 2, 3, 4, 5, 6, 7, 8])
fig_radar_chart = update_grafico_radar_chart(filtroGen)
st.plotly_chart(fig_radar_chart)