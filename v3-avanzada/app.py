import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
from tkinter import filedialog
from datetime import datetime



from servicios.persistencia import cargar_movimientos
from servicios.persistencia import guardar_movimientos



#Cargamos los movimientos existentes
movimientos = cargar_movimientos()

#Ventana principal de Finanzas personales
root = tk.Tk()
root.title("Finanzas v2")
root.geometry("540x540")
root.minsize(480,380)

#Zonas frames
frmSuperior = tk.Frame(root, bg="#f0f0f0", padx=10,pady=10)
frmSuperior.pack(fill="x")

frmFiltros = tk.Frame(root, bg="#f0f0f0")
frmFiltros.pack(fill="x")

frmCentral = tk.Frame(root, bg="#f7f7f7")
frmCentral.pack(fill="both", expand=True)

frmInferior = tk.Frame(root,bg="#f0f0f0", padx=10, pady=8)
frmInferior.pack(fill="x")

#Variable global
indices_vista_actual = None

#Variables de estado
tipo_var = tk.StringVar(value="ingreso")
cantidad_var = tk.StringVar(value="")
categoria_var = tk.StringVar(value="")
fecha_var = tk.StringVar(value="")
ingresos_var = tk.StringVar(value="0.00")
gastos_var = tk.StringVar(value="0.00")
balance_var = tk.StringVar(value="0.00")

filtro_cat_var = tk.StringVar(value="")
filtro_mes_var = tk.StringVar(value="")

# Exportar a CSV 
def exportar_csv():
    #Decidimos qué filas exportar (vista completa o filtrada)
    idx = range(len(movimientos)) if indices_vista_actual is None else indices_vista_actual

    #Abrir dialógo "Guardar como..."
    ruta = filedialog.asksaveasfilename(
        title="Guardar archivo como...",
        defaultextension=".csv", 
        filetypes=[("CSV","*.csv"),("Todos los archivos","*.*")]
    )
    
    if not ruta:
        return #Usuario cancelo
    
    try:
        with open(ruta,"w",newline='',encoding="utf-8") as f:
            w = csv.writer(f)
            # Encabezados
            w.writerow(["fecha","tipo","cantidad","categoria"])

            # Filas
            for i in idx:
                mov = movimientos[i]
                fecha = mov.get("fecha") or "-"
                tipo = mov.get("tipo","")
                try:
                    cantidad = float(mov.get("cantidad",0))
                except (TypeError,ValueError):
                    cantidad = 0.0
                categoria = mov.get("categoria","")

                w.writerow([fecha,tipo,f"{cantidad:.2f}",categoria])
            
            # Feedback
            feedback_lbl.config(text="📤 Exportación completada", fg="green")
            messagebox.showinfo("Exportación a CSV", "Archivo exportado correctamente.")
    except Exception as e:
        # Si algo falla, avisa
        messagebox.showerror("Error al exportar", f"No se pudo exportar el CSV.\n\nDetalle: {e}")
        feedback_lbl.config(text="❌ Error al exportar", fg="red")
    



# Filtros - Aplicar filtro
def aplicar_filtros():
    # Si no hay filtros, señalamos "vista completa"
    global indices_vista_actual

    #Validamos entradas de filtros
    cat = filtro_cat_var.get().strip().lower()
    mes = filtro_mes_var.get().strip() or None

    # Validación ligera de mes para que se ingrese correctamente
    if mes and (len(mes) != 7 or mes[4] != "-"):
        messagebox.showwarning("Formato de mes", "Usa 'YYYY-mm' (ej: 2025-09).")
        return

    if not cat and not mes:
        indices_vista_actual = None
    else:
        indices_vista_actual = []

        for i, mov in enumerate(movimientos):
            ok = True

            if cat and cat not in mov.get("categoria","").lower():
                ok = False
            
            if mes:
                fecha = mov.get("fecha")
                if not fecha or len(fecha) < 7 or fecha[:7] != mes:
                    ok = False
            
            if ok:
                indices_vista_actual.append(i)


    # Pintamos en una sola llamada
    refrescar_lista(indices_vista_actual)

    #Total de elementos filtrados, o no.
    total = len(movimientos) if indices_vista_actual is None else len(indices_vista_actual)
    feedback_lbl.config(text=f"🔎 Filtro aplicado: {total} resultados")

# Filtros - Quitar filtros
def quitar_filtros():
    global indices_vista_actual 

    filtro_cat_var.set("")
    filtro_mes_var.set("")

    indices_vista_actual = None
    refrescar_lista(indices_vista_actual)
    
    feedback_lbl.config(text="✨ Filtros quitados")
    filtro_categoria.focus_set()

