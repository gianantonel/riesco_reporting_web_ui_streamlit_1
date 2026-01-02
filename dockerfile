# Usar una imagen base ligera de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto por defecto de Streamlit
EXPOSE 8501

# Comando para ejecutar la app
# Ajusta "app.py" al nombre de tu archivo principal
CMD ["streamlit", "run", "app_v1.py", "--server.port=8501", "--server.address=0.0.0.0"]