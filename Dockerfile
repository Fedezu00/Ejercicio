#La imagen base utilizada
FROM python:3.9-slim 

# ==== Evita que se creen archivos .pyc, hace que pip no cachee paquetes localmente, hace que la salida stdout no este en buffer ====
ENV PYTHONDONTWRITEBYTECODE=1 \   
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ==== Directorio de trabajo ====
WORKDIR /app

# ==== Dependencias de sistema mínimas ====
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
 && rm -rf /var/lib/apt/lists/*

# ==== Instalación de dependencias de Python ====
# Copiamos primero el requirements.txt para aprovechar el cache y upgradeamos pip y luego instala los requierments
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==== Copiamos el código ====
COPY app.py .
COPY start.sh .
#Permisoo de ejecucion al archivo
RUN chmod +x /app/start.sh

# ==== Puerto expuesto ====
EXPOSE 5000

# ==== Comando por defecto ====
CMD ["/app/start.sh"]
