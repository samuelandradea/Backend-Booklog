from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.recovery_repository import enviar_email_recuperacao, verificar_codigo, remover_codigo, redefinir_senha_firebase

router = APIRouter()

class RecoveryEmailModel(BaseModel):
    email: str

class RecoveryCodeModel(BaseModel):
    email: str
    codigo: str

class NewPasswordModel(BaseModel):
    email: str
    codigo: str
    nova_senha: str

@router.post("/recovery/send-code")
def send_recovery_code(body: RecoveryEmailModel):
    """Envia um código de 6 dígitos para o email informado."""
    try:
        enviar_email_recuperacao(body.email)
        return {"message": f"Código enviado para {body.email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {str(e)}")

@router.post("/recovery/verify-code")
def verify_recovery_code(body: RecoveryCodeModel):
    """Verifica se o código informado é válido."""
    if not verificar_codigo(body.email, body.codigo):
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")
    return {"message": "Código válido"}

@router.post("/recovery/reset-password")
def reset_password(body: NewPasswordModel):
    """Verifica o código e redefine a senha via Firebase Admin."""
    if not verificar_codigo(body.email, body.codigo):
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")
    remover_codigo(body.email)
    return {"message": "Senha redefinida com sucesso"}

@router.post("/recovery/reset-password")
def reset_password(body: NewPasswordModel):
    """Verifica o código e redefine a senha via Firebase Admin."""
    if not verificar_codigo(body.email, body.codigo):
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")
    try:
        redefinir_senha_firebase(body.email, body.nova_senha)
        remover_codigo(body.email)
        return {"message": "Senha redefinida com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao redefinir senha: {str(e)}")