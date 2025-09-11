# 📑 Changelog

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

## [v2.0.0] - 2025-08-20
### ✨ Añadido
- Interfaz gráfica con `tkinter`.
- Formulario para añadir ingresos y gastos.
- Tabla (`Treeview`) con scroll para listar movimientos.
- Resumen inferior con ingresos, gastos y balance.
- Persistencia en JSON dentro de la carpeta `datos/`.

## [v1.0.0] - 2025-08-15
### ✨ Añadido
- Versión inicial con interfaz de consola.
- Registro de movimientos (tipo, cantidad, categoría y fecha).
- Guardado en JSON con persistencia básica.