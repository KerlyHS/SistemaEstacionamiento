import requests

# URL de la API HTTP en la ESP32 Gateway
URL_API = "http://10.25.100.222/api/estacionamiento"

def obtener_estado_estacionamiento(timeout=3):
    """
    Obtiene los datos de las plazas desde la ESP32 Gateway.
    Devuelve: (conectado: bool, plazas: list)
    """
    try:
        respuesta = requests.get(URL_API, timeout=timeout)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            return True, datos.get("plazas", [])
        return False, []
    except Exception:
        return False, []