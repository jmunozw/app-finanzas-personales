import os, json

def get_ruta_json():
    return os.path.join("datos","movimientos.json")

def cargar_movimientos():
    ruta = get_ruta_json()

    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        #Archivo vacío o corrupto -> empezamos de cero
        return []
    
def guardar_movimientos(movimientos):
    ruta = get_ruta_json()
    os.makedirs(os.path.dirname(ruta), exist_ok=True) #asegura /datos
    
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(movimientos, archivo, ensure_ascii=False, indent=4)






