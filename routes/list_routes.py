from fastapi import APIRouter
from repositories.list_repository import (
    create_list, get_list, get_lists_by_user,
    add_book_to_list, remove_book_from_list,
    update_list, delete_list
)
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

# Modelo para criação de lista — só precisa do nome e do userId
class ListModel(BaseModel):
    name: str
    userId: str

# Modelo para atualização — só o nome pode ser alterado diretamente
class ListUpdateModel(BaseModel):
    name: Optional[str] = None

# Modelo para adicionar/remover livro
class BookEntryModel(BaseModel):
    bookIsbn: str

@router.post("/lists")
def create_list_route(body: ListModel):
    # Gera um ID único automaticamente para a lista
    list_id = str(uuid.uuid4())
    create_list(list_id, {
        "name": body.name,
        "userId": body.userId,
        "bookEntries": {}
    })
    return {"id": list_id, "message": "Lista criada com sucesso"}

@router.get("/lists/{list_id}")
def get_list_route(list_id: str):
    return get_list(list_id)

@router.get("/users/{uid}/lists")
def get_user_lists_route(uid: str):
    # Rota dedicada para buscar todas as listas de um usuário específico
    return get_lists_by_user(uid)

@router.put("/lists/{list_id}")
def update_list_route(list_id: str, body: ListUpdateModel):
    update_list(list_id, body.model_dump(exclude_none=True))
    return {"message": "Lista atualizada com sucesso"}

@router.post("/lists/{list_id}/books")
def add_book_route(list_id: str, body: BookEntryModel):
    add_book_to_list(list_id, body.bookIsbn)
    return {"message": "Livro adicionado com sucesso"}

@router.delete("/lists/{list_id}/books/{book_isbn}")
def remove_book_route(list_id: str, book_isbn: str):
    remove_book_from_list(list_id, book_isbn)
    return {"message": "Livro removido com sucesso"}

@router.delete("/lists/{list_id}")
def delete_list_route(list_id: str):
    delete_list(list_id)
    return {"message": "Lista deletada com sucesso"}