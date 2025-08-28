from flask import Flask
import redis, time, os
from featureflags.client import CfClient
from featureflags.evaluations.auth_target import Target

app = Flask(__name__)

# Redis config
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# Harness FF config
HARNESS_FF_API_KEY = os.getenv("HARNESS_FF_API_KEY", "").strip()
FEATURE_FLAG_NAME = os.getenv("FEATURE_FLAG_NAME", "My_Test_Flag")
Apagar_todo = os.getenv("FEATURE_FLAG_NAME2", "Apagar_todo")


ff_client = None
if HARNESS_FF_API_KEY:
    try:
        ff_client = CfClient(HARNESS_FF_API_KEY)
        ff_client.wait_for_initialization()
        print("✅ Harness FF client inicializado")
    except Exception as e:
        print(f"⚠️ Error inicializando Harness FF: {e}")
else:
    print("⚠️ HARNESS_FF_API_KEY no provisto, flags deshabilitados")


def wait_for_redis():
    for i in range(30):
        print(f"🔍 Intentando conectar con Redis... intento {i+1}/30")
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
            r.ping()
            print("✅ Conexión con Redis exitosa")
            return r
        except redis.ConnectionError:
            print(f"⏳ Redis no disponible, reintentando en 1s...")
            time.sleep(1)
    raise Exception("❌ Redis no disponible después de 30 intentos")


@app.route('/')
def home():
    r = wait_for_redis()
    visitas = r.incr("visitas")


    bg, fg, msg = "#111827", "#c5227c", "🌙 Belgrano (flag ON)"
    
    treatment = False
    if ff_client:
        target = Target(identifier=str(visitas), name=f"user-{visitas}")
        treatment = ff_client.bool_variation(FEATURE_FLAG_NAME, target, False)

    if treatment:
        bg, fg, msg = "#111827", "#22c55e", "🌙 Nueva UI habilitada (flag ON)"
   

    treatment2 = False
    if ff_client:
        target = Target(identifier=str(visitas), name=f"user-{visitas}")
        treatment2 = ff_client.bool_variation(Apagar_todo, target, False)

    if treatment2:    #Si esta encendida muestra la pagina 
         return f"""
    <html>
      <body style="background:{bg};color:{fg};text-align:center;padding:50px;">
        <h1>📊 Contador de Visitas</h1>
        <p>Visitas: {visitas}</p>
        <p>{msg}</p>
        <a href="/reiniciar">Reiniciar</a> | <a href="/health">Health</a>
      </body>
    </html>
    """
    else:  #Muestra la pagina en blanco
        return f"""
        <html>
        </html>
        """




@app.route('/reiniciar')
def reiniciar():
    r = wait_for_redis()
    r.set("visitas", 0)
    return "✅ Contador reiniciado"


@app.route('/health')
def health():
    r = wait_for_redis()
    r.ping()
    return f"✅ Flask OK | Redis OK | HarnessFF {'OK' if ff_client else 'DISABLED'}"


if __name__ == "__main__":
    print("🚀 Iniciando Flask + Redis + Harness Feature Flags...")
    app.run(host="0.0.0.0", port=5000)
