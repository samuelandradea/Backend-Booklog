from firebase.config import db
from firebase_admin import firestore
from datetime import datetime, timezone

def create_review(uid: str, data: dict):
    data["userId"] = uid
    data["dataCriacao"] = datetime.now(timezone.utc).isoformat()

    _, doc_ref = db.collection("reviews").add(data)
    review_id = doc_ref.id

    db.collection("users").document(uid).update({
        "reviewIds": firestore.ArrayUnion([review_id])
    })

    return review_id

def get_reviews(uid: str):
    user_doc = db.collection("users").document(uid).get()
    if not user_doc.exists:
        return []

    review_ids = user_doc.to_dict().get("reviewIds", [])
    if not review_ids:
        return []

    reviews = []
    for review_id in review_ids:
        doc = db.collection("reviews").document(review_id).get()
        if doc.exists:
            reviews.append({"id": doc.id, **doc.to_dict()})

    return reviews

def get_review(review_id: str):
    doc = db.collection("reviews").document(review_id).get()
    if not doc.exists:
        return None
    return {"id": doc.id, **doc.to_dict()}

def update_review(review_id: str, data: dict):
    doc = db.collection("reviews").document(review_id).get()
    if not doc.exists:
        return False
    db.collection("reviews").document(review_id).update(data)
    return True

def delete_review(uid: str, review_id: str):
    doc = db.collection("reviews").document(review_id).get()
    if not doc.exists:
        return False

    db.collection("reviews").document(review_id).delete()

    db.collection("users").document(uid).update({
        "reviewIds": firestore.ArrayRemove([review_id])
    })

    return True