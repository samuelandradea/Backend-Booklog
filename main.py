from fastapi import FastAPI
from firebase import config

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Booklog API"}