# Normalizar fecha
def normalizar_fecha(texto_fecha):

    if not texto_fecha:
        return None
    
    fecha = texto_fecha.strip()
    
    #Caso dd/mm/yyyy
    if "/" in fecha:
        try:
            fecha = datetime.strptime(fecha,"%d/%m/%Y")
            return fecha.strftime("%Y-%m-%d")
        except ValueError:
            return None #Fecha no válida
    
    # Caso yyyy-mm-dd
    elif "-" in fecha:
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            return fecha.strftime("%Y-%m-%d")  # La devuelve normalizada
        except ValueError:
            return None
    #Si no cuadra con formato
    else:
        return None

    
    
# Obtener selección del TreeView
def get_seleccion():
    """Devuelve (index_en_tabla, values_tuple) o None si no hay selección"""
    sels = tv.selection()

    if not sels:
        return None
    
    item_id = sels[0]
    idx = int(item_id)
    values = tv.item(item_id, "values")
    return idx, values

#Actualizar estados de botones
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
    global indices_vista_actual
    sel = tv.selection()
    if not sel:
        return

    #Mensaje de confirmación
    ok = messagebox.askyesno("Eliminar","¿Seguro que quieres eliminar el movimiento seleccionado?")
    if not ok:
        return
    
    # Obtenemos indice actual de la fila seleccionada
    item_id = sel[0]
    idx = int(item_id)

    

    #Borramos el movimiento del modelo de memoria
    try:
        movimientos.pop(idx)
    except IndexError:
        #Si algo raro pasa con el índice, salimos con aviso
        messagebox.showwarning("Aviso","No se pudo elminar el elemento seleccionado.")
        return
    
    
    
    # Persistencia y refrescar UI
    guardar_movimientos(movimientos)
    
    aplicar_filtros()
    tv.selection_remove(*tv.selection())
    actualizar_estado_botones()

    feedback_lbl.config(text="🗑️ Movimiento eliminado", fg="orange")

# Quitar seleccion
def quitar_seleccion():
    tv.selection_remove(*tv.selection())
    tv.focus("")
    actualizar_estado_botones()

def on_tree_click_vacio(e):
    #Si se hace click en una zona sin fila, limpia la selección
    if tv.identify_row(e.y) == "":
        quitar_seleccion()

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
    idx = int(item_id)

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
        
        # Validación fecha
        fecha = fecha_local.get().strip()
        fecha_norm = normalizar_fecha(fecha)
        if fecha and not fecha_norm:
            messagebox.showerror("Fecha inválida", "Usa formato dd/mm/yyyy o yyyy-mm-dd.")
            return


        # Actualizar en memoria
        movimientos[idx] = {
            "tipo": tipo_local.get().strip(),
            "cantidad": cant,
            "categoria": categoria_local.get().strip().lower(),
            "fecha": (fecha_norm or None),
        }

        # Persistir y refrescar UI
        guardar_movimientos(movimientos)

        aplicar_filtros()

        # Reseleccionar la fila editada (si sigue existiendo)
        iid = str(idx)
        if tv.exists(iid):
            tv.selection_set(iid)
            tv.focus(iid)
            tv.see(iid)  

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
def refrescar_lista(indices = None):
    #Decide qué mostrar
    idxs = range(len(movimientos)) if indices is None else indices

    #Limpiamos TreeView
    tv.delete(*tv.get_children())

    #Repintamos el TreeView según indices(idx)
    for i in idxs:
        mov = movimientos[i]
        fecha = mov.get("fecha") or "-"
        tipo = mov.get("tipo","")
        #Forzamos a float por si viene como string del JSON
        cantidad = f"{float(mov.get('cantidad',0)):.2f}"
        categoria = mov.get("categoria","")

        # Usamos iid = str(i) para que Editar/Eliminar siga funcionando con filtros
        tv.insert("","end",iid=str(i),values=(fecha,tipo,cantidad,categoria))
        
    
    #Actualizamos el resumen
    actualizar_resumen(indices)

    #Limpiar selección (para evitar botones activos tras refrescar)
    tv.selection_remove(*tv.selection())
    actualizar_estado_botones()


