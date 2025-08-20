import tkinter as tk
from tkinter import messagebox
from tkinter import ttk



from servicios.persistencia import cargar_movimientos
from servicios.persistencia import guardar_movimientos


#Cargamos los movimientos existentes
movimientos = cargar_movimientos()

#Ventana principal de Finanzas personales
root = tk.Tk()
root.title("Finanzas v2")
root.geometry("520x520")
root.minsize(480,360)

#Zonas frames
frmSuperior = tk.Frame(root, bg="#f0f0f0", padx=10,pady=10)
frmSuperior.pack(fill="x")

frmCentral = tk.Frame(root, bg="#f7f7f7")
frmCentral.pack(fill="both", expand=True)

frmInferior = tk.Frame(root,bg="#f0f0f0", padx=10, pady=8)
frmInferior.pack(fill="x")

#Variables de estado
tipo_var = tk.StringVar(value="ingreso")
cantidad_var = tk.StringVar(value="")
categoria_var = tk.StringVar(value="")
fecha_var = tk.StringVar(value="")
ingresos_var = tk.StringVar(value="0.00")
gastos_var = tk.StringVar(value="0.00")
balance_var = tk.StringVar(value="0.00")


# Refrescar lista
def refrescar_lista():
    #Limpiamos filas
    for item in tv.get_children():
        tv.delete(item)
    
    #Inserta movimientos actuales
    for mov in movimientos:
        fecha = mov.get("fecha") or "-"
        tipo = mov.get("tipo","")
        #Fuerza a float por si viene como string del JSON
        cantidad = f"{float(mov.get('cantidad',0)):.2f}"
        categoria = mov.get("categoria","")
        tv.insert("","end", values=(fecha, tipo, cantidad, categoria))
    
    #Actualizamos el resumen
    actualizar_resumen()

# Actualizar resumen de ingresos, gastos y balance
def actualizar_resumen():
    tot_ing = 0.0
    tot_gas = 0.0
    
    for mov in movimientos:
        #Validamos que el valor obtenido realmente sea un número, caso contrario se asigna 0.0
        try: 
            cantidad = float(mov.get("cantidad",0))
        except (TypeError, ValueError):
            cantidad = 0.0


        if mov.get("tipo") == "ingreso":
            tot_ing += cantidad
        else:
            tot_gas += cantidad
        
    #Actualizamos las variables de estado para los casos

    ingresos_var.set(f"{tot_ing:.2f}")
    gastos_var.set(f"{tot_gas:.2f}")
    balance_var.set(f"{(tot_ing-tot_gas):.2f}")


# Callback del botón Añadir
def on_add_click():
    tipo = tipo_var.get().strip()
    cant_txt = cantidad_var.get().strip()
    categoria = categoria_var.get().strip()
    fecha = fecha_var.get().strip() or None # Si esta vacío, None

    #Validación básica de cantidad
    try:
        cantidad = float(cant_txt)
    except ValueError:
        messagebox.showerror("Cantidad inválida","La cantidad debe ser un número (usa punto para decimales).")
        return

    movimiento = {
        "tipo": tipo,
        "cantidad": cantidad,
        "categoria": categoria,
        "fecha": fecha
    }

    #Añadimos nuevo movimiento a la lista de movimientos
    movimientos.append(movimiento)

    #Guardamos lista de movimiento actualizada a nuestro JSON
    guardar_movimientos(movimientos)

    #Por ahora se imprime en consola
    print("Movimiento listo: ", movimiento)
    feedback_lbl.config(text="✅ Movimiento guardado.", fg="green")

    #Refrescamos lista de movimientos en la interfaz
    refrescar_lista()

    #Limpiar campos (menos el tipo)
    cantidad_var.set("")
    categoria_var.set("")
    fecha_var.set("")
    ent_cantidad.focus_set()


