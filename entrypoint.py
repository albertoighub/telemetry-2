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
    # CPU y Memoria
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    # Almacenamiento (Disco raíz)
    disk = psutil.disk_usage('/')
    
    # Tráfico de Red global
    net = psutil.net_io_counters()
    
    data = {
        "status": "online",
        "cpu_percent": cpu_usage,
        "memory_total_mb": round(memory.total / (1024 * 1024), 2),
        "memory_used_mb": round(memory.used / (1024 * 1024), 2),
        "memory_percent": memory.percent,
        "disk_total_gb": round(disk.total / (1024 * 1024 * 1024), 2),
        "disk_used_gb": round(disk.used / (1024 * 1024 * 1024), 2),
        "disk_free_gb": round(disk.free / (1024 * 1024 * 1024), 2),
        "disk_percent": disk.percent,
        "network_bytes_sent": net.bytes_sent,
        "network_bytes_recv": net.bytes_recv
    }
    return jsonify(data), 200

def background_worker():
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            net = psutil.net_io_counters()
            
            print(f"[TELEMETRY] CPU: {cpu_usage}% | RAM: {memory.percent}% | Disco: {disk.percent}% | Red (Enviados/Recibidos): {net.bytes_sent}/{net.bytes_recv} bytes")
        except Exception as e:
            print(f"[BACKGROUND ERROR] No se pudieron obtener métricas: {e}")
        time.sleep(60)

if __name__ == "__main__":
    print("--- INICIANDO CONTENEDOR CON TELEMETRÍA DE RED Y ALMACENAMIENTO ---")
    worker_thread = threading.Thread(target=background_worker, daemon=True)
    worker_thread.start()
