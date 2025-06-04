import pandas as pd
import numpy as np

DATASET_PATH = "assets/pokedex.csv"

# Lendo dataframe
df_pokemon = pd.read_csv(DATASET_PATH)
# Apagando colunas
df_pokemon = df_pokemon.drop(['Unnamed: 0', 'german_name', 'japanese_name', 'against_normal', 'against_fire', 'against_water', 'against_electric','against_grass', 'against_ice', 'against_fight', 'against_poison', 'against_ground', 'against_flying', 'against_psychic', 'against_bug', 'against_rock', 'against_ghost', 'against_dragon', 'against_dark', 'against_steel', 'against_fairy'], axis=1)
# Criando coluna de percentage female
df_pokemon['percentage_female'] = 100 - df_pokemon['percentage_male']
# Criando coluna de semm gênero
df_pokemon['genderless'] = np.where(df_pokemon['percentage_male'].notna(), False, True)
# Colocando "-" no lugar de NaN na coluna type_2
df_pokemon['type_2'] = df_pokemon['type_2'].fillna('-')
# Criando coluna type_all com uma concatenação de ambos os tipos
df_pokemon['type_all'] = df_pokemon['type_1'] + '/' + df_pokemon['type_2']