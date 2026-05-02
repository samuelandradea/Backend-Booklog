from fastapi import APIRouter
from repositories.friendship_repository import follow_user, unfollow_user, get_following
 
router = APIRouter()

 
@router.post("/users/{uid}/follow/{target_uid}")
def follow_user_route(uid: str, target_uid: str):
    follow_user(uid, target_uid)
    return {"message": "Usuário seguido com sucesso"}
 
 
@router.delete("/users/{uid}/unfollow/{target_uid}")
def unfollow_user_route(uid: str, target_uid: str):
    unfollow_user(uid, target_uid)
    return {"message": "Usuário deixado de seguir com sucesso"}
 
 
@router.get("/users/{uid}/following")
def get_following_route(uid: str):
    return get_following(uid)