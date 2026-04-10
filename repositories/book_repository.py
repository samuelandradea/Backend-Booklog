from firebase.config import db

def get_books():
    docs = db.collection("books").stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def get_book(isbn: str):
    docs = db.collection("books").where("isbn13", "==", int(isbn)).limit(1).stream()
    for doc in docs:
        return {"id": doc.id, **doc.to_dict()}
    return None