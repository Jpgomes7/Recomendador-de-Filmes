import pandas as pd
import ast
from difflib import get_close_matches
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

filmes = pd.read_csv('tmdb_5000_movies.csv')
creditos = pd.read_csv('tmdb_5000_credits.csv')

creditos = creditos.rename(columns={'movie_id': 'id'})
dados = filmes.merge(creditos, on='id')
dados = dados[['id', 'title_x', 'overview', 'genres', 'keywords', 'cast', 'crew']]
dados = dados.rename(columns={'title_x': 'title'})
dados = dados.dropna().reset_index(drop=True)

def extrair_nomes(texto):
    return [item['name'] for item in ast.literal_eval(texto)]

def extrair_elenco_principal(texto):
    return [item['name'] for item in ast.literal_eval(texto)[:3]]

def extrair_diretor(texto):
    equipe = ast.literal_eval(texto)
    diretores = [item['name'] for item in equipe if item['job'] == 'Director']
    return diretores

def remover_espacos(lista):
    return [item.replace(' ', '') for item in lista]

for coluna, funcao in [('genres', extrair_nomes), ('keywords', extrair_nomes),
                       ('cast', extrair_elenco_principal), ('crew', extrair_diretor)]:
    dados[coluna] = dados[coluna].apply(funcao)

dados['generos_legiveis'] = dados['genres']
dados['overview'] = dados['overview'].apply(lambda texto: texto.split())

for coluna in ['genres', 'keywords', 'cast', 'crew']:
    dados[coluna] = dados[coluna].apply(remover_espacos)

dados['tags'] = dados['overview'] + dados['genres'] + dados['keywords'] + dados['cast'] + dados['crew']
dados['tags'] = dados['tags'].apply(lambda lista: ' '.join(lista).lower())

vetorizador = CountVectorizer(max_features=5000, stop_words='english')
matriz_vetores = vetorizador.fit_transform(dados['tags']).toarray()
matriz_similaridade = cosine_similarity(matriz_vetores)

def indices_similares(titulo, quantidade=5):
    indice = dados[dados['title'] == titulo].index[0]
    notas_similaridade = list(enumerate(matriz_similaridade[indice]))
    notas_similaridade = sorted(notas_similaridade, key=lambda item: item[1], reverse=True)
    return notas_similaridade[1:quantidade + 1]

def recomendar(titulo, quantidade=5):
    return [dados.iloc[i]['title'] for i, nota in indices_similares(titulo, quantidade)]

def recomendar_detalhado(titulo, quantidade=5):
    resultado = []
    for i, nota in indices_similares(titulo, quantidade):
        linha = dados.iloc[i]
        resultado.append({'titulo': linha['title'], 'generos': linha['generos_legiveis'], 'similaridade': nota})
    return resultado

def buscar_titulo(entrada):
    correspondencia_exata = dados[dados['title'].str.lower() == entrada.lower()]
    if not correspondencia_exata.empty:
        return correspondencia_exata.iloc[0]['title']
    parecidos = get_close_matches(entrada, dados['title'], n=1, cutoff=0.6)
    return parecidos[0] if parecidos else None

if __name__ == '__main__':
    entrada = input('Digite o nome de um filme: ')
    titulo = buscar_titulo(entrada)
    if titulo is None:
        print('Filme não encontrado na base de dados.')
    else:
        print(f'Recomendações para "{titulo}":')
        for filme in recomendar(titulo):
            print('-', filme)