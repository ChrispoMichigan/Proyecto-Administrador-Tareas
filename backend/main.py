import json
from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel

# python -m uvicorn main:app --reload

app = FastAPI()

class Data():
    def __init__(self, id=None, titulo=None, fecha=None, estado=False, prioridad=False):
        self.id = id
        self.titulo = titulo
        self.fecha = fecha
        self.estado = estado
        self.prioridad = prioridad

class Nodo:
    def __init__(self, datos=None):
        self.datos = Data() if datos is None else datos
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.head = None

    def insertar_al_final(self, datos):
        # datos debe ser una instancia de Data
        nuevo_nodo = Nodo(datos)

        if self.head is None:
            self.head = nuevo_nodo
            return {"Success": "Tarea creada"}

        actual = self.head
        while actual.siguiente:
            actual = actual.siguiente

        actual.siguiente = nuevo_nodo
        return {"Success": "Tarea creada"}

    def eliminar_tarea(self, id):
        if self.head is None:
            return {"Error": "No hay tareas"}

        if self.head.datos.id == id:
            self.head = self.head.siguiente
            return {"Success": f"Tarea con id {id} eliminada"}

        actual = self.head
        while actual.siguiente and actual.siguiente.datos.id != id:
            actual = actual.siguiente

        if actual.siguiente:
            actual.siguiente = actual.siguiente.siguiente
            return {"Success": f"Tarea con id {id} eliminada"}
        
        # Caso donde el ID no existe
        return {"Error": f"No se encontró tarea con id {id}"}

    def buscar(self, id):
        actual = self.head

        while actual:
            if actual.datos.id == id:
                return actual.datos
            actual = actual.siguiente

        return None

    def obtenerTodasLasTareas(self):
        actual = self.head

        if actual is None:
            return {"Error": "No hay tareas"}

        elementos = []

        while actual:
            elementos.append({"id": actual.datos.id, "titulo": actual.datos.titulo, "fecha": actual.datos.fecha, "estado": actual.datos.estado, "prioridad": actual.datos.prioridad})
            actual = actual.siguiente

        return elementos
    
    def cambiarEstadoTarea(self, id):
        data = self.buscar(id)
        if data is None:
            return {"Error": f"No se encontró tarea con id {id}"}
        
        if data.estado:
            data.estado = False
            return {"Sucess" : "Estado cambiado a falso"}
        data.estado = True
        return {"Sucess" : "Estado cambiado a verdadero"}
    
    def cambiarPrioridadTarea(self, id):
        data = self.buscar(id)
        if data is None:
            return {"Error": f"No se encontró tarea con id {id}"}
        
        if data.prioridad:
            data.prioridad = False
            return {"Sucess" : "Prioridad cambiada a falso"}
        data.prioridad = True
        return {"Sucess" : "Prioridad cambiada a verdadero"}


lista_tareas = ListaEnlazada()
control_id = 0

class TaskCreate(BaseModel):
    titulo: str
    fecha: str
    estado: bool
    prioridad: bool

@app.post("/createTask")
def createTask(task: TaskCreate):

    # print(f"Título: {task.titulo}")
    # print(f"Fecha: {task.fecha}")
    # print(f"Estado: {task.estado}")
    # print(f"Prioridad: {task.prioridad}")

    global control_id
    newTask = Data()
    newTask.id = control_id + 1
    control_id = control_id + 1
    newTask.titulo = task.titulo
    newTask.fecha = task.fecha
    newTask.estado = task.estado
    newTask.prioridad = task.prioridad

    response = lista_tareas.insertar_al_final(newTask)
    return response

@app.get("/getAllTasks")
def getAllTasks():
    response = lista_tareas.obtenerTodasLasTareas()
    return response

class TaskId(BaseModel):
    id: int

@app.post("/deleteTaskById")
def deleteTaskById(task : TaskId):
    response = lista_tareas.eliminar_tarea(task.id)
    return response

@app.post("/changeTaskStatusById")
def changeTaskStatusById(task : TaskId):
    response = lista_tareas.cambiarEstadoTarea(task.id)
    return response

@app.post("/changeTaskPriorityById")
def changeTaskPriorityById(task : TaskId):
    response = lista_tareas.cambiarPrioridadTarea(task.id)
    return response

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}



# @app.get("/getAllTasks")
# def read_root():
#     data = {
#         "data": [
#             {
#                 "id": 1,
#                 "titulo": "Tirar basura",
#                 "fecha": "2025-09-01",
#                 "estado": False,
#                 "prioridad": False
#             },
#             {
#                 "id": 2,
#                 "titulo": "Lavar",
#                 "fecha": "2025-09-03",
#                 "estado": False,
#                 "prioridad": False
#             },
#             {
#                 "id": 3,
#                 "titulo": "Llamar Juan",
#                 "fecha": "2025-09-05",
#                 "estado": False,
#                 "prioridad": False
#             },
#             {
#                 "id": 4,
#                 "titulo": "Comprar Sopa",
#                 "fecha": "2025-09-08",
#                 "estado": False,
#                 "prioridad": False
#             }
#         ]
#     }

#     return data

