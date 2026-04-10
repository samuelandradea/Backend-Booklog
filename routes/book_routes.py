from fastapi import APIRouter, HTTPException
from repositories.book_repository import get_books, get_book

router = APIRouter()

@router.get("/books")
def get_books_route():
    return get_books()

@router.get("/books/{isbn}")
def get_book_route(isbn: str):
    book = get_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book