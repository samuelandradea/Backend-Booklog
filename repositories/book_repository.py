from firebase.config import db

def get_books_for_home(limite: int = 15):
    # Conecta com a coleção 'books'
    books_ref = db.collection('books')
    

    query = books_ref.limit(limite).stream()

    livros = []
    for doc in query:
        book_data = doc.to_dict()
        book_data['id'] = doc.id
        livros.append(book_data)

    return livros