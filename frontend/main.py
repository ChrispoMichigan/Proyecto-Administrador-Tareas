
from datetime import date
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import Calendar
import requests


main = tk.Tk()
main.title("Main Window")
main.config(bg="#E4E2E2")
main.geometry("700x700")


style = ttk.Style(main)
style.theme_use("clam")


# label principal de recordatorios, simplemente dice "Recordatorios"
style.configure("label2.TLabel", background="#E4E2E2", foreground="#000")
label2 = ttk.Label(master=main, text="Recordatorios", style="label2.TLabel")
label2.place(x=550, y=150, height=40)

#scroll para recordatorios
# Crear una Listbox para los recordatorios
listbox = tk.Listbox(main, height=10, width=30, selectmode=tk.SINGLE)
listbox.place(x=527, y=250)
# Crear una Scrollbar y asociarla a la Listbox
scrollbar = tk.Scrollbar(main, orient="vertical", command=listbox.yview)
scrollbar.place(x=510,y=250,height=164)

# Crear una segunda scrollbar porsi ponen recordatorios muy largos
scrollbar2 = tk.Scrollbar(main, orient="horizontal", command=listbox.xview)
scrollbar2.place(x=510,y=415,width=184)

# Configurar la Listbox para que use las Scrollbar
listbox.config(yscrollcommand=scrollbar.set)
listbox.config(xscrollcommand=scrollbar2.set)



#recordatorios de prueba
for i in range (5):
    listbox.insert(tk.END, f"recordatorio {i}")

def Add_recordatorio():
    #aqui se usaria la funcion para añadir tareas a la lista
    dataR = {
        "data" : {
            "id": 1,
            "titulo": "recordatorio 1",
        }
    }
    recordatorio = simpledialog.askstring("Input", "Ingrese el recordatorio", parent=main)
    if recordatorio :
         dataR ['data']['titulo'] = recordatorio 
         
    else :
        messagebox.showwarning("Error", "No se ingreso recordatorio")

    listbox.insert(tk.END, f" {recordatorio}")


#boton para añadir recordatorios que aun no le he hecho la funcion 
btnRecordatorio = ttk.Button(master=main, text="añadir recordatorio", style="button.TButton",command=Add_recordatorio)
btnRecordatorio.place(x=550, y=207, height=40)


style.configure("button.TButton", background="#E4E2E2", foreground="#000")
style.map("button.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])



style.configure("option_menu.TCombobox", fieldbackground="#E4E2E2", foreground="#000")
option_menu_options = ["todas","prioritarias","pendientes","completadas"]
option_menu_var = tk.StringVar(value="filtros")
option_menu = ttk.Combobox(main, textvariable=option_menu_var, values=option_menu_options, style="option_menu.TCombobox")
option_menu.place(x=180, y=320, width=150, height=40)


#calendario
cal = Calendar(master=main, selectmode='day', date_pattern='dd-mm-yyyy') 
cal.pack(pady=20)


def Add_tarea():
    #obtiene la fecha para poder coloriear la casilla donde se añade una tarea
    fecha_date = cal.selection_get()
    print(f"Fecha seleccionada:", fecha_date)
    

    #aqui se usaria la funcion para añadir tareas a la lista
    data = {
        "titulo": None,
        "fecha": None,
        "estado": False,
        "prioridad": False
    }

    data['fecha'] = str(fecha_date)

    tareaName = simpledialog.askstring("Nombre de la tarea", "Ingrese el nombre de la tarea", parent=main)
    if tareaName :
        data['titulo'] = tareaName
    else :
        messagebox.showwarning("Error", "No se ingreso un nombre")
        return
    
    # year = data ['data']['fecha'] [0:4]
    
    # month = data ['data']['fecha'] [5:7]
    # day = data ['data']['fecha'] [8:-1]
    
    # fecha = date(int(year), int(month), int(day))

    url = "http://127.0.0.1:8000/createTask"
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Se guardo la tarea')

    AddTaskViewsInCalender()
    AddTaskViewsInList()

def AddTaskViewsInCalender():
    url = "http://127.0.0.1:8000/getAllTasks"
    response = requests.get(url)

    if response.status_code != 200:
        print('Error')
    else:
        data = response.json() 

    for task in data:
        # print(task)
        year = int(task['fecha'][:4])
        mes = int(task['fecha'][5:7])
        dia = int(task['fecha'][8:])
        # print(dia)
        fecha = date(year, mes, dia)
        # print(f'{year}, {mes}, {dia}')
        cal.calevent_create(fecha, task['titulo'], "tarea")
        cal.tag_config("tarea", background="red", foreground="white")

btnAdd = ttk.Button(master=main, text="añadir tarea", command=Add_tarea)
btnAdd.pack(pady=10)


#boton para borrar sin comando aun
btnDelete = ttk.Button(master=main, text="BorrarTarea",)
btnDelete.place(relx=0.75, rely=0.65)
#boton para hacer prioridad 
btnPriority = ttk.Button(master=main, text="Establecer como prioridad",)
btnPriority.place(relx=0.75, rely=0.75)

#boton para marcar como completado 
btnCompletado = ttk.Button(master=main, text="Marcar como completado",)
btnCompletado.place(relx=0.75, rely=0.85)


#aqui va una lista de tareas
tk.Label(master=main, text="Tareas:").place(relx=0.2, rely=0.55)
menutareas = tk.Listbox(master=main, width=70, height=12)
menutareas.place(relx= 0.1, rely=0.6)

def AddTaskViewsInList():
    url = "http://127.0.0.1:8000/getAllTasks"
    response = requests.get(url)

    if response.status_code != 200:
        print('Error')
    else:
        data = response.json()

    print(data)

main.mainloop()