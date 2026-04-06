from firebase.config import db 

def search_in_firebase(termo: str):
    resultados = {
        "usuarios": [],
        "livros": [],
        "autores": [] 
    }

    if not termo:
        return resultados

    # 1. BUSCANDO USUÁRIOS (Coleção: users | Campo: name)
    users_ref = db.collection('users')
    query_users = users_ref.where('name', '==', termo).stream()
    
    for doc in query_users:
        user_data = doc.to_dict()
        user_data['id'] = doc.id 
        resultados["usuarios"].append(user_data)

    # 2. BUSCANDO LIVROS (Coleção: books | Campo: title)
    books_ref = db.collection('books')
    query_books = books_ref.where('title', '==', termo).stream()
    
    for doc in query_books:
        book_data = doc.to_dict()
        book_data['id'] = doc.id
        resultados["livros"].append(book_data)

    # 3. BUSCANDO AUTORES (Coleção: books | Campo: authors)
    query_authors = books_ref.where('authors', '==', termo).stream()
    
    for doc in query_authors:
        author_data = doc.to_dict()
        author_data['id'] = doc.id
        resultados["autores"].append(author_data)

    return resultados