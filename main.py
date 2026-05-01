from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from firebase import config
from routes.user_routes import router as user_router
from routes.search_routes import router as search_router
from routes.book_routes import router as book_routes
from routes.review_routes import router as review_router
from routes.recovery_routes import router as recovery_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(search_router)
app.include_router(review_router)
app.include_router(book_routes)
app.include_router(recovery_router)

@app.get("/")
def root():
    return {"message": "Booklog API"}