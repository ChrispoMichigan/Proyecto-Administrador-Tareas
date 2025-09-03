
from datetime import date
import json
import tkinter as tk
from tkinter import ttk
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
label2.place(x=550, y=41, height=40)

# estos probablemente deberian se un scroll en lugar de labels :p
style.configure("label.TLabel", background="#E4E2E2", foreground="#000")
label = ttk.Label(master=main, text="placeholder", style="label.TLabel")
label.place(x=550, y=98, height=40)

style.configure("label1.TLabel", background="#E4E2E2", foreground="#000")
label1 = ttk.Label(master=main, text="placeholder", style="label1.TLabel")
label1.place(x=550, y=135, height=40)

#boton para añadir recordatorios que aun no le he hecho la funcion 
btnRecordatorio = ttk.Button(master=main, text="añadir recordatorio", style="button.TButton")
btnRecordatorio.place(x=550, y=207, height=40)


style.configure("button.TButton", background="#E4E2E2", foreground="#000")
style.map("button.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])



style.configure("option_menu.TCombobox", fieldbackground="#E4E2E2", foreground="#000")
option_menu_options = ["prioritarias","recordatorios","pendientes","completadas"]
option_menu_var = tk.StringVar(value="filtros")
option_menu = ttk.Combobox(main, textvariable=option_menu_var, values=option_menu_options, style="option_menu.TCombobox")
option_menu.place(x=480, y=282, width=150, height=40)


#calendario
cal = Calendar(master=main, selectmode='day', date_pattern='dd-mm-yyyy') 
cal.pack(pady=20)


def color_date():
    #obtiene la fecha para poder coloriear la casilla donde se añade una tarea
    fecha_date = cal.selection_get()
    print(f"Fecha seleccionada:", fecha_date)
    
    response = requests.get("http://127.0.0.1:8000/")

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Error:", response.status_code)
    print(len(data['data']))
    for i, dato in enumerate(data['data']):
        print(f'{i}')
        print(dato)

    #aqui se usaria la funcion para añadir tareas a la lista

    
    # year = data ['data']['fecha'] [0:4]
    
    # month = data ['data']['fecha'] [5:7]
    # day = data ['data']['fecha'] [8:-1]
    
    # fecha = date(int(year), int(month), int(day))

    cal.calevent_create(fecha, data['data']['titulo'], "tarea")

    cal.tag_config("tarea", background="red", foreground="white")
    
#renombrar a añadir tarea depues
btn = ttk.Button(master=main, text="colorear casilla", command=color_date)
btn.pack(pady=10)

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

main.mainloop()