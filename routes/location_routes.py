from fastapi import APIRouter, HTTPException
from repositories.location_repository import create_location, get_all_locations, get_location, update_location, delete_location
from pydantic import BaseModel, Field
from typing import Optional

# ==========================================
# MODELOS (PYDANTIC) - Validação de Dados
# ==========================================

class LocationModel(BaseModel):
    """
    Modelo de validação para criar um Novo Local.
    O FastAPI vai recusar automaticamente qualquer requisição que não envie todos esses campos (exceto fotoUrl que é Optional).
    """
    nome: str
    endereco: str
    latitude: float
    longitude: float
    tipo: str # Ex: 'livraria', 'biblioteca', 'sebo'
    fotoUrl: Optional[str] = None # Campo opcional para salvar a imagem do local

class LocationUpdateModel(BaseModel):
    """
    Modelo para atualização. Todos os campos são opcionais, 
    permitindo que o usuário atualize apenas o 'nome' ou apenas a 'foto', por exemplo.
    """
    nome: Optional[str] = None
    endereco: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tipo: Optional[str] = None
    fotoUrl: Optional[str] = None

# Cria o objeto que vai gerenciar as rotas HTTP de locais
router = APIRouter()

# ==========================================
# ENDPOINTS (ROTAS HTTP)
# ==========================================

@router.post("/users/{uid}/locations", status_code=201)
def create_location_route(uid: str, body: LocationModel):
    """
    Rota para CADASTRAR um novo local.
    Recebe o ID do usuário (uid) na URL e os dados do local no corpo da requisição (body).
    """
    # model_dump() transforma o modelo Pydantic num dicionário Python que o Firebase aceita
    result = create_location(uid, body.model_dump())
    
    # Se o repositório avisar que já existe um local nessas coordenadas exatas, barra a criação (Erro 409 - Conflict)
    if result == "DUPLICATE":
        raise HTTPException(status_code=409, detail="Já existe um Ponto Literário cadastrado exatamente nessas coordenadas.")
        
    return {"message": "Local criado com sucesso", "locationId": result}


@router.get("/locations")
def get_all_locations_route():
    """
    Rota para LISTAR TODOS os locais cadastrados.
    Vai ser usada para popular o mapa do app assim que ele abrir.
    """
    return get_all_locations()


@router.get("/locations/{location_id}")
def get_location_route(location_id: str):
    """
    Rota para PEGAR UM LOCAL ESPECÍFICO através do seu ID.
    Pode ser usado quando o usuário clica num pin do mapa para ver os detalhes completos daquela livraria.
    """
    location = get_location(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return location


@router.put("/locations/{location_id}")
def update_location_route(location_id: str, body: LocationUpdateModel):
    """
    Rota para ATUALIZAR dados de um local existente.
    """
    # exclude_none=True garante que se o usuário não mandou um campo (ex: não mandou 'nome'), 
    # ele não vai apagar o 'nome' que já estava salvo no banco.
    updated = update_location(location_id, body.model_dump(exclude_none=True))
    
    if not updated:
        raise HTTPException(status_code=404, detail="Local não encontrado para atualização")
    return {"message": "Local atualizado com sucesso"}


@router.delete("/users/{uid}/locations/{location_id}")
def delete_location_route(uid: str, location_id: str):
    """
    Rota para DELETAR um local.
    Recebe o uid de quem está tentando deletar para checarmos a permissão de segurança.
    """
    result = delete_location(uid, location_id)
    
    if result == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Local não encontrado")
    if result == "UNAUTHORIZED":
        raise HTTPException(status_code=403, detail="Acesso Negado: Você não tem permissão para deletar este local porque não foi você quem o criou.")
        
    return {"message": "Local deletado com sucesso"}
