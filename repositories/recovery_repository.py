import smtplib
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = email
    msg["Subject"] = "Código de recuperação - Booklog"

    corpo = f"""
    Olá!

    Seu código de recuperação do Booklog é:

    {codigo}

    Este código é válido por 10 minutos.
    Se você não solicitou a recuperação, ignore este email.

    Equipe Booklog
    """
    msg.attach(MIMEText(corpo, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_user, gmail_password)
        smtp.sendmail(gmail_user, email, msg.as_string())

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
