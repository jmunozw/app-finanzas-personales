import os, json
from modelos.movimiento import Movimiento

def cargar_movimientos():
    ruta = os.path.join("datos","movimientos.json")
    if os.path.exists(ruta):
        with open(ruta,"r",encoding="utf-8") as archivo:
            return json.load(archivo)
    else:
        return []

def guardar_movimientos(movimientos):
    ruta = os.path.join("datos","movimientos.json")
    with open(ruta,"w",encoding="utf-8") as archivo:
        json.dump(movimientos,archivo,ensure_ascii=False, indent=4)


if __name__ == "__main__":

    movimientos = cargar_movimientos()

    while(True):
        print("---------- Dinero Quest ----------")
        print("1. Añadir un movimiento")
        print("2. Ver movimientos")
        print("3. Ver balance")
        print("4. Salir")

        opcion = input("Elige un opción: ").strip()

        if opcion == "1":
            print("----- Tipo de Movimiento -----")
            print("1. Ingreso")
            print("2. Gasto")

            opcionTipo = input("Elige el tipo de movimiento:").strip()

            if opcionTipo == "1":
                tipo = "ingreso"
            elif opcionTipo == "2":
                tipo = "gasto"
            else:
                print("Opcion no valida.")
                continue

            print("----- Cantidad -----")
            
            cantidad = input("Introduce la cantidad: ")
            cantidad = float(cantidad)


            categoria = input("Introduce la categoria: ").strip()
            
            opcionFecha = input("¿Quieres indicar una fecha? (s/n): ").strip()

            if opcionFecha == "s":
                fecha = input("Introduce la fecha (YYYY-mm-dd): ").strip()
            else:
                fecha = None

            mov = Movimiento(tipo,cantidad,categoria,fecha)
            print("✅ Movimiento registrado:")
            print(mov.to_dict())
            movimientos.append(mov.to_dict())
            guardar_movimientos(movimientos)


        elif opcion == "2":
            if not movimientos:
                print("💤 No hay movimientos que mostrar")
            else:
                for movimiento in movimientos:
                    print(f"{movimiento['fecha']} {movimiento['tipo']}  -  {movimiento['cantidad']}  -  {movimiento['categoria']}")
        elif opcion == "3":
            totIngresos, totGastos = 0, 0
            for movimiento in movimientos:
                if movimiento["tipo"] == "ingreso":
                    totIngresos += float(movimiento["cantidad"])
                else:
                    totGastos += float(movimiento["cantidad"])
            
            print(f"📈 Ingresos: {totIngresos} €")
            print(f"📉 Gastos:   {totGastos} €")
            print(f"💰 Balance final: {totIngresos - totGastos} €")

        elif opcion == "4":
            print("Salir del progrma")
            break
        else:
            print("Opción no válida.")