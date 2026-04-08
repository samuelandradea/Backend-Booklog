from fastapi import APIRouter
from repositories.search_repository import search_in_firebase

router = APIRouter()

@router.get("/search")
def search_all(q: str = ""):
    dados_encontrados = search_in_firebase(q)
    

    return dados_encontrados