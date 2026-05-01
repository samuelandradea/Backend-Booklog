from firebase.config import db
from datetime import datetime

def create_list(list_id: str, data: dict):
    # Adiciona a data de criação automaticamente antes de salvar
    data["createdAt"] = datetime.utcnow().isoformat()
    db.collection("lists").document(list_id).set(data)

def get_list(list_id: str):
    doc = db.collection("lists").document(list_id).get()
    if not doc.exists:
        return None
    return {"id": doc.id, **doc.to_dict()}

def get_lists_by_user(uid: str):
    # Busca todas as listas onde o campo userId é igual ao uid recebido
    docs = db.collection("lists").where("userId", "==", uid).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def add_book_to_list(list_id: str, book_isbn: str):
    doc_ref = db.collection("lists").document(list_id)
    doc = doc_ref.get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    # bookEntries é um dicionário onde a chave é o ISBN e o valor é a data de adição
    book_entries = data.get("bookEntries", {})
    book_entries[book_isbn] = datetime.utcnow().isoformat()
    doc_ref.update({"bookEntries": book_entries})

def remove_book_from_list(list_id: str, book_isbn: str):
    doc_ref = db.collection("lists").document(list_id)
    doc = doc_ref.get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    book_entries = data.get("bookEntries", {})
    # Remove o livro do dicionário se ele existir
    book_entries.pop(book_isbn, None)
    doc_ref.update({"bookEntries": book_entries})

def update_list(list_id: str, data: dict):
    db.collection("lists").document(list_id).update(data)

def delete_list(list_id: str):
    db.collection("lists").document(list_id).delete()