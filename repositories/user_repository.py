from firebase.config import db

def create_user(uid: str, data: dict):
    doc_ref = db.collection("users").document(uid)
    doc_ref.set(data)

def get_user(uid: str):
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()
    return doc.to_dict()

def update_user(uid: str, data: dict):
    doc_ref = db.collection("users").document(uid)
    doc_ref.update(data)

def delete_user(uid: str):
    doc_ref = db.collection("users").document(uid)
    doc_ref.delete()