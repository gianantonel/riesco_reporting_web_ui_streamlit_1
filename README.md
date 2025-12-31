# Optimizar-IA — UI de Generación Automática de Reportes (Streamlit)

Esta aplicación es una interfaz web simple hecha con **Python + Streamlit** para disparar procesos de generación automática de reportes en **n8n** mediante un **Webhook**.

La UI muestra un logo, un título y 4 botones. Al presionar un botón:
1. La app envía un **HTTP POST** al webhook de n8n correspondiente.
2. Se muestra un **spinner** con el texto “Ejecutando proceso”.
3. La app espera la respuesta del workflow de n8n (**modo sync**) y finalmente muestra si el proceso fue **exitoso** o **falló**.

---

## ¿Por qué el archivo se llama `app_v1.py`?

El archivo principal se llama `app_v1.py` para identificar esta versión como la primera versión estable (v1) de la UI.
Esto permite mantener versiones futuras en paralelo (por ejemplo `app_v2.py`, `app_v3.py`) sin pisar la anterior, y facilita volver atrás si se realizan cambios grandes.

---

## Requisitos

- Python 3.10+ (recomendado)
- Acceso a internet para conectarse al webhook de n8n

---

## Estructura del proyecto

```text
.
├─ app_v1.py
├─ requirements.txt
└─ logo/
   └─ optimizar-ia.png   (o .jpg / .jpeg)
