import json
import logging
import threading
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "estacionamiento/plazas"

logger = logging.getLogger("api_estacionamiento")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

_latest_plazas = []
_latest_conectado = False
_lock = threading.Lock()

def _get_latest():
    with _lock:
        return _latest_conectado, list(_latest_plazas)

def _set_latest(conectado, plazas):
    global _latest_plazas, _latest_conectado
    with _lock:
        _latest_conectado = conectado
        _latest_plazas = list(plazas)

def on_message(client, userdata, msg):
    try:
        datos = json.loads(msg.payload)
        plazas = datos.get("plazas", [])
        logger.info(f"Datos recibidos por MQTT: {plazas}")
        _set_latest(True, plazas)
    except Exception as e:
        logger.error(f"Error procesando MQTT: {e}")

def mqtt_loop():
    client = mqtt.Client()
    client.on_message = on_message
    try:
        client.connect(BROKER, 1883, 60)
        client.subscribe(TOPIC)
        logger.info(f"Conectado al broker MQTT {BROKER}, topic {TOPIC}")
        client.loop_forever()
    except Exception as e:
        logger.error(f"Error conectando al broker MQTT: {e}")
        _set_latest(False, [])

_iniciado = False

def iniciar_mqtt():
    global _iniciado
    if not _iniciado:
        _iniciado = True
        hilo = threading.Thread(target=mqtt_loop, daemon=True)
        hilo.start()

def obtener_estado_estacionamiento():
    return _get_latest()
