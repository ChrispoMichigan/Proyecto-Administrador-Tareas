import json
from datetime import date

#
# Estructura de dato data
#

data = {
    "data" : {
        "id": 1,
        "titulo": "hola",
        "fecha": "2013-10-21",
        "estado": False,
        "prioridad": False
    }
}

print(json.dumps(data['data']))

#
# Cambiar dato de data
#

data['data']['titulo'] = "Cambiar titulo"

print(json.dumps(data['data']))

#
# Cambiar fecha fecha
#

fecha = date(2025, 9, 1)

data['data']['fecha'] = str(fecha)

print(json.dumps(data['data']))


