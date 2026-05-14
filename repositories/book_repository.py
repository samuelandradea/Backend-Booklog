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

def get_book_by_isbn(isbn: str):
    books_ref = db.collection('books')
    
    query = books_ref.where('isbn', '==', isbn).limit(1).stream()
    
    for doc in query:
        book_data = doc.to_dict()
        book_data['id'] = doc.id
        return book_data
    
    return None

def get_books_by_author(nome_autor: str):
    books_ref = db.collection('books')
    query = books_ref.where('author', '==', nome_autor).stream()
    livros = []
    for doc in query:
        book_data = doc.to_dict()
        book_data['id'] = doc.id
        livros.append(book_data)
    return livros