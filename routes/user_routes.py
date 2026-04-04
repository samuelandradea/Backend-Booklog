from fastapi import APIRouter
from repositories.user_repository import create_user, get_user, update_user, delete_user

router = APIRouter()

@router.post("/users/{uid}")#CREATE
def create_user_route(uid: str, data: dict):
    create_user(uid, data)
    return {"message": "Usuário criado com sucesso"}

@router.get("/users/{uid}")#READ
def get_user_route(uid: str):
    user = get_user(uid)
    return user

@router.put("/users/{uid}")#UPDATE
def update_user_route(uid: str, data: dict):
    update_user(uid, data)
    return {"message": "Usuário editado com sucesso"}

@router.delete("/users/{uid}")#DELETE
def delete_user_route(uid: str):
    delete_user(uid)
    return {"message": "Usuário deletado com sucesso"}
