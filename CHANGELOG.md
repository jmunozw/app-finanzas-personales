# 📑 Changelog

## [v3.2.0] - 2025-09-23
### ✨ Añadido
- **Exportación a CSV**: los movimientos visibles (todos o filtrados) pueden guardarse en un archivo de texto (`.csv`).
- Diálogo de "Guardar como..." integrado en la interfaz con soporte de codificación UTF-8.

### 🛠 Cambiado
- La opción de refresco de lista tras añadir/editar/eliminar ahora reaplica filtros para mantener coherencia.
- `README.md` principal y de `v3-avanzada` actualizados con la nueva funcionalidad.

---

## [v3.1.0] - 2025-09-19
### ✨ Añadido
- **Filtros dinámicos** por categoría y mes (`YYYY-mm`).
- Botones de **Aplicar filtro** y **Quitar filtros** en la interfaz.
- Feedback visual mostrando el número de resultados filtrados.
- Validación ligera del formato de mes al aplicar filtros.

### 🛠 Cambiado
- Los resúmenes de ingresos, gastos y balance ahora se recalculan según la vista actual (todos los datos o filtrados).
- El refresco de la tabla (`Treeview`) se centraliza en `aplicar_filtros()` para mantener siempre la coherencia de la vista.
- Los botones de acción (Editar, Eliminar, Quitar selección) se actualizan tras aplicar filtros o limpiar selección.

### 🐞 Corregido
- Eliminación de movimientos desde una vista filtrada: ahora los filtros se reaplican automáticamente tras eliminar.
- Manejo de casos con fechas inválidas o ausentes al aplicar filtros.

---

## [v3.0.0] - 2025-09-11
### ✨ Añadido
- Botones de acción en la interfaz: **Editar**, **Eliminar** y **Quitar selección**.
- Función **Eliminar** con confirmación y actualización automática del resumen.
- Función **Editar** con popup modal, campos precargados y validación de datos.
- Reselección automática de la fila editada tras guardar.
- Mensajes de feedback en la interfaz para todas las acciones.
- Persistencia en JSON mantenida tras editar y eliminar.

### 🛠 Cambiado
- La lógica de selección en la tabla ahora controla el estado de los botones según haya fila seleccionada o no.

### 🐞 Corregido
- Manejo de intentos de editar/eliminar sin fila seleccionada.
- Errores de cierre del popup (la “X” ahora dispara el mismo flujo que Cancelar).

---

## [v2.0.0] - 2025-08-20
### ✨ Añadido
- Interfaz gráfica con `tkinter`.
- Formulario para añadir ingresos y gastos.
- Tabla (`Treeview`) con scroll para listar movimientos.
- Resumen inferior con ingresos, gastos y balance.
- Persistencia en JSON dentro de la carpeta `datos/`.

---

## [v1.0.0] - 2025-08-15
### ✨ Añadido
- Versión inicial con interfaz de consola.
- Registro de movimientos (tipo, cantidad, categoría y fecha).
- Guardado en JSON con persistencia básica.