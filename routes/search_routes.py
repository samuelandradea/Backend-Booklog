from fastapi import APIRouter
# Importamos a função que acabamos de criar na cozinha
from repositories.search_repository import search_in_firebase

router = APIRouter()

@router.get("/search")
def search_all(q: str = ""):
    # O garçom pega o pedido (q) e leva para a cozinha
    dados_encontrados = search_in_firebase(q)
    
    # O garçom entrega o prato pronto para o cliente (aplicativo)
    return dados_encontrados