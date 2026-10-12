FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl iproute2 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalamos las dependencias necesarias incluyendo psutil para telemetría
RUN pip install --no-cache-dir flask requests gunicorn psutil

COPY entrypoint.py /app/entrypoint.py

EXPOSE 8080

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "entrypoint:app"]
