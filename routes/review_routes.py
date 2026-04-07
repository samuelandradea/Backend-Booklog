from fastapi import APIRouter
from repositories.review_repository import create_review, get_reviews, get_review, update_review, delete_review
from pydantic import BaseModel
from typing import Optional

class ReviewModel(BaseModel):
    bookIsbn: str
    nomeLivro: str
    nomeAutor: str
    nota: float
    resenha: str

class ReviewUpdateModel(BaseModel):
    nota: Optional[float] = None
    resenha: Optional[str] = None

router = APIRouter()

@router.post("/users/{uid}/reviews")
def create_review_route(uid: str, body: ReviewModel):
    create_review(uid, body.model_dump())
    return {"message": "Review criada com sucesso"}

@router.get("/users/{uid}/reviews")
def get_reviews_route(uid: str):
    return get_reviews(uid)

@router.get("/users/{uid}/reviews/{review_id}")
def get_review_route(uid: str, review_id: str):
    return get_review(uid, review_id)

@router.put("/users/{uid}/reviews/{review_id}")
def update_review_route(uid: str, review_id: str, body: ReviewUpdateModel):
    update_review(uid, review_id, body.model_dump(exclude_none=True))
    return {"message": "Review atualizada com sucesso"}

@router.delete("/users/{uid}/reviews/{review_id}")
def delete_review_route(uid: str, review_id: str):
    delete_review(uid, review_id)
    return {"message": "Review deletada com sucesso"}