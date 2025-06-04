import requests
from PIL import Image
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px
import base64
from plotly.subplots import make_subplots
from helper_utils import get_image_url, dados_grafico_radar
from dataframe import df_pokemon

#Variáveis para geração das imagens
# Tipos de Pokémon e suas cores em formato RGB
cores_por_tipo = {
    'Grass': (120, 180, 120),
    'Fire': (220, 120, 120),
    'Water': (120, 150, 200),
    'Electric': (220, 220, 100),
    'Ice': (120, 200, 200),
    'Steel': (160, 160, 160),
    'Rock': (170, 170, 170),
    'Ground': (200, 160, 120),
    'Bug': (160, 190, 100),
    'Normal': (180, 160, 130),
    'Dark': (130, 100, 80),
    'Ghost': (120, 120, 180),
    'Psychic': (200, 120, 180),
    'Fairy': (200, 140, 200),
    'Dragon': (100, 140, 180),
    'Flying': (130, 170, 210),
    'Fighting': (180, 120, 100),
    'Poison': (140, 100, 180)
}

# Lista de todos os tipos de Pokémon
types = ['Grass', 'Fire', 'Water', 'Electric', 'Ice', 'Steel', 'Rock', 'Ground','Bug', 'Normal',
         'Dark', 'Ghost', 'Psychic', 'Fairy', 'Dragon','Flying', 'Fighting', 'Poison']

# Definindo as cores de cada tipo
cores_tipos = {
    'Grass': '#78C850', 'Fire': '#F08030', 'Water': '#6890F0', 'Electric': '#F8D030',
    'Ice': '#98D8D8', 'Steel': '#B8B8D0', 'Rock': '#B8A038', 'Ground': '#E0C068',
    'Bug': '#A8B820', 'Normal': '#A8A878', 'Dark': '#705848', 'Ghost': '#705898',
    'Psychic': '#F85888', 'Fairy': '#EE99AC', 'Dragon': '#7038F8', 'Flying': '#A890F0',
    'Fighting': '#C03028', 'Poison': '#A040A0'
}

