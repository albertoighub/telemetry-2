import os
import threading
import time
import psutil
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Sistema Multipoder V2.0 - Nodo Operativo", 200

@app.route("/telemetry", methods=["GET"])
def get_telemetry():
    # Endpoint HTTP para consultar el estado del nodo en tiempo real
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    data = {
        "status": "online",
        "cpu_percent": cpu_usage,
        "memory_total_mb": round(memory.total / (1024 * 1024), 2),
        "memory_used_mb": round(memory.used / (1024 * 1024), 2),
        "memory_percent": memory.percent,
        "disk_percent": disk.percent
    }
    return jsonify(data), 200

def background_worker():
    # Hilo secundario para telemetría de rendimiento y red en segundo plano
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            print(f"[BACKGROUND TELEMETRY] CPU: {cpu_usage}% | RAM Usada: {memory.percent}% ({round(memory.used / (1024 * 1024), 2)} MB)")
        except Exception as e:
            print(f"[BACKGROUND ERROR] No se pudieron obtener métricas: {e}")
        
        # Intervalo de 60 segundos entre cada reporte
        time.sleep(60)

if __name__ == "__main__":
    print("--- INICIANDO CONTENEDOR MULTIPODER CON TELEMETRÍA AVANZADA ---")
    
    # Lanzar el motor de telemetría de fondo en un hilo separado
    worker_thread = threading.Thread(target=background_worker, daemon=True)
    worker_thread.start()
