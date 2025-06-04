import numpy as np
from dataframe import df_pokemon

# Função para obter URL da imagem
def get_image_url(pokedex_number):
    number_str = str(pokedex_number).zfill(4)
    return f"https://pokejungle.net/sprites/normal/{number_str}.png"

# Função para criar dados do gráfico de radar
def dados_grafico_radar(tipo_desejado,generation):
    # Filtrando o DataFrame conforme a geração
    if generation != 'Todas':
        df_filtrado_geracoes = df_pokemon[df_pokemon['generation'] == generation]
    else:
        df_filtrado_geracoes = df_pokemon
    # Filtrando o DataFrame pelo tipo da função
    df_tipo = df_filtrado_geracoes[df_filtrado_geracoes['type_all'].str.contains(tipo_desejado)]

    # Calculando a média dos status dos Pokémon do tipo da função
    status_cols = ['hp', 'sp_attack', 'sp_defense', 'speed', 'defense', 'attack']
    status_means = df_tipo[status_cols].mean()

    # Ordenando conforme a ordem do padrão dos jogos
    ordem = ['hp', 'sp_attack', 'sp_defense', 'speed', 'defense', 'attack']
    status_means = status_means[ordem]

    # Alterando nomes da legenda
    legenda = ['HP', 'Sp. Atk', 'Sp. Def', 'Speed', 'Defense', 'Attack']
    values = status_means.values

    # Preparando dados para o gráfico
    values = np.concatenate((values, [values[0]]))

    return values, legenda