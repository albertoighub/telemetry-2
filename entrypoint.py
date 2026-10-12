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
    # Endpoints adicionales para consultar métricas en tiempo real vía HTTP
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
    # Hilo secundario para telemetría continua y supervisión de recursos
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            print(f"[BACKGROUND TELEMETRY] CPU: {cpu_usage}% | RAM Usada: {memory.percent}% ({round(memory.used / (1024 * 1024), 2)} MB)")
        except Exception as e:
            print(f"[BACKGROUND ERROR] No se pudieron obtener métricas: {e}")
        
        # Intervalo de 60 segundos entre cada reporte de telemetría interna
        time.sleep(60)

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    print("--- INICIANDO CONTENEDOR MULTIPODER CON TELEMETRÍA AVANZADA ---")
    
    # Lanzar el motor de telemetría de fondo en un hilo separado
    worker_thread = threading.Thread(target=background_worker, daemon=True)
    worker_thread.start()
    
    # Iniciar el servidor web principal en el hilo principal con Gunicorn/Flask
    run_web_server()
