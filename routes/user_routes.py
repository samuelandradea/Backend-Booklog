from fastapi import APIRouter
from repositories.user_repository import create_user, get_user, update_user, delete_user
from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    name: str
    email: str
    gender: str
    birthDate: str
    genres: list[str] = []
    friendIds: list[str] = []
    listIds: list[str] = []
    reviewIds: list[str] = []

router = APIRouter()

@router.post("/users/{uid}")#CREATE
def create_user_route(uid: str, body: UserModel):
    create_user(uid, body.model_dump())
    return {"message": "Usuário criado com sucesso"}

@router.get("/users/{uid}")#READ
def get_user_route(uid: str):
    user = get_user(uid)
    return user

@router.put("/users/{uid}")#UPDATE
def update_user_route(uid: str, body: UserModel):
    update_user(uid, body.model_dump())
    return {"message": "Usuário atualizado com sucesso"}

@router.delete("/users/{uid}")#DELETE
def delete_user_route(uid: str):
    delete_user(uid)
    return {"message": "Usuário deletado com sucesso"}