# Frame Superior - Formulario para rellenar datos (usamos grid dentro de frmSuperior)
#Etiquetas
tk.Label(frmSuperior, text="Tipo", bg="#f0f0f0").grid(row=0,column=0,sticky="w",padx=4,pady=4)
tk.Label(frmSuperior, text="Cantidad", bg="#f0f0f0").grid(row=1,column=0,sticky="w",padx=4,pady=4)
tk.Label(frmSuperior, text="Categoría", bg="#f0f0f0").grid(row=2,column=0,sticky="w",padx=4,pady=4)
tk.Label(frmSuperior, text="Fecha", bg="#f0f0f0").grid(row=3,column=0,sticky="w",padx=4,pady=4)

#Widgets
opciones_tipo = ("ingreso","gasto")
opt_tipo = tk.OptionMenu(frmSuperior, tipo_var, *opciones_tipo)
opt_tipo.grid(row=0,column=1,sticky="w",padx=4,pady=4)

ent_cantidad = tk.Entry(frmSuperior, textvariable=cantidad_var)
ent_cantidad.grid(row=1,column=1,sticky="ew",padx=4,pady=4)

ent_categoria = tk.Entry(frmSuperior, textvariable=categoria_var)
ent_categoria.grid(row=2,column=1,sticky="ew",padx=4,pady=4)

ent_fecha = tk.Entry(frmSuperior,textvariable=fecha_var)
ent_fecha.grid(row=3,column=1,sticky="ew",padx=4,pady=4)

#Botón Añadir
btn_add = tk.Button(frmSuperior, text="Añadir", command=on_add_click)
btn_add.grid(row=4,column=0,columnspan=2,sticky="ew",padx=4,pady=(8,0))

#Que la columna 1 se estire al redimensionar
frmSuperior.grid_columnconfigure(1,weight=1)

# Frame Central - Listado de movimientos

#Treeview + scrollbar en frmCentral(Usamos grid dentro de este frame)
frmCentral.grid_rowconfigure(0,weight=1)
frmCentral.grid_columnconfigure(0,weight=1)


tv = ttk.Treeview(frmCentral,columns=("fecha","tipo","cantidad","categoria"), show="headings")

#Encabezados
tv.heading("fecha", text="Fecha")
tv.heading("tipo", text="Tipo")
tv.heading("cantidad", text="Cantidad")
tv.heading("categoria", text="Categoría")

#Configuramos columnas
tv.column("fecha", anchor="center", width=110, stretch=False)
tv.column("tipo", anchor="center", width=90, stretch=False)
tv.column("cantidad", anchor="e", width=110, stretch=False)
tv.column("categoria", anchor="w", width=180)

#Scrollbar vertical
scroll = ttk.Scrollbar(frmCentral, orient="vertical", command=tv.yview)
tv.configure(yscrollcommand=scroll.set)

tv.grid(row=0, column=0, sticky="nsew")
scroll.grid(row=0,column=1,sticky="ns")

#Llamamos a refrescar_lista para cargar el TreeView si hubiese movimientos guardados en el JSON
refrescar_lista()

# Frame Inferior - Resumen de ingresos, gastos y balance total

lbl_ing = tk.Label(frmInferior, text="Ingresos:")
val_ing = tk.Label(frmInferior, textvariable= ingresos_var)
lbl_gas = tk.Label(frmInferior, text="Gastos:")
val_gas = tk.Label(frmInferior, textvariable= gastos_var)
lbl_bal = tk.Label(frmInferior, text="Balance:")
val_bal = tk.Label(frmInferior, textvariable= balance_var)

lbl_ing.grid(row=0, column=0, sticky="w", padx=4)
val_ing.grid(row=0, column=1, sticky="w", padx=4)
lbl_gas.grid(row=0, column=2, sticky="w", padx=4)
val_gas.grid(row=0, column=3, sticky="w", padx=4)
lbl_bal.grid(row=0, column=4, sticky="w", padx=4)
val_bal.grid(row=0, column=5, sticky="w", padx=4)

#Feedback en la fila 1 del grid
feedback_lbl = tk.Label(frmInferior, text="Listo para añadir movimientos...", bg="#f0f0f0")
feedback_lbl.grid(row=1,column=0,columnspan=6,sticky="w", pady=(6,0))

#Que las columnas respiren un poco si se estira
frmInferior.grid_columnconfigure(5, weight=1)

#UX: foco inicial
ent_cantidad.focus_set()

#Iniciamos el buble principal de la interfaz
root.mainloop()