# Actualizar resumen de ingresos, gastos y balance
def actualizar_resumen(indices = None):
    #Decide qué mostrar
    idxs = range(len(movimientos)) if indices is None else indices

    tot_ing = 0.0
    tot_gas = 0.0
    
    for i in idxs:
        mov = movimientos[i]
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
    categoria = categoria_var.get().strip().lower()
    fecha = fecha_var.get().strip() or None # Si esta vacío, None

    #Validación básica de cantidad
    try:
        cantidad = float(cant_txt)
    except ValueError:
        messagebox.showerror("Cantidad inválida","La cantidad debe ser un número (usa punto para decimales).")
        return

    #Validación fecha
    fecha_norm = normalizar_fecha(fecha)
    if fecha and not fecha_norm:
        messagebox.showerror("Fecha inválida", "Usa formato dd/mm/yyyy o yyyy-mm-dd.")
        return

    movimiento = {
        "tipo": tipo,
        "cantidad": cantidad,
        "categoria": categoria,
        "fecha": fecha_norm
    }

    #Añadimos nuevo movimiento a la lista de movimientos
    movimientos.append(movimiento)

    #Guardamos lista de movimiento actualizada a nuestro JSON
    guardar_movimientos(movimientos)

    #Por ahora se imprime en consola
    print("Movimiento listo: ", movimiento)
    feedback_lbl.config(text="✅ Movimiento guardado.", fg="green")

    #Refrescamos lista de movimientos en la interfaz
    aplicar_filtros()

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

# Frame Filtros - Filtros para aplicar al listado de movimientos activo

#Etiquetas
tk.Label(frmFiltros, text="Categoría", bg="#f0f0f0").grid(row=0,column=0,sticky="w",padx=4,pady=4)
tk.Label(frmFiltros, text="Mes (YYYY-mm)", bg="#f0f0f0").grid(row=1,column=0,sticky="w",padx=4,pady=4)

#Entradas
filtro_categoria = tk.Entry(frmFiltros, textvariable=filtro_cat_var)
filtro_categoria.grid(row=0,column=1,sticky="ew", padx=4,pady=4)

filtro_mes = tk.Entry(frmFiltros, textvariable=filtro_mes_var)
filtro_mes.grid(row=1,column=1,sticky="ew",padx=4,pady=4)

#Botones
btn_aplicar_filtro = tk.Button(frmFiltros, text="Aplicar", command=aplicar_filtros)
btn_aplicar_filtro.grid(row=0,column=2,sticky="ew",padx=4,pady=(8,0))

btn_quitar_filtro = tk.Button(frmFiltros, text="Quitar", command=quitar_filtros)
btn_quitar_filtro.grid(row=0,column=3,sticky="ew",padx=4,pady=(8,0))


frmFiltros.grid_columnconfigure(1,weight=1)

# Frame Central - Listado de movimientos

#Treeview + scrollbar en frmCentral(Usamos grid dentro de este frame)
frmCentral.grid_rowconfigure(0,weight=1)
frmCentral.grid_columnconfigure(0,weight=1)


tv = ttk.Treeview(frmCentral,columns=("fecha","tipo","cantidad","categoria"), show="headings")

# Añadimos el vinculo de ejecución al seleccionar un valor del TreeView
tv.bind("<<TreeviewSelect>>", lambda e: actualizar_estado_botones())

#Atajo para exportar CSV
root.bind("<Control-e>", lambda e: exportar_csv())

#Añadimos atajos de teclado Eliminar movimiento - Spr/Backspace
tv.bind("<Delete>", on_key_delete)
tv.bind("<BackSpace>", on_key_delete)

#Si se hace clic en una zona sin fila, limpia la selección
tv.bind("<Button-1>", on_tree_click_vacio, add="+")

#Atajos en los Entry de filtros
filtro_categoria.bind("<Return>", lambda e: aplicar_filtros())
filtro_mes.bind("<Return>", lambda e: aplicar_filtros())
filtro_categoria.bind("<Escape>", lambda e: quitar_filtros())
filtro_mes.bind("<Escape>", lambda e: quitar_filtros())

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
btn_reset_sel = tk.Button(frmAcciones, text="Quitar selección", state=tk.DISABLED, command=quitar_seleccion)
btn_exportar = tk.Button(frmAcciones, text="Exportar CSV", command=exportar_csv)

btn_editar.pack(fill="x",pady=(0,6))
btn_eliminar.pack(fill="x",pady=(0,6))
btn_reset_sel.pack(fill="x", pady=(0,6))
btn_exportar.pack(fill="x")


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

# Al iniciar, aplicamos filtros (aunque estén vacios) para centralizar lógia
aplicar_filtros()
actualizar_estado_botones()

#UX: foco inicial
ent_cantidad.focus_set()

#Iniciamos el buble principal de la interfaz
root.mainloop()