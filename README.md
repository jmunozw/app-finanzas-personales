# 💼 App de Finanzas Personales

Proyecto en evolución continua, diseñado para registrar, visualizar y gestionar ingresos y gastos.  
Construido desde cero como parte de mi portafolio técnico y mi proceso de reconversión profesional en desarrollo.

Cada versión representa una etapa de aprendizaje y mejora, aplicando nuevas herramientas, buenas prácticas y funcionalidades reales.

---

## 🚀 Objetivo del proyecto

Demostrar una evolución práctica como desarrollador autodidacta, con foco en:

- Modularidad
- Persistencia de datos
- Interfaces usables (consola / GUI)
- Escalabilidad y empaquetado
- Documentación profesional

---

## 🧩 Versiones del proyecto

| Versión | Descripción | Enlace |
|---------|-------------|--------|
| `v1-consola-json` | Versión inicial con interfaz por consola y persistencia en JSON | [Ver carpeta](./v1-consola-json) |
| `v2-gui-tkinter`  | Interfaz gráfica con `tkinter`, tabla de movimientos y resumen de ingresos/gastos | [Ver carpeta](./v2-gui-tkinter) |
| `v3-avanzada`     | CRUD completo en GUI: añadir, editar, eliminar, persistencia en JSON + filtros dinámicos | [Ver carpeta](./v3-avanzada) |

📑 Consulta el [CHANGELOG](./CHANGELOG.md) para ver la evolución detallada del proyecto.

---

## 📚 Tecnologías utilizadas

- Python 3
- JSON
- Tkinter
- (Próximamente: CSV, PyInstaller, etc.)

---

## 📂 Estructura del repositorio


```
app-finanzas-personales/
├── v1-consola-json/
│ ├── main.py
│ ├── modelos/
│ └── datos/
│
├── v2-gui-tkinter/
│ ├── app.py
│ ├── servicios/
│ └── datos/
│
├── v3-avanzada/
│ ├── app.py
│ ├── servicios/
│ ├── modelos/
│ └── datos/
│
├── .gitignore # exclusiones de cachés, entornos y archivos temporales
├── README.md ← este archivo
└── CHANGELOG.md ← historial de cambios
```
---

## 🛠 Buenas prácticas aplicadas

- Control de versiones con Git.
- Uso de un archivo `.gitignore` para excluir:
  - `__pycache__/`, `*.pyc` y otros binarios de Python.
  - Entornos virtuales (`venv/`, `.env/`).
  - Archivos temporales de sistema (`.DS_Store`, `Thumbs.db`).
- Documentación clara y organizada en cada versión.

---

## 💻 Sobre el autor

Este proyecto forma parte del portafolio de [@jmunozw](https://github.com/jmunozw).  
Desarrollado como parte de mi ruta hacia Dev profesional con ChatGPT como mentor técnico y la guía práctica de MoureDev.