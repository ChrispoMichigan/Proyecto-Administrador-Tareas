import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/getAllTasks")
def read_root():
    data = {
        "data": [
            {
                "id": 1,
                "titulo": "Tirar basura",
                "fecha": "2025-09-01",
                "estado": False,
                "prioridad": False
            },
            {
                "id": 2,
                "titulo": "Lavar",
                "fecha": "2025-09-03",
                "estado": False,
                "prioridad": False
            },
            {
                "id": 3,
                "titulo": "Llamar Juan",
                "fecha": "2025-09-05",
                "estado": False,
                "prioridad": False
            },
            {
                "id": 4,
                "titulo": "Comprar Sopa",
                "fecha": "2025-09-08",
                "estado": False,
                "prioridad": False
            }
        ]
    }

    return data

