from firebase.config import db

def create_review(uid: str, data: dict):
    db.collection("users").document(uid).collection("reviews").add(data)

def get_reviews(uid: str):
    docs = db.collection("users").document(uid).collection("reviews").stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def get_review(uid: str, review_id: str):
    doc = db.collection("users").document(uid).collection("reviews").document(review_id).get()
    return {"id": doc.id, **doc.to_dict()}

def update_review(uid: str, review_id: str, data: dict):
    db.collection("users").document(uid).collection("reviews").document(review_id).update(data)

def delete_review(uid: str, review_id: str):
    db.collection("users").document(uid).collection("reviews").document(review_id).delete()