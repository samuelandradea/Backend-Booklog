# Booklog — Backend API

Backend do aplicativo **Booklog**, desenvolvido com **FastAPI** (Python) e **Firebase Firestore** como banco de dados. Deployado no **Railway**.

---

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/) — framework web para Python
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) — integração com Firestore
- [Supabase](https://supabase.com/) — armazenamento de fotos de perfil
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [Railway](https://railway.app/) — plataforma de deploy

---

## 📁 Estrutura do Projeto

```
PISI3/
├── main.py                      # Ponto de entrada da aplicação
├── firebase/
│   └── config.py                # Configuração do Firebase Admin SDK
├── routes/
│   ├── book_routes.py           # Rotas de livros
│   ├── user_routes.py           # Rotas de usuários
│   ├── review_routes.py         # Rotas de avaliações
│   ├── list_routes.py           # Rotas de listas de leitura
│   ├── search_routes.py         # Rotas de pesquisa
│   ├── location_routes.py       # Rotas de pontos literários
│   ├── friendship_routes.py     # Rotas de amizades
│   └── recovery_routes.py       # Rotas de recuperação de senha
└── repositories/
    ├── book_repository.py       # Operações no Firestore para livros
    ├── user_repository.py       # Operações no Firestore para usuários
    ├── review_repository.py     # Operações no Firestore para avaliações
    ├── list_repository.py       # Operações no Firestore para listas
    ├── search_repository.py     # Operações de busca no Firestore
    ├── location_repository.py   # Operações no Firestore para locais
    ├── friendship_repository.py # Operações no Firestore para amizades
    └── recovery_repository.py   # Operações de recuperação de senha
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
| `GET` | `/books/{isbn}` | Busca um livro pelo ISBN |
| `GET` | `/authors/{nome_autor}/books` | Lista livros de um autor |

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

### Listas de Leitura
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/lists` | Cria uma nova lista |
| `GET` | `/lists/{list_id}` | Busca uma lista pelo ID |
| `GET` | `/users/{uid}/lists` | Lista todas as listas de um usuário |
| `PUT` | `/lists/{list_id}` | Atualiza o nome de uma lista |
| `POST` | `/lists/{list_id}/books` | Adiciona um livro à lista |
| `DELETE` | `/lists/{list_id}/books/{book_isbn}` | Remove um livro da lista |
| `DELETE` | `/lists/{list_id}` | Deleta uma lista |

### Pontos Literários
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/users/{uid}/locations` | Cadastra um novo ponto literário |
| `GET` | `/locations` | Lista todos os pontos literários |
| `GET` | `/locations/{location_id}` | Busca um ponto pelo ID |
| `PUT` | `/locations/{location_id}` | Atualiza um ponto |
| `DELETE` | `/users/{uid}/locations/{location_id}` | Deleta um ponto |
| `POST` | `/suggestions` | Envia sugestão de novo local |

### Amizades
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/users/{uid}/follow/{target_uid}` | Seguir um usuário |
| `DELETE` | `/users/{uid}/unfollow/{target_uid}` | Deixar de seguir |
| `GET` | `/users/{uid}/following` | Lista usuários seguidos |

### Pesquisa
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/search?q={termo}` | Busca usuários, livros e autores |

### Recuperação de Senha
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/recovery/send-code` | Envia código de recuperação por e-mail |
| `POST` | `/recovery/verify-code` | Verifica o código informado |
| `POST` | `/recovery/reset-password` | Redefine a senha |

---

## ⚙️ Como rodar localmente

### Pré-requisitos

- Python 3.12+
- Conta no [Firebase](https://firebase.google.com/) com um projeto criado
- Conta no [Supabase](https://supabase.com/) com um bucket de storage criado
- Conta no [SendGrid](https://sendgrid.com/) para envio de e-mails de recuperação

### 1. Clone o repositório

```bash
git clone https://github.com/samuelandradea/PISI3.git
cd PISI3/PISI3
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Firebase — credenciais da conta de serviço
# Acesse: Firebase Console → Configurações do projeto → Contas de serviço → Gerar nova chave privada
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=seu-project-id
FIREBASE_PRIVATE_KEY_ID=seu-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@seu-projeto.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=seu-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/...

# SendGrid — para envio de e-mails de recuperação de senha
# Acesse: sendgrid.com → Settings → API Keys → Create API Key
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
GMAIL_USER=seu-email@gmail.com

# Supabase — para armazenamento de fotos de perfil
# Acesse: supabase.com → seu projeto → Settings → API
SUPABASE_URL=https://xxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> ⚠️ **Nunca commite o `.env` no repositório.** Certifique-se de que ele está no `.gitignore`.

### 4. Inicie o servidor

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.
A documentação interativa estará em `http://localhost:8000/docs`.

---

## 🔥 Configuração do Firebase

1. Acesse o [Firebase Console](https://console.firebase.google.com/)
2. Selecione seu projeto → **Configurações do projeto** → **Contas de serviço**
3. Clique em **Gerar nova chave privada** — isso baixa um arquivo `.json`
4. Copie os valores do `.json` para as variáveis de ambiente descritas acima

---

## 👥 Time

Projeto desenvolvido para a disciplina de **DSI / PISI3 / ESSI1** — UFRPE.