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

class ListModel(BaseModel):
    name: str

class ListUpdateModel(BaseModel):
    name: Optional[str] = None

class BookEntryModel(BaseModel):
    bookIsbn: str

@router.post("/users/{uid}/lists")
def create_list_route(uid: str, body: ListModel):
    list_id = str(uuid.uuid4())
    create_list(uid, list_id, {
        "name": body.name,
        "userId": uid,
        "bookEntries": {}
    })
    return {"id": list_id, "message": "Lista criada com sucesso"}

@router.get("/users/{uid}/lists")
def get_user_lists_route(uid: str):
    return get_lists_by_user(uid)

@router.get("/users/{uid}/lists/{list_id}")
def get_list_route(uid: str, list_id: str):
    return get_list(uid, list_id)

@router.put("/users/{uid}/lists/{list_id}")
def update_list_route(uid: str, list_id: str, body: ListUpdateModel):
    update_list(uid, list_id, body.model_dump(exclude_none=True))
    return {"message": "Lista atualizada com sucesso"}

@router.post("/users/{uid}/lists/{list_id}/books")
def add_book_route(uid: str, list_id: str, body: BookEntryModel):
    add_book_to_list(uid, list_id, body.bookIsbn)
    return {"message": "Livro adicionado com sucesso"}

@router.delete("/users/{uid}/lists/{list_id}/books/{book_isbn}")
def remove_book_route(uid: str, list_id: str, book_isbn: str):
    remove_book_from_list(uid, list_id, book_isbn)
    return {"message": "Livro removido com sucesso"}

@router.delete("/users/{uid}/lists/{list_id}")
def delete_list_route(uid: str, list_id: str):
    delete_list(uid, list_id)
    return {"message": "Lista deletada com sucesso"}