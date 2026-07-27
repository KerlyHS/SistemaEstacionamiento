#include <WiFi.h>
#include <esp_now.h>
#include <WebServer.h>
#include <PubSubClient.h>

//==================================================
// Credenciales WiFi y Broker Mosquitto (Windows)
//==================================================
const char* ssid          = "RED-INTERNET";
const char* password      = "CONTRASENIA";
const char* mqtt_server   = "192.168.1.5"; // IP de la PC donde corre Mosquitto / Streamlit
const int   mqtt_port     = 1883;

//==================================================
// Objetos y Variables Globales
//==================================================
WiFiClient espClient;
PubSubClient mqttClient(espClient);
WebServer server(80);

// Estructura recibida desde los nodos sensores vía ESP-NOW
typedef struct
{
    int id;
    bool ocupada;
} Mensaje;

Mensaje datos;

// Estado local para SOLO 2 PLAZAS (Índices 1 y 2)
bool estado_plazas[3] = {false, false, false};
volatile bool nuevo_dato_pendiente = false; // Flag para sincronización entre núcleos

//==================================================
// Construcción del JSON ajustado a 2 Plazas
//==================================================
String construirJSON()
{
    int ocupadas = 0;
    if (estado_plazas[1]) ocupadas++;
    if (estado_plazas[2]) ocupadas++;

    String json = "{";
    json += "\"resumen\":{";
    json += "\"total\":2,";
    json += "\"ocupadas\":" + String(ocupadas) + ",";
    json += "\"libres\":" + String(2 - ocupadas);
    json += "},";
    json += "\"plazas\":[";

    // Plaza 1
    json += "{\"id\":1,\"estado\":\"" + String(estado_plazas[1] ? "ocupada" : "libre") + "\"},";
    // Plaza 2
    json += "{\"id\":2,\"estado\":\"" + String(estado_plazas[2] ? "ocupada" : "libre") + "\"}";

    json += "]}";
    return json;
}

//==================================================
// Callback recepción ESP-NOW (Ultrarrápido)
//==================================================
void OnDataRecv(const esp_now_recv_info *info, const uint8_t *incomingData, int len)
{
    if (len != sizeof(Mensaje)) return;

    memcpy(&datos, incomingData, sizeof(datos));

    // Solo aceptamos nodos con ID 1 o ID 2
    if (datos.id == 1 || datos.id == 2)
    {
        estado_plazas[datos.id] = datos.ocupada;
        nuevo_dato_pendiente = true; // Notificamos a la tarea MQTT
    }
}

//==================================================
// Conexión a Mosquitto
//==================================================
void conectarMQTT()
{
    if (mqttClient.connected()) return;

    Serial.print("[MQTT] Conectando a Mosquitto en ");
    Serial.print(mqtt_server);
    Serial.print("... ");

    String clientID = "ESP32_Gateway_" + String(random(0xffff), HEX);

    if (mqttClient.connect(clientID.c_str()))
    {
        Serial.println("¡CONECTADO!");
        // Enviar estado inicial retenido
        mqttClient.publish("estacionamiento/plazas", construirJSON().c_str(), true);
    }
    else
    {
        Serial.print("Falló, rc=");
        Serial.println(mqttClient.state());
    }
}

//==================================================
// Tarea FreeRTOS para MQTT (Core 1)
//==================================================
void tareaMQTT(void *pvParameters)
{
    for (;;)
    {
        if (WiFi.status() == WL_CONNECTED)
        {
            if (!mqttClient.connected())
            {
                conectarMQTT();
                vTaskDelay(pdMS_TO_TICKS(3000)); // Espera 3s si falla
            }
            else
            {
                mqttClient.loop();

                // Publicar al recibir un cambio desde un nodo ESP-NOW
                if (nuevo_dato_pendiente)
                {
                    nuevo_dato_pendiente = false;
                    String payload = construirJSON();

                    // 1. Resumen global (para Streamlit)
                    mqttClient.publish("estacionamiento/plazas", payload.c_str(), true);

                    // 2. Tópico individual por plaza (estacionamiento/plaza/1 o 2)
                    String topicoPlaza = "estacionamiento/plaza/" + String(datos.id);
                    String jsonSingle = "{\"id\":" + String(datos.id) + ",\"estado\":\"" + (datos.ocupada ? "ocupada" : "libre") + "\"}";
                    mqttClient.publish(topicoPlaza.c_str(), jsonSingle.c_str(), true);

                    Serial.println("[MQTT] Publicación exitosa:");
                    Serial.println(payload);
                }
            }
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

//==================================================
// SETUP
//==================================================
void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n==================================");
    Serial.println("  INICIANDO GATEWAY (2 PLAZAS)    ");
    Serial.println("==================================");

    // 1. Conexión WiFi
    WiFi.mode(WIFI_AP_STA);
    WiFi.begin(ssid, password);

    Serial.print("Conectando a red WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi Conectado!");
    Serial.print("IP Gateway: ");  Serial.println(WiFi.localIP());
    Serial.print("MAC Gateway: "); Serial.println(WiFi.macAddress());

    // 2. Configuración MQTT
    mqttClient.setServer(mqtt_server, mqtt_port);

    // 3. Crear tarea FreeRTOS para MQTT
    xTaskCreatePinnedToCore(
        tareaMQTT,
        "Tarea_MQTT",
        8192,
        NULL,
        1,
        NULL,
        1
    );

    // 4. Inicializar ESP-NOW
    if (esp_now_init() != ESP_OK)
    {
        Serial.println("ERROR: No se pudo iniciar ESP-NOW");
        return;
    }
    esp_now_register_recv_cb(OnDataRecv);
    Serial.println("ESP-NOW Inicializado exitosamente.");

    // 5. Configurar API HTTP de respaldo
    server.on("/api/estacionamiento", HTTP_GET, []() {
        server.send(200, "application/json", construirJSON());
    });
    server.begin();

    Serial.println("----------------------------------");
    Serial.print("API REST Lista en: http://");
    Serial.print(WiFi.localIP());
    Serial.println("/api/estacionamiento");
    Serial.println("----------------------------------\n");
}

//==================================================
// LOOP PRINCIPAL
//==================================================
void loop()
{
    server.handleClient();
}