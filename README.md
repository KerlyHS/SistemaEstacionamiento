# Sistema M2M Descentralizado para Estacionamiento Ecológico Inteligente

> Prototipo IoT para el monitoreo en tiempo real de plazas de estacionamiento mediante comunicación M2M utilizando ESP32, ESP-NOW, MQTT y Streamlit.

---

## Descripción

Este proyecto desarrolla un sistema de estacionamiento inteligente basado en una arquitectura **Machine-to-Machine (M2M)** descentralizada que permite detectar la ocupación de plazas de estacionamiento y visualizar su disponibilidad en tiempo real.

El sistema utiliza sensores ultrasónicos HC-SR04 conectados a microcontroladores ESP32 para detectar vehículos, comunicándose mediante **ESP-NOW** hacia un Gateway, el cual publica la información mediante **MQTT** y la expone mediante una API REST consumida por un dashboard desarrollado en Streamlit.

Su objetivo es reducir el tiempo de búsqueda de estacionamiento y contribuir a disminuir las emisiones de CO₂ producidas por la congestión vehicular.

---

# Vista del proyecto

## Prototipo físico

![Prototipo]([imagenes/prototipo.jpg](https://github.com/user-attachments/assets/3eaacb64-3755-42fc-a895-9f509374a94c))

## Dashboard

![Dashboard]([imagenes/dashboard.png](https://github.com/user-attachments/assets/63064e04-9eb0-4eac-a785-28b69f07dad9))

---

# Arquitectura del sistema

```
        ESP32 Nodo 1
      + HC-SR04 Sensor
             │
             │ ESP-NOW
             ▼

        ESP32 Gateway
             │
      API REST + MQTT
             │
             ▼
      Dashboard Streamlit
```

---

# Tecnologías utilizadas

- ESP32
- HC-SR04
- ESP-NOW
- MQTT
- Python
- Streamlit
- Arduino IDE
- REST API

---

# Estructura del proyecto

```
Proyecto/

├── gateway/
│   ├── gateway.ino
│
├── nodo_sensor/
│   ├── sensor.ino
│
├── dashboard/
│   ├── api.py
│   ├── main.py
│   ├── components/
│
├── imagenes/
│   ├── dashboard.png
│   ├── prototipo.jpg
│
└── README.md
```

---

# Funcionamiento

1. El sensor HC-SR04 detecta un vehículo.
2. El ESP32 determina si la plaza está libre u ocupada.
3. La información es enviada mediante ESP-NOW.
4. El Gateway recibe los datos.
5. El Gateway publica el estado mediante MQTT.
6. Streamlit consulta la API REST cada 2 segundos.
7. El usuario visualiza el estado de las plazas.

---

# 📊 Características

✔ Detección automática de ocupación

✔ Comunicación M2M

✔ Baja latencia mediante ESP-NOW

✔ Dashboard en tiempo real

✔ Arquitectura IoT

✔ Bajo consumo energético

---

# Resultados

- Detección correcta de las plazas.
- Actualización del dashboard cada 2 segundos.
- Comunicación estable mediante ESP-NOW.
- Publicación correcta mediante MQTT.

---

# Hardware utilizado

| Componente | Cantidad |
|------------|---------:|
| ESP32 | 3 |
| HC-SR04 | 2 |
| Protoboard | 2 |
| Cables Dupont | Varios |

---

# Software

- Arduino IDE
- Python 3.12
- Streamlit
- Requests
- Broker MQTT

---

# Instalación

## Clonar el repositorio

```bash
git clone https://github.com/usuario/repositorio.git
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
streamlit run main.py
```

---

# Autores

- Ariana Córdova
- Viviana Córdova
- Kerly Huachaca
- Jossibel Pérez
- Isauro Rivera

Universidad Nacional de Loja

Carrera de Computación

