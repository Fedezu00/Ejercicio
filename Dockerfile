FROM python:3.9-slim

WORKDIR /app

COPY app.py .
COPY requirements.txt .
COPY start.sh .

# Instalar Redis
RUN apt-get update && apt-get install -y redis-server \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
# Dar permisos de ejecución
RUN chmod +x start.sh



CMD ["bash", "start.sh"]

