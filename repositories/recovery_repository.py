import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_admin import auth as firebase_auth

# Armazena os códigos temporariamente em memória {email: codigo}
codigos_recuperacao = {}

def gerar_codigo() -> str:
    """Gera um código aleatório de 6 dígitos."""
    return str(random.randint(100000, 999999))

def enviar_email_recuperacao(email: str) -> str:
    """Gera um código e envia por email. Retorna o código gerado."""
    codigo = gerar_codigo()
    codigos_recuperacao[email] = codigo

    message = Mail(
        from_email=os.getenv("GMAIL_USER"),
        to_emails=email,
        subject="Código de recuperação - Booklog",
        plain_text_content=f"""
Olá!

Seu código de recuperação do Booklog é:

{codigo}

Este código é válido por 10 minutos.
Se você não solicitou a recuperação, ignore este email.

Equipe Booklog
        """
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)

    return codigo

def verificar_codigo(email: str, codigo: str) -> bool:
    """Verifica se o código informado bate com o armazenado."""
    return codigos_recuperacao.get(email) == codigo

def remover_codigo(email: str):
    """Remove o código após uso."""
    codigos_recuperacao.pop(email, None)
    
def redefinir_senha_firebase(email: str, nova_senha: str):
    """Redefine a senha do usuário no Firebase Auth pelo email."""
    usuario = firebase_auth.get_user_by_email(email)
    firebase_auth.update_user(usuario.uid, password=nova_senha)