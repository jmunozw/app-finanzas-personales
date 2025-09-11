# 💰 App de Finanzas Personales – v3 (Funcionalidades avanzadas)

Versión con interfaz gráfica en `tkinter`, que amplía las funcionalidades básicas de la v2.  
Ahora incluye edición y eliminación de movimientos desde la tabla, manteniendo la persistencia en `JSON`.

---

## ✨ Funcionalidades actuales
- **Añadir movimientos** (tipo, cantidad, categoría, fecha opcional).
- **Editar movimientos** en un popup con los datos precargados.
- **Eliminar movimientos** con confirmación.
- **Tabla (Treeview)** con scroll para listar movimientos.
- **Resumen automático** con ingresos, gastos y balance.
- **Persistencia** en `datos/movimientos.json`.
- **Feedback en la interfaz** para confirmar acciones.

---

## 🗂 Estructura

```
v3-avanzada/
├── app.py
├── modelos/
│ └── movimiento.py # igual que en v1/v2 (opcional)
├── servicios/
│ ├── persistencia.py # cargar y guardar en JSON
│ └── validacion.py # (opcional) helpers de validación de fecha
└── datos/
└── movimientos.json
```

---

## ▶️ Ejecución
```bash
python app.py
```

---

## 🔮 Próximos pasos (en desarrollo)
- **Filtros** por categoría y mes (YYYY-mm).
- **Exportación a CSV** de los movimientos visibles (todos o filtrados).
- Decisión: resumen calculado sobre **todos** los datos o sobre la **vista filtrada**

---

## 📚 Tecnologías utilizadas

- Python 3
- Tkinter (GUI)
- JSON (persistencia)

---

## 🧑‍💻 Autor

Este proyecto forma parte del portafolio de [@jmunozw](https://github.com/jmunozw).  
Desarrollado como parte de mi ruta hacia Dev profesional con ChatGPT como mentor técnico y la guía práctica de MoureDev.