# Imagem com Top Maiores (Status a definir pelo usuário)
def best_status(status_desejado):
    # Definindo o status desejado para filtrar os Pokémon
    # Pode ser 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'
    # status_desejado = 'attack'
    
    # Filtrando os Pokémon com base no status desejado
    data = df_pokemon
    top_5_status = data.nlargest(5, status_desejado)
    
    # Criando uma lista para armazenar as imagens e informações
    images_best_status_info = []

    for _, row in top_5_status.iterrows():
        name = row['name']
        status_value = row[status_desejado]
        url = get_image_url(row['pokedex_number'])

        response = requests.get(url)
        if response.status_code == 200:
            image_best_status = Image.open(BytesIO(response.content))
            images_best_status_info.append((name, status_value, image_best_status))
        else:
            print(f"Erro ao obter a imagem do Pokémon com Pokedex Number {row['pokedex_number']}")

    # Criando a figura Plotly
    fig_best_status = go.Figure()

    for i, (name, status_value, image) in enumerate(images_best_status_info):
        # Convertendo a imagem PIL para uma URL base64
        image_stream = BytesIO()
        image.save(image_stream, format='png')
        image_base64 = base64.b64encode(image_stream.getvalue()).decode()
        image_url = f"data:image/png;base64,{image_base64}"

        # Adicionando a imagem à figura
        fig_best_status.add_layout_image(
            dict(
                source=image_url,
                x=i * 0.2,
                y=1,
                sizex=0.2,
                sizey=0.6,
                xanchor="left",
                yanchor="top"
            )
        )

        # Adicionando o texto ao lado da imagem
        fig_best_status.add_annotation(
            dict(
                text=f"{name}<br>{status_desejado.capitalize()}: {status_value}",
                x=i * 0.18 + 0.055,
                y=0.55,
                showarrow=False,
                font=dict(size=14),
                xanchor="left",
                yanchor="top"
            )
        )

    # Ajustando o layout
    fig_best_status.update_layout(
        width=1600,
        height=400,
        showlegend=False,
        xaxis=dict(
            visible=False,
            range=[0, 1]
        ),
        yaxis=dict(
            visible=False,
            range=[0, 1]
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    # Exibindo o gráfico
    #fig_best_status.show()
    return fig_best_status

# Radar Chart por tipo
def radar_chart_status(generation):
    # Criando subplots
    fig_radar_chart = make_subplots(rows=6, cols=3, specs=[[{'type': 'polar'}]*3]*6, subplot_titles=types)

    for i, tipo in enumerate(types):
        row = i // 3 + 1
        col = i % 3 + 1

        values, legenda = dados_grafico_radar(tipo,generation)

        fig_radar_chart.add_trace(go.Scatterpolar(
            r=values,
            theta=legenda,
            fill='toself',
            name=tipo,
            line=dict(color=cores_tipos[tipo]),
            showlegend=False
        ), row=row, col=col)

        # Ajustando a rotação do gráfico
        fig_radar_chart.update_polars(
            row=row, col=col,
            angularaxis=dict(
                rotation=60
            ),
            radialaxis=dict(
                visible=True,
                range=[0, 155]
            )
        )

    # Ajustando o layout dos subplots
    fig_radar_chart.update_layout(
        title="Gráficos de Radar dos Tipos de Pokémon",
        height=1200,
        width=1800,
        showlegend=False,
        grid=dict(
            rows=6,
            columns=3,
            pattern='independent',
        )
    )

    # Ajustando o título de cada subplot
    for i, tipo in enumerate(types):
        row = i // 3 + 1
        col = i % 3 + 1
        fig_radar_chart.layout.annotations[i].update(text=tipo, font=dict(size=12, color='black'))

    # Exibindo o gráfico
    #fig_radar_chart.show()
    return fig_radar_chart

# Gráfico de barras: quantidade de pokémon por tipos
def quant_types(generation):
    # Filtrando o DataFrame conforme a geração
    if generation != 'Todas':
        df_filtrado_geracoes = df_pokemon[df_pokemon['generation'] == generation]
    else:
        df_filtrado_geracoes = df_pokemon
    
    # Inicializando o dicionário com os valores desejados
    types_count = {
        'Grass': 0,
        'Fire': 0,
        'Water': 0,
        'Electric': 0,
        'Ice': 0,
        'Steel': 0,
        'Rock': 0,
        'Ground': 0,
        'Bug': 0,
        'Normal': 0,
        'Dark': 0,
        'Ghost': 0,
        'Psychic': 0,
        'Fairy': 0,
        'Dragon': 0,
        'Flying': 0,
        'Fighting': 0,
        'Poison': 0
    }

    # Contando os tipos a partir do DataFrame
    for types in df_filtrado_geracoes['type_all']:
        if '/' in types:
            type1, type2 = types.split('/')
            if type1 in types_count:
                types_count[type1] += 1
            if type2 in types_count:
                types_count[type2] += 1
        else:
            type1 = types
            if type1 in types_count:
                types_count[type1] += 1

    # Removendo o tipo "-"
    if '-' in types_count:
        del types_count['-']

    # Preparando os dados para Plotly
    x_quant_types = list(types_count.keys())
    y_quant_types = list(types_count.values())
    colors_quant_types = ['rgb({},{},{})'.format(*cores_por_tipo[tipo]) for tipo in x_quant_types]

    # Criando o gráfico de barras
    fig_quant_types = go.Figure(data=[go.Bar(x=x_quant_types, y=y_quant_types, marker_color=colors_quant_types)])

    # Ajustes do layout
    fig_quant_types.update_layout(
        title='Quantidade de Pokémon por Tipo',
        xaxis_title='Tipo de Pokémon',
        yaxis_title='Quantidade',
        xaxis_tickangle=-45,
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.7)',
            gridwidth=1
        ),
        template='plotly_white'
    )

    #fig_quant_types.show()
    return fig_quant_types

# Gráfico de dispersão: altura x peso
def dispersao(tipo):    
    # Filtrando o DataFrame conforme a geração
    if tipo != 'Todos':
        df_pokemon_dispersao = df_pokemon[df_pokemon['type_all'].str.contains(tipo, case=False, na=False)]
    else:
        df_pokemon_dispersao = df_pokemon
    
    # Filtrando linhas onde height_m ou weight_kg sejam nulos
    df_pokemon_dispersao = df_pokemon_dispersao.dropna(subset=['height_m', 'weight_kg', 'name'])
    
    # Criando o gráfico de dispersão
    fig_dispersao = px.scatter(
        df_pokemon_dispersao,
        hover_data={'name': True, 'height_m': True, 'weight_kg': True},
        x='height_m',
        y='weight_kg',
        title='Gráfico de Dispersão de Altura x Peso dos Pokémon',
        labels={'height_m': 'Altura (m)', 'weight_kg': 'Peso (kg)'},
        opacity=0.5,
        color_discrete_sequence=['blue']
    )

    # Personalizando a dica de ferramenta
    fig_dispersao.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Altura: %{x} m<br>Peso: %{y} kg<extra></extra>",
        customdata=df_pokemon_dispersao[['name']].values
    )

    # Adicionando bordas pretas às bolinhas
    fig_dispersao.update_traces(marker=dict(line=dict(width=1, color='black')))
    
    return fig_dispersao

