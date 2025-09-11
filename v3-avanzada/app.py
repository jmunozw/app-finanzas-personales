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


# Obtener selección del TreeView
def get_seleccion():
    """Devuelve (index_en_tabla, values_tuple) o None si no hay selección"""
    sels = tv.selection()

    if not sels:
        return None
    
    item_id = sels[0]
    idx = tv.index(item_id)
    values = tv.item(item_id, "values")
    return idx, values

#Actualizar estos de botones
def actualizar_estado_botones():

    sel = get_seleccion()

    if sel is None:
        btn_editar.config(state=tk.DISABLED)
        btn_eliminar.config(state=tk.DISABLED)
        btn_reset_sel.config(state=tk.DISABLED)
    else:
        btn_editar.config(state=tk.NORMAL)
        btn_eliminar.config(state=tk.NORMAL)
        btn_reset_sel.config(state=tk.NORMAL)
    
#Eliminar movimiento seleccionado
def eliminar_seleccionado():
    sel = tv.selection()
    if not sel:
        return

    #Mensaje de confirmación
    ok = messagebox.askyesno("Eliminar","¿Seguro que quieres eliminar el movimiento seleccionado?")
    if not ok:
        return
    
    # Obtenemos indice actual de la fila seleccionada
    item_id = sel[0]
    idx = tv.index(item_id)

    

    #Borramos el movimiento del modelo de memoria
    try:
        movimientos.pop(idx)
    except IndexError:
        #Si algo raro pasa con el índice, salimos con aviso
        messagebox.showwarning("Aviso","No se pudo elminar el elemento seleccionado.")
        return

    # Persistencia y refrescar UI
    guardar_movimientos(movimientos)
    refrescar_lista()
    actualizar_estado_botones()
    feedback_lbl.config(text="🗑️ Movimiento eliminado", fg="orange")

# Eliminar movimiento seleccionado - Atajo teclado Spr/Backspace
def on_key_delete(event):
    eliminar_seleccionado()

#Editar movimiento seleccionado
def editar_seleccionado():
    sel = tv.selection()

    if not sel:
        return
    
    #Obtenemos indice actual de la fila seleccionada
    item_id = sel[0]
    idx = tv.index(item_id)

    try:
        actual = movimientos[idx]
    except IndexError:
        messagebox.showwarning("Aviso","Selección inválida")
        return
    
    # --- Ventana de edición (popup) ---
    top = tk.Toplevel(root)
    top.title("Editar movimiento")
    top.transient(root)
    top.grab_set() # Modal, bloquea interacción fuera del popup.
    top.resizable(False,False) #No redimensionable
    top.configure(padx=10,pady=10)
        
    # Variables locales precargadas
    tipo_local = tk.StringVar(value=actual.get("tipo", "ingreso"))
    cantidad_local = tk.StringVar(value=str(actual.get("cantidad", "")))
    categoria_local = tk.StringVar(value=actual.get("categoria", ""))
    fecha_local = tk.StringVar(value=actual.get("fecha") or "")

    #Layouts simple con grid
    tk.Label(top, text="Tipo:").grid(row=0, column=0, sticky="w", pady=4)
    tk.Label(top, text="Cantidad:").grid(row=1, column=0, sticky="w", pady=4)
    tk.Label(top, text="Categoría:").grid(row=2, column=0, sticky="w", pady=4)
    tk.Label(top, text="Fecha (YYYY-mm-dd):").grid(row=3, column=0, sticky="w", pady=4)

    opt = tk.OptionMenu(top, tipo_local, "ingreso", "gasto")
    opt.grid(row=0, column=1, sticky="ew", pady=4)

    ent_cant = tk.Entry(top, textvariable=cantidad_local)
    ent_cant.grid(row=1, column=1, sticky="ew", pady=4)

    ent_cat = tk.Entry(top, textvariable=categoria_local)
    ent_cat.grid(row=2, column=1, sticky="ew", pady=4)

    ent_fec = tk.Entry(top, textvariable=fecha_local)
    ent_fec.grid(row=3, column=1, sticky="ew", pady=4)

    #Que la segunda columna se estire
    top.grid_columnconfigure(1,weight=1)

    def on_cancelar():
        top.destroy()
        
    def on_guardar():
        # Validación cantidad
        try:
            cant = float(cantidad_local.get().strip())
        except ValueError:
            messagebox.showerror("Cantidad inválida", "La cantidad debe ser un número (usa punto para decimales).")
            ent_cant.focus_set()
            return

        # Actualizar en memoria
        movimientos[idx] = {
            "tipo": tipo_local.get().strip(),
            "cantidad": cant,
            "categoria": categoria_local.get().strip(),
            "fecha": (fecha_local.get().strip() or None),
        }

        # Persistir y refrescar UI
        guardar_movimientos(movimientos)
        refrescar_lista()

        # Reseleccionar la fila editada (si sigue existiendo)
        items = tv.get_children()
        if 0 <= idx < len(items):
            tv.selection_set(items[idx])
            tv.focus(items[idx])
            tv.see(items[idx])

        feedback_lbl.config(text="✏️ Movimiento actualizado", fg="blue")
        top.destroy()

    #Podemos cerrar el popup con Esc
    top.bind("<Escape>", lambda e: on_cancelar())
    #Validamos guardar con Enter
    top.bind("<Return>", lambda e: on_guardar())
    #Validamos cerrar con la X del popup
    top.protocol("WM_DELETE_WINDOW", on_cancelar)

    frm_btns = tk.Frame(top)
    frm_btns.grid(row=4, column=0, columnspan=2, pady=(8, 0), sticky="e")

    tk.Button(frm_btns, text="Guardar", command=on_guardar).pack(side="right", padx=(6, 0))
    tk.Button(frm_btns, text="Cancelar", command=on_cancelar).pack(side="right")
    ent_cant.focus_set()


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

    #Limpiar selección (para evitar botones activos tras refrescar)
    tv.selection_remove(tv.selection())
    actualizar_estado_botones()


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

