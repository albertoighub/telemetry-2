import os
import threading
import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def health_check():
    # Respuesta estándar para que los balanceadores de carga de Render/Koyeb vean el servicio activo
    return "System Operational - Multipower Node V2.0", 200

def run_web_server():
    # Koyeb y Render inyectan la variable de entorno PORT; por defecto usamos el puerto 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def background_worker():
    # Hilo secundario para ejecutar tareas en segundo plano (telemetría, micro-proxy, etc.)
    while True:
        print("[BACKGROUND] Nodo multipoder activo y sincronizando...")
        # Aquí puedes integrar llamadas de control o scripts de red personalizados
        time.sleep(300)

if __name__ == "__main__":
    print("--- INICIANDO CONTENEDOR MULTIPODER (FRENTE 1) ---")
    
    # Lanzar el motor de fondo en un hilo separado
    worker_thread = threading.Thread(target=background_worker, daemon=True)
    worker_thread.start()
    
    # Iniciar el servidor web principal en el hilo principal
    run_web_server()