FROM python:3.9-slim

# ==== Configuración de entorno ====
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
# Copiamos primero el requirements.txt para aprovechar la caché
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==== Copiamos el código ====
COPY app.py .
COPY start.sh .
RUN chmod +x /app/start.sh

# ==== Puerto expuesto ====
EXPOSE 5000

# ==== Comando por defecto ====
CMD ["/app/start.sh"]
