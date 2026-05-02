from firebase.config import db
from firebase_admin import firestore
from datetime import datetime, timezone

def create_location(uid: str, data: dict):
    """
    Função responsável por salvar um novo Ponto Literário (local) no banco de dados.
    Antes de salvar, ela verifica se já existe outro local cadastrado exatamente na mesma posição (mesma latitude e longitude).
    """
    
    # 1. BLOQUEIO DE DUPLICATAS: Busca no banco se já existe um documento com essa latitude e longitude
    lat = data.get("latitude")
    lon = data.get("longitude")
    
    # Fazemos uma query (consulta) na coleção 'locations'
    existing_locations = db.collection("locations").where("latitude", "==", lat).where("longitude", "==", lon).limit(1).stream()
    
    # Se o loop rodar pelo menos uma vez, significa que achou um local com as mesmas coordenadas
    for _ in existing_locations:
        return "DUPLICATE" # Retorna a tag de erro para a rota avisar o usuário

    # 2. SALVAR NOVO LOCAL: Se chegou aqui, não é duplicado.
    # Injetamos o ID do usuário que criou o local e a data/hora atual no formato ISO
    data["criadoPor"] = uid
    data["dataCriacao"] = datetime.now(timezone.utc).isoformat()
    
    # Adicionamos na coleção 'locations' do Firestore
    _, doc_ref = db.collection("locations").add(data)
    
    # Retornamos apenas o ID gerado automaticamente pelo banco
    return doc_ref.id

def get_all_locations():
    """
    Função que busca e retorna absolutamente todos os locais salvos no banco.
    Útil para pintar todos os pins de uma vez no mapa do aplicativo.
    """
    docs = db.collection("locations").stream()
    locations = []
    
    # Iteramos sobre todos os documentos encontrados, pegamos o ID gerado pelo banco e juntamos com os dados (nome, etc)
    for doc in docs:
        locations.append({"id": doc.id, **doc.to_dict()})
        
    return locations

def get_location(location_id: str):
    """
    Busca os detalhes de um local específico através do seu ID único.
    """
    doc = db.collection("locations").document(location_id).get()
    
    # Se o documento não existir, retorna vazio (None)
    if not doc.exists:
        return None
        
    return {"id": doc.id, **doc.to_dict()}

def update_location(location_id: str, data: dict):
    """
    Atualiza informações de um local que já existe (ex: mudou de endereço ou atualizou a foto).
    """
    doc = db.collection("locations").document(location_id).get()
    if not doc.exists:
        return False
        
    db.collection("locations").document(location_id).update(data)
    return True

def delete_location(uid: str, location_id: str):
    """
    Deleta permanentemente um local do mapa.
    Possui regra de segurança: Apenas a pessoa que criou o local tem permissão para deletá-lo.
    """
    doc = db.collection("locations").document(location_id).get()
    
    if not doc.exists:
        return "NOT_FOUND" # Local não existe no banco
    
    # Pega os dados atuais do local do banco de dados
    doc_data = doc.to_dict()
    
    # REGRA DE SEGURANÇA: Verifica se o 'uid' (quem tá chamando a API) é igual ao 'criadoPor' salvo no banco
    if doc_data.get("criadoPor") != uid:
        return "UNAUTHORIZED" # Sem permissão
        
    # Se for o próprio criador, deleta o documento
    db.collection("locations").document(location_id).delete()
    return "SUCCESS"
