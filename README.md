# Booklog — Backend API

Backend do aplicativo **Booklog**, desenvolvido com **FastAPI** (Python) e **Firebase Firestore** como banco de dados. Deployado no **Railway**.

---

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/) — framework web para Python
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) — integração com Firestore
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [Railway](https://railway.app/) — plataforma de deploy

---

## 📁 Estrutura do Projeto

```
PISI3/
├── main.py                  # Ponto de entrada da aplicação
├── firebase/
│   └── config.py            # Configuração do Firebase Admin SDK
├── routes/
│   ├── book_routes.py       # Rotas de livros
│   ├── user_routes.py       # Rotas de usuários
│   ├── review_routes.py     # Rotas de avaliações
│   └── search_routes.py     # Rotas de pesquisa
└── repositories/
    ├── book_repository.py   # Operações no Firestore para livros
    ├── user_repository.py   # Operações no Firestore para usuários
    ├── review_repository.py # Operações no Firestore para avaliações
    └── search_repository.py # Operações de busca no Firestore
```

---

## 🌐 Base URL

```
https://pisi3-production.up.railway.app
```

A documentação interativa da API está disponível em:
```
https://pisi3-production.up.railway.app/docs
```

---

## 📚 Endpoints

### Livros

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/books` | Lista os livros disponíveis |
| `GET` | `/books/{isbn}` | Busca um livro pelo ISBN13 |

### Usuários

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/users/{uid}` | Cria um novo usuário |
| `GET` | `/users/{uid}` | Busca os dados de um usuário |
| `PUT` | `/users/{uid}` | Atualiza os dados de um usuário |
| `DELETE` | `/users/{uid}` | Deleta um usuário |

### Avaliações

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/users/{uid}/reviews` | Cria uma nova avaliação |
| `GET` | `/users/{uid}/reviews` | Lista as avaliações de um usuário |
| `GET` | `/reviews/{review_id}` | Busca uma avaliação pelo ID |
| `PUT` | `/reviews/{review_id}` | Atualiza nota e/ou resenha |
| `DELETE` | `/users/{uid}/reviews/{review_id}` | Deleta uma avaliação |

### Pesquisa

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/search?q={termo}` | Busca livros pelo termo informado |

---

## 📝 Modelos de Dados

### UserModel
```json
{
  "name": "string",
  "email": "string",
  "gender": "string",
  "birthDate": "string",
  "genres": ["string"],
  "friendIds": ["string"],
  "listIds": ["string"],
  "reviewIds": ["string"]
}
```

### ReviewModel
```json
{
  "bookIsbn": "string",
  "nomeLivro": "string",
  "nomeAutor": "string",
  "nota": 0.0,
  "resenha": "string"
}
```

### ReviewUpdateModel
```json
{
  "nota": 0.0,
  "resenha": "string"
}
```

---

## ⚙️ Como rodar localmente

### Pré-requisitos
- Python 3.10+
- Credenciais do Firebase (arquivo `serviceAccountKey.json`)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/samuelandradea/PISI3.git

# Entre na pasta do projeto
cd PISI3/PISI3

# Instale as dependências
pip install -r requirements.txt

# Rode o servidor
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

---

## 🔥 Configuração do Firebase

Configure as credenciais do Firebase criando o arquivo `firebase/serviceAccountKey.json` com as credenciais do seu projeto Firebase.

---

## 👥 Time

Projeto desenvolvido para a disciplina de **DSI / PISI3 / ESSI1** - UFRPE.