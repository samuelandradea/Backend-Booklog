from fastapi import APIRouter
from repositories.book_repository import get_books_for_home

router = APIRouter()

@router.get("/books")
def get_books():
    dados_livros = get_books_for_home()
    
    # Devolve a lista de livros para o aplicativo
    return dados_livros