# 💰 App de Finanzas Personales – v3 (Funcionalidades avanzadas)

Aplicación de escritorio en **Python + Tkinter** para gestionar ingresos, gastos y balance de manera sencilla.  
Amplía las versiones anteriores con una interfaz gráfica completa, edición y eliminación de movimientos y sistema de filtros.

---

## ✨ Funcionalidades actuales
- **Añadir movimientos** (tipo, cantidad, categoría y fecha opcional).
- **Editar movimientos** en un popup con los datos precargados.
- **Eliminar movimientos** con confirmación.
- **Filtros dinámicos**:
  - Por **categoría** (texto parcial o completo).
  - Por **mes** (`YYYY-mm`).
  - Botón de **Quitar filtros** para volver a la vista completa.
- **Tabla (Treeview)** con scroll para listar movimientos.
- **Resumen automático** con ingresos, gastos y balance, calculado sobre la vista actual (todos o filtrados).
- **Persistencia** en `datos/movimientos.json`.
- **Feedback en la interfaz** para confirmar acciones (guardado, edición, borrado, filtros aplicados).

---

## 🗂 Estructura

```
v3-avanzada/
├── app.py
├── modelos/
│ └── movimiento.py # igual que en v1/v2 (opcional)
├── servicios/
│ ├── persistencia.py # cargar y guardar en JSON
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
- **Exportación a CSV** de los movimientos visibles (todos o filtrados).
- **Resaltado visual** en la tabla para distinguir ingresos y gastos.
- Mejoras de UX en edición (validación en vivo, atajos de teclado).
- Explorar refactor hacia **MVC** (separar vista, lógica y modelo).

---

## 📚 Tecnologías utilizadas

- **Python 3**
- **Tkinter** (GUI)
- **JSON** (persistencia)

---

## 🧑‍💻 Autor

Este proyecto forma parte del portafolio de [@jmunozw](https://github.com/jmunozw).  
Desarrollado como parte de mi ruta hacia Dev profesional con ChatGPT como mentor técnico y la guía práctica de MoureDev.