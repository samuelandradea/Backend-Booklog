# repositories/ml_repository.py
import math
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

BASE    = Path(__file__).parent.parent
_modelo = joblib.load(BASE / 'models' / 'best_model.pkl')
_mlb    = joblib.load(BASE / 'models' / 'mlb.pkl')
_df     = pd.read_parquet(BASE / 'data' / 'books_clean.parquet')
_X_npz  = np.load(BASE / 'data' / 'X_matrix.npz')
_X      = _X_npz[_X_npz.files[0]]

# Garantir que genre_list é lista de verdade (não array numpy)
_df['genre_list'] = _df['genre_list'].apply(
    lambda x: list(x) if not isinstance(x, list) else x
)


def _limpar_valor(v):
    """
    Converte qualquer valor que não seja serializável em JSON para None.
    Cobre: float NaN, numpy NaN, numpy int/float, numpy arrays.
    """
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    # Tipos numpy não são serializáveis pelo json padrão
    if isinstance(v, np.floating):
        return None if math.isnan(float(v)) else float(v)
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.ndarray):
        return v.tolist()
    return v


def _serializar(df_resultado) -> list:
    """
    Converte um DataFrame de resultados para lista de dicts JSON-safe.
    Aplica _limpar_valor em todos os campos de todas as linhas.
    """
    return [
        {k: _limpar_valor(v) for k, v in row.items()}
        for row in df_resultado.to_dict(orient='records')
    ]


def get_recomendacoes(generos: list[str], top_n: int = 10) -> list:
    """
    Recebe lista de gêneros do usuário e retorna os top_n livros
    mais similares usando o modelo KNN treinado.

    Escopo: todos os 84k livros do dataset.

    Parâmetros
    ----------
    generos : list[str]
        Lista de gêneros preferidos pelo usuário.
        Ex: ['fantasy', 'mystery']
    top_n : int
        Quantidade de livros a retornar. Padrão: 10.

    Retorna
    -------
    list de dicts com campos: title, author, genre, rating, img, isbn, similaridade
    """
    generos_validos = [
        g.lower().strip() for g in generos
        if g.lower().strip() in _mlb.classes_
    ]

    if not generos_validos:
        return []

    # Vetorizar o perfil do usuário no mesmo espaço dos livros
    user_genre_vec = _mlb.transform([generos_validos])
    n_num          = _X.shape[1] - user_genre_vec.shape[1]
    user_vec       = np.hstack([user_genre_vec, np.zeros((1, n_num))])

    # Buscar os top_n livros mais próximos
    distances, indices = _modelo.kneighbors(user_vec, n_neighbors=top_n)

    resultado = _df.iloc[indices[0]][['title', 'author', 'genre', 'rating', 'img', 'isbn']].copy()
    resultado['similaridade'] = (1 - distances[0]).round(4)

    return _serializar(resultado)


def get_recomendacoes_por_autor(generos: list[str], nome_autor: str, top_n: int = 10) -> list:
    """
    Mesmo modelo KNN, mas restringe o escopo aos livros de um autor específico.
    Útil para recomendar dentro da obra de um autor que o usuário já gosta.

    Parâmetros
    ----------
    generos : list[str]
        Lista de gêneros preferidos pelo usuário.
    nome_autor : str
        Nome do autor para filtrar o escopo.
    top_n : int
        Quantidade de livros a retornar. Padrão: 10.

    Retorna
    -------
    list de dicts com campos: title, author, genre, rating, img, isbn, similaridade
    """
    generos_validos = [
        g.lower().strip() for g in generos
        if g.lower().strip() in _mlb.classes_
    ]

    if not generos_validos:
        return []

    # Filtrar índices dos livros do autor no dataset
    indices_autor = _df[
        _df['author'].str.lower() == nome_autor.lower()
    ].index.tolist()

    if not indices_autor:
        return []

    # Vetorizar o perfil do usuário
    user_genre_vec = _mlb.transform([generos_validos])
    n_num          = _X.shape[1] - user_genre_vec.shape[1]
    user_vec       = np.hstack([user_genre_vec, np.zeros((1, n_num))])

    # Calcular similaridade por cosseno apenas nos livros do autor
    from sklearn.metrics.pairwise import cosine_similarity
    X_autor       = _X[indices_autor]
    similaridades = cosine_similarity(user_vec, X_autor)[0]

    # Pegar os top_n mais similares
    top_idx_local  = np.argsort(similaridades)[::-1][:top_n]
    top_idx_global = [indices_autor[i] for i in top_idx_local]

    resultado = _df.iloc[top_idx_global][['title', 'author', 'genre', 'rating', 'img', 'isbn']].copy()
    resultado['similaridade'] = similaridades[top_idx_local].round(4)

    return _serializar(resultado)