# Añadimos el vinculo de ejecución al seleccionar un valor del TreeView
tv.bind("<<TreeviewSelect>>", lambda e: actualizar_estado_botones())

#Añadimos atajos de teclado Eliminar movimiento - Spr/Backspace
tv.bind("<Delete>", on_key_delete)
tv.bind("<BackSpace>", on_key_delete)

#Encabezados
tv.heading("fecha", text="Fecha")
tv.heading("tipo", text="Tipo")
tv.heading("cantidad", text="Cantidad")
tv.heading("categoria", text="Categoría")

#Configuramos columnas
tv.column("fecha", anchor="center", width=90, stretch=False)
tv.column("tipo", anchor="center", width=80, stretch=False)
tv.column("cantidad", anchor="e", width=90, stretch=False)
tv.column("categoria", anchor="w", width=120)

#Scrollbar vertical
scroll = ttk.Scrollbar(frmCentral, orient="vertical", command=tv.yview)
tv.configure(yscrollcommand=scroll.set)

tv.grid(row=0, column=0, sticky="nsew")
scroll.grid(row=0,column=1,sticky="ns")

# ----- Panel de acciones (derecha del Treeview) -----
frmAcciones = tk.Frame(frmCentral, bg="#f7f7f7", padx=6, pady=6)
frmAcciones.grid(row=0,column=2,sticky="n", padx=(6,0))

btn_editar = tk.Button(frmAcciones, text="Editar",state=tk.DISABLED, command=editar_seleccionado)
btn_eliminar = tk.Button(frmAcciones, text="Eliminar", state=tk.DISABLED, command=eliminar_seleccionado)
btn_reset_sel = tk.Button(frmAcciones, text="Quitar selección", state=tk.DISABLED)

btn_editar.pack(fill="x",pady=(0,6))
btn_eliminar.pack(fill="x",pady=(0,6))
btn_reset_sel.pack(fill="x")



#Llamamos a refrescar_lista para cargar el TreeView si hubiese movimientos guardados en el JSON
refrescar_lista()
# Llamamos a actualizar_estado_botones para actualizar el estado de los botones de acciones
actualizar_estado_botones()

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