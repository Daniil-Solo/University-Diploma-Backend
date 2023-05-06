from fastapi import FastAPI
from uvicorn import run

from src.university_structure.router import router as university_structure_router

app = FastAPI(title="ПГНИУ: Цифровой помощник", )

app.include_router(university_structure_router)

if __name__ == "__main__":
    run("app:app", host="127.0.0.1", port=5001, reload=True)
