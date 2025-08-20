# 💰 App de Finanzas Personales – v2 (GUI con tkinter)

Versión con interfaz gráfica usando `tkinter`. Permite añadir ingresos/gastos, ver el listado con tabla y scrollbar, y muestra un resumen con totales y balance. La información se guarda en `JSON` para mantener la persistencia entre sesiones.

---

## ✨ Funcionalidades
- Formulario para **añadir movimientos** (tipo, cantidad, categoría, fecha opcional).
- **Tabla (Treeview)** con scroll para listar los movimientos.
- **Resumen** inferior con ingresos, gastos y balance.
- **Persistencia** en `datos/movimientos.json`.

---

## 🗂 Estructura

```
v2-gui-tkinter/
├── app.py
├── modelos/
│ └── movimiento.py
├── servicios/
│ └── persistencia.py
└── datos/
└── movimientos.json
```

---

## ▶️ Ejecución
```bash
python app.py
```
