# repositories/ml_repository.py
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

BASE       = Path(__file__).parent.parent
_modelo    = joblib.load(BASE / 'models' / 'best_model.pkl')
_mlb       = joblib.load(BASE / 'models' / 'mlb.pkl')
_df        = pd.read_parquet(BASE / 'data' / 'books_clean.parquet')
_X_npz     = np.load(BASE / 'data' / 'X_matrix.npz')
_X         = _X_npz[_X_npz.files[0]]

_df['genre_list'] = _df['genre_list'].apply(
    lambda x: list(x) if not isinstance(x, list) else x
)


def get_recomendacoes(generos: list[str], top_n: int = 10) -> list:
    """
    Recebe lista de gêneros e retorna os top_n livros mais similares.
    Escopo padrão: todos os 84k livros do dataset.
    """
    generos_validos = [
        g.lower().strip() for g in generos
        if g.lower().strip() in _mlb.classes_
    ]

    if not generos_validos:
        return []

    # Vetorizar o perfil do usuário
    user_genre_vec = _mlb.transform([generos_validos])
    n_num          = _X.shape[1] - user_genre_vec.shape[1]
    user_vec       = np.hstack([user_genre_vec, np.zeros((1, n_num))])

    # Buscar vizinhos
    distances, indices = _modelo.kneighbors(user_vec, n_neighbors=top_n)

    resultado = _df.iloc[indices[0]][['title', 'author', 'genre', 'rating', 'img', 'isbn']].copy()
    resultado['similaridade'] = (1 - distances[0]).round(4)

    return resultado.to_dict(orient='records')


def get_recomendacoes_por_autor(generos: list[str], nome_autor: str, top_n: int = 10) -> list:
    """
    Mesmo modelo, mas filtra o escopo para livros de um autor específico.
    Útil para recomendar dentro da obra de um autor que o usuário gosta.
    """
    generos_validos = [
        g.lower().strip() for g in generos
        if g.lower().strip() in _mlb.classes_
    ]

    if not generos_validos:
        return []

    # Filtrar índices do autor no dataset
    indices_autor = _df[_df['author'].str.lower() == nome_autor.lower()].index.tolist()

    if not indices_autor:
        return []

    # Vetorizar usuário
    user_genre_vec = _mlb.transform([generos_validos])
    n_num          = _X.shape[1] - user_genre_vec.shape[1]
    user_vec       = np.hstack([user_genre_vec, np.zeros((1, n_num))])

    # Calcular similaridade só nos livros do autor
    from sklearn.metrics.pairwise import cosine_similarity
    X_autor      = _X[indices_autor]
    similaridades = cosine_similarity(user_vec, X_autor)[0]

    top_idx_local = np.argsort(similaridades)[::-1][:top_n]
    top_idx_global = [indices_autor[i] for i in top_idx_local]

    resultado = _df.iloc[top_idx_global][['title', 'author', 'genre', 'rating', 'img', 'isbn']].copy()
    resultado['similaridade'] = similaridades[top_idx_local].round(4)

    return resultado.to_dict(orient='records')