# Boxplot: total points por tipo
def box_plot_total_points(generation):
    # Filtrando o DataFrame conforme a geração
    if generation != 'Todas':
        df_filtrado_geracoes = df_pokemon[df_pokemon['generation'] == generation]
    else:
        df_filtrado_geracoes = df_pokemon
    
    # Preparando os dados para o box plot
    data_box_plot = []
    colors_box_plot = []

    for t in types:
        subset = df_filtrado_geracoes[(df_filtrado_geracoes['type_1'] == t) | (df_filtrado_geracoes['type_2'] == t)]
        if not subset.empty:
            data_box_plot.append(subset['total_points'])
            colors_box_plot.append(f'rgb{cores_por_tipo[t]}')

    # Criando o box plot
    fig_box_plot = go.Figure()

    for i, t in enumerate(types):
        fig_box_plot.add_trace(go.Box(
            y=data_box_plot[i],
            name=t,
            marker_color=colors_box_plot[i],
            boxmean='sd'  # Mostra a média e o desvio padrão na caixa
        ))

    # Personalizando o layout
    fig_box_plot.update_layout(
        title='Box Plot de Base Total Points por tipos de Pokémon',
        xaxis_title='Tipos',
        yaxis_title='Base Total Points',
        xaxis_tickangle=-45,
        template='plotly_white'
    )

    # Exibindo o gráfico
    #fig_box_plot.show()
    return fig_box_plot

# Histograma: quantidade de habilidades (3,2,1)
def histograma_habilidades(tipo):
    # Filtrando o DataFrame conforme a geração
    if tipo != 'Todos':
        df_pokemon_histograma = df_pokemon[df_pokemon['type_all'].str.contains(tipo, case=False, na=False)]
    else:
        df_pokemon_histograma = df_pokemon
    
    # Criando o histograma
    fig_hist = px.histogram(
        df_pokemon_histograma,
        x='abilities_number',
        nbins=4,
        category_orders={'abilities_number': [0, 1, 2, 3]},
        title='Histograma do Número de Habilidades dos Pokémon',
        labels={'abilities_number': 'Número de Habilidades', 'count': 'Frequência'}
    )

    # Adicionando bordas pretas às barras
    fig_hist.update_traces(marker=dict(line=dict(width=1, color='black')))

    # Configurações do gráfico
    fig_hist.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=['0', '1', '2', '3']
        ),
        yaxis_title='Quantidade de Pokémon',
        template='plotly_white'
    )

    # Exibindo o gráfico
    #fig_hist.show()
    return fig_hist

def image_pokemon(numero):
    nome_pokemon = df_pokemon[df_pokemon['pokedex_number'] == numero]
    nome_pokemon = nome_pokemon['name'].values[0]
    # Definindo a URL da imagem
    numero = str(numero).zfill(4)
    url = f"https://pokejungle.net/sprites/normal/{numero}.png"
    # Fazendo o download da imagem
    response = requests.get(url)
    # Abrindo a imagem
    img = Image.open(BytesIO(response.content))
    # Convertendo a imagem para Base64
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    
    # Criando a figura com Plotly
    fig_pokemon = go.Figure()

    # Adicionando a imagem à figura
    fig_pokemon.add_layout_image(
        dict(
            source=f'data:image/png;base64,{img_base64}',
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            xanchor="left",
            yanchor="top",
            opacity=1,
            layer="below"
        )
    )

    # Ajustando a configuração da figura
    fig_pokemon.update_layout(
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        width=img.width,
        height=img.height,
        title=f'{nome_pokemon}'
    )

    # Exibindo a figura
    #fig_pokemon.show()
    return fig_pokemon