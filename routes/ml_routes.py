# routes/ml_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from repositories.ml_repository import get_recomendacoes, get_recomendacoes_por_autor
from repositories.user_repository import get_user

router = APIRouter()


class RecomendacaoBody(BaseModel):
    generos: list[str]
    top_n: Optional[int] = 10


@router.post("/users/{uid}/recomendacoes")
def recomendar_para_usuario(uid: str, body: RecomendacaoBody):
    """
    Rota principal — recebe os gêneros do usuário e retorna livros recomendados.
    O front passa os genres que já buscou do Firebase.
    """
    resultado = get_recomendacoes(body.generos, body.top_n)

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma recomendação encontrada para os gêneros informados"
        )

    return {"recomendacoes": resultado, "total": len(resultado)}


@router.post("/users/{uid}/recomendacoes/autor/{nome_autor}")
def recomendar_por_autor(uid: str, nome_autor: str, body: RecomendacaoBody):
    """
    Escopo restrito — recomenda dentro da obra de um autor específico.
    Ex: "quero livros de Stephen King que combinem com meu gosto"
    """
    resultado = get_recomendacoes_por_autor(body.generos, nome_autor, body.top_n)

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum livro encontrado para o autor '{nome_autor}' com esses gêneros"
        )

    return {"recomendacoes": resultado, "autor": nome_autor, "total": len(resultado)}