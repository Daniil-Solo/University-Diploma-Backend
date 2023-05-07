from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from src.university_structure.router import router as university_structure_router

app = FastAPI(title="ПГНИУ: Цифровой помощник", )

app.include_router(university_structure_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin"]
)

if __name__ == "__main__":
    run("app:app", host="127.0.0.1", port=5001, reload=True)
