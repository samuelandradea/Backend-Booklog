from firebase.config import db 

def search_in_firebase(termo: str):
    resultados = {
        "usuarios": [],
        "livros": [],
        "autores": [] 
    }

    if not termo:
        return resultados

    
    # 1. Arruma o texto colocando a primeira letra de cada palavra maiúscula
    termo_formatado = termo.title()
    
    # 2. Cria o limite final da busca com o caractere mágico do Firebase
    limite = termo_formatado + '\uf8ff'

    # ---------------------------------------------------------
    # 1. BUSCANDO USUÁRIOS
    # Procura nomes que comecem com as letras digitadas
    # ---------------------------------------------------------
    users_ref = db.collection('users')
    query_users = users_ref.where('name', '>=', termo_formatado).where('name', '<=', limite).stream()
    
    for doc in query_users:
        user_data = doc.to_dict()
        user_data['id'] = doc.id 
        resultados["usuarios"].append(user_data)

    # ---------------------------------------------------------
    # 2. BUSCANDO LIVROS 
    # ---------------------------------------------------------
    books_ref = db.collection('books')
    query_books = books_ref.where('title', '>=', termo_formatado).where('title', '<=', limite).stream()
    
    for doc in query_books:
        book_data = doc.to_dict()
        book_data['id'] = doc.id
        resultados["livros"].append(book_data)

    # ---------------------------------------------------------
    # 3. BUSCANDO AUTORES
    # ---------------------------------------------------------
    query_authors = books_ref.where('authors', '>=', termo_formatado).where('authors', '<=', limite).stream()
    
    for doc in query_authors:
        author_data = doc.to_dict()
        author_data['id'] = doc.id
        resultados["autores"].append(author_data)

    return resultados