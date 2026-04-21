from fastapi import APIRouter, HTTPException
from repositories.book_repository import get_books_for_home, get_book_by_isbn

router = APIRouter()

@router.get("/books")
def get_books():
    dados_livros = get_books_for_home()
    
    # Devolve a lista de livros para o aplicativo
    return dados_livros

@router.get("/books/{isbn}")
def get_book(isbn: str):
    livro = get_book_by_isbn(isbn)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro