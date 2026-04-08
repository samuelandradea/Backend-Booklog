from fastapi import APIRouter, HTTPException
from repositories.review_repository import create_review, get_reviews, get_review, update_review, delete_review
from pydantic import BaseModel, Field
from typing import Optional

class ReviewModel(BaseModel):
    bookIsbn: str
    nomeLivro: str
    nomeAutor: str
    nota: float = Field(ge=0, le=5)
    resenha: str

class ReviewUpdateModel(BaseModel):
    nota: Optional[float] = Field(default=None, ge=0, le=5)
    resenha: Optional[str] = None

router = APIRouter()

@router.post("/users/{uid}/reviews", status_code=201)
def create_review_route(uid: str, body: ReviewModel):
    review_id = create_review(uid, body.model_dump())
    return {"message": "Review criada com sucesso", "reviewId": review_id}

@router.get("/users/{uid}/reviews")
def get_reviews_route(uid: str):
    return get_reviews(uid)

@router.get("/reviews/{review_id}")
def get_review_route(review_id: str):
    review = get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    return review

@router.put("/reviews/{review_id}")
def update_review_route(review_id: str, body: ReviewUpdateModel):
    updated = update_review(review_id, body.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    return {"message": "Review atualizada com sucesso"}

@router.delete("/users/{uid}/reviews/{review_id}")
def delete_review_route(uid: str, review_id: str):
    deleted = delete_review(uid, review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    return {"message": "Review deletada com sucesso"}