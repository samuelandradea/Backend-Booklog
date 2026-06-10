from firebase.config import db
from datetime import datetime, timezone
import uuid

def create_review(uid: str, data: dict):
    # Adiciona metadados antes de salvar
    data["userId"] = uid
    data["dataCriacao"] = datetime.now(timezone.utc).isoformat()
    
    # Gera um ID único para a review
    review_id = str(uuid.uuid4())
    
    # Salva como subcoleção do usuário
    db.collection("users").document(uid).collection("reviews").document(review_id).set(data)
    
    return review_id

def get_reviews(uid: str):
    # Busca todas as reviews da subcoleção do usuário
    docs = db.collection("users").document(uid).collection("reviews").stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def get_review(uid: str, review_id: str):
    doc = db.collection("users").document(uid).collection("reviews").document(review_id).get()
    if not doc.exists:
        return None
    return {"id": doc.id, **doc.to_dict()}

def update_review(uid: str, review_id: str, data: dict):
    doc_ref = db.collection("users").document(uid).collection("reviews").document(review_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.update(data)
    return True

def delete_review(uid: str, review_id: str):
    doc_ref = db.collection("users").document(uid).collection("reviews").document(review_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True