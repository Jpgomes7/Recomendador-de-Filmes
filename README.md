# CineMatch — Sistema de Recomendação de Filmes (Projeto de Machine Learning)

## O que é este projeto

Este é um **projeto de Machine Learning** que implementa um sistema de recomendação de filmes **baseado em conteúdo** (content-based filtering) — uma das técnicas clássicas de aprendizado de máquina aplicada a sistemas de recomendação. Diferente de sistemas que recomendam com base no que *outras pessoas* assistiram (filtragem colaborativa), aqui a recomendação é feita comparando o **conteúdo** dos próprios filmes: sinopse, gêneros, palavras-chave, elenco principal e diretor.

A lógica é simples de entender: se dois filmes têm sinopses parecidas, os mesmos gêneros, atores em comum ou o mesmo diretor, é provável que quem gostou de um vá gostar do outro. O sistema transforma essas informações em texto, depois em números (vetores), e mede matematicamente o quão "parecido" cada filme é dos demais usando **Similaridade de Cosseno**.

O projeto tem duas formas de uso:
- **`recomendador.py`** — versão de linha de comando (terminal), onde você digita o nome de um filme e recebe a lista de recomendações.
- **`app.py`** — versão com interface visual (web), construída com Streamlit, no estilo "ingresso de cinema".

Os dados vêm do dataset público **TMDB 5000 Movie Dataset** (The Movie Database), com informações de ~5.000 filmes.

---

## Como o sistema funciona (visão geral)

1. **Carrega e junta** os dois arquivos CSV (filmes e créditos) em uma única tabela, usando o `id` do filme.
2. **Extrai as informações relevantes** de cada filme: sinopse, gêneros, palavras-chave, os 3 atores mais creditados e o diretor.
3. **Junta tudo em um único texto** por filme (chamado de `tags`).
4. **Transforma esse texto em vetores numéricos**, contando a frequência das palavras.
5. **Calcula a similaridade de cosseno** entre todos os pares de filmes — um número de 0 a 1 que indica o quão parecidos são.
6. Quando você escolhe um filme, o sistema **ordena todos os outros filmes pela similaridade** com ele e devolve os mais parecidos.

---

## Estrutura de arquivos

```
📁 projeto/
├── app.py                  → Interface visual (Streamlit)
├── recomendador.py          → Lógica de recomendação (processamento + funções)
├── requirements.txt         → Lista de bibliotecas necessárias
├── README.md                → Este arquivo
├── .streamlit/
│   └── config.toml          → Tema visual do Streamlit (cores, fonte)
├── tmdb_5000_movies.csv      → Dados dos filmes (você precisa adicionar)
└── tmdb_5000_credits.csv     → Dados de elenco/equipe (você precisa adicionar)
```

---

## Bibliotecas usadas e para que servem

### `pandas`
Biblioteca para manipulação de tabelas de dados (semelhante a planilhas, mas em código). É usada para:
- Ler os arquivos CSV (`read_csv`).
- Juntar as duas tabelas de filmes e créditos (`merge`).
- Selecionar colunas, remover linhas com dados faltando e aplicar transformações em cada linha (`apply`).

### `ast` *(biblioteca nativa do Python, não precisa instalar)*
As colunas `genres`, `keywords`, `cast` e `crew` do CSV guardam listas de dicionários, mas como **texto** (ex: `"[{'id': 28, 'name': 'Action'}]"`). O módulo `ast`, através da função `literal_eval`, converte esse texto de volta para uma lista/dicionário real do Python, permitindo extrair só o que interessa (o nome do gênero, do ator, etc.).

### `scikit-learn`
É a biblioteca de **Machine Learning** do projeto — a mesma usada em boa parte dos projetos de ML em Python. Dela vêm duas ferramentas principais:
- **`CountVectorizer`**: transforma o texto de cada filme (a `tags`) em um vetor numérico, contando quantas vezes cada palavra aparece. É o que permite comparar filmes matematicamente.
- **`cosine_similarity`**: calcula a similaridade entre esses vetores, medindo o ângulo entre eles no espaço vetorial. Quanto mais próximo de 1, mais parecidos são os filmes.

### `difflib` *(biblioteca nativa do Python, não precisa instalar)*
Usada na versão de terminal (`recomendador.py`) para encontrar o título mais parecido com o que o usuário digitou, mesmo com erro de digitação ou diferença de maiúsculas/minúsculas (função `get_close_matches`).

### `streamlit`
Framework que transforma um script Python em uma aplicação web interativa, sem precisar escrever HTML/CSS/JavaScript do zero. É usado no `app.py` para criar:
- Campos de seleção (`selectbox`), controles deslizantes (`slider`) e botões (`button`).
- A barra lateral de controles (`st.sidebar`).
- A exibição dos resultados na tela (`st.markdown`, `st.columns`).

### `numpy`
Não é importado diretamente no código, mas é uma **dependência** do `pandas` e do `scikit-learn` — eles usam o `numpy` internamente para fazer as contas com vetores e matrizes de forma rápida. Por isso não aparece no `requirements.txt`: ele é instalado automaticamente junto com as outras bibliotecas.

---

## Instalação

Com o Python já instalado, abra o terminal na pasta do projeto e rode:

```bash
python -m pip install -r requirements.txt
```

Isso instala `pandas`, `scikit-learn` e `streamlit` de uma vez.

Depois, baixe o dataset **TMDB 5000 Movie Dataset** (arquivos `tmdb_5000_movies.csv` e `tmdb_5000_credits.csv`) e coloque os dois na mesma pasta dos scripts.

---

## Como rodar

### Versão terminal
```bash
python recomendador.py
```
O programa vai pedir o nome de um filme e imprimir as 5 recomendações mais parecidas.

### Versão web (Streamlit)
```bash
python -m streamlit run app.py
```
Isso abre automaticamente uma aba no navegador com a interface visual: escolha o filme na barra lateral, ajuste quantas recomendações quer ver e clique em "Gerar recomendações".

---

## Arquivos de dados esperados

O projeto usa o **TMDB 5000 Movie Dataset**, disponível publicamente (ex: no Kaggle), composto por dois arquivos:

- **`tmdb_5000_movies.csv`** — contém `id`, `title`, `overview`, `genres`, `keywords`, entre outras colunas.
- **`tmdb_5000_credits.csv`** — contém `movie_id`, `title`, `cast` e `crew`.

O `recomendador.py` junta os dois pela coluna de ID do filme.

---

