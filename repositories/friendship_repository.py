from firebase.config import db
from firebase_admin import firestore
 
 
def follow_user(uid: str, target_uid: str):
    doc_ref = db.collection("users").document(uid)
    doc_ref.update({"friendIds": firestore.ArrayUnion([target_uid])})
 
 
def unfollow_user(uid: str, target_uid: str):
    doc_ref = db.collection("users").document(uid)
    doc_ref.update({"friendIds": firestore.ArrayRemove([target_uid])})
 
 
def get_following(uid: str):
    doc = db.collection("users").document(uid).get()
    user_data = doc.to_dict()
 
    if not user_data or not user_data.get("friendIds"):
        return []
 
    friends = []
    for friend_id in user_data["friendIds"]:
        friend_doc = db.collection("users").document(friend_id).get()
        if friend_doc.exists:
            data = friend_doc.to_dict()
            data["id"] = friend_id
            friends.append(data)
 
    return friends