/*
=========================================================
 NODO SENSOR - ESTACIONAMIENTO ECOLÓGICO
 HC-SR04 + FreeRTOS + ESP-NOW
=========================================================
*/

#include <WiFi.h>
#include <esp_now.h>

//==================================================
// Pines HC-SR04
//==================================================
#define TRIG 26
#define ECHO 27

//==================================================
// Parámetros
//==================================================
const float DISTANCIA_OCUPADA = 7.0;
const unsigned long TIEMPO_CONFIRMACION = 5000;

//==================================================
// Dirección MAC del Gateway
//==================================================
uint8_t gatewayMAC[] =
{
  0xE0, 0x8C, 0xFE, 0x5D, 0xCD, 0xB4
};
//==================================================
// Estructura del mensaje
//==================================================
typedef struct
{
  int id;
  bool ocupada;
} Mensaje;

Mensaje datos;

esp_now_peer_info_t peerInfo;

//==================================================
// Variable compartida
//==================================================
volatile float distanciaActual = -1;

// Estado actual de la plaza
bool estadoActual = false;

//==================================================
// Callback de envío
//==================================================
void OnDataSent(const wifi_tx_info_t *info,
                esp_now_send_status_t status)
{

  Serial.print("ESP-NOW: ");

  if (status == ESP_NOW_SEND_SUCCESS)
    Serial.println("OK");
  else
    Serial.println("ERROR");

}

//==================================================
// Medición HC-SR04
//==================================================
float medirDistancia()
{

  digitalWrite(TRIG, LOW);
  delayMicroseconds(3);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);

  long tiempo = pulseIn(ECHO, HIGH, 30000);

  if (tiempo == 0)
    return -1;

  return tiempo * 0.0343 / 2.0;

}

//==================================================
// TAREA SENSOR
//==================================================
void tareaSensor(void *pvParameters)
{

  while (true)
  {

    distanciaActual = medirDistancia();

    vTaskDelay(pdMS_TO_TICKS(100));

  }

}

//==================================================
// TAREA ESTADO
//==================================================
void tareaEstado(void *pvParameters)
{

  bool condicionAnterior = false;

  unsigned long inicioCambio = millis();

  while (true)
  {

    float distancia = distanciaActual;

    if (distancia < 0)
    {
      vTaskDelay(pdMS_TO_TICKS(100));
      continue;
    }

    Serial.print("Distancia: ");
    Serial.print(distancia);
    Serial.println(" cm");

    bool condicionActual = (distancia <= DISTANCIA_OCUPADA);

    // Si cambió la condición reiniciamos contador
    if (condicionActual != condicionAnterior)
    {

      condicionAnterior = condicionActual;
      inicioCambio = millis();

    }

    // Si permaneció estable 5 segundos
    if (millis() - inicioCambio >= TIEMPO_CONFIRMACION)
    {

      if (condicionActual != estadoActual)
      {

        estadoActual = condicionActual;

        datos.id = 2;
        datos.ocupada = estadoActual;

        esp_err_t resultado =
          esp_now_send(gatewayMAC,
                       (uint8_t *)&datos,
                       sizeof(datos));

        if (resultado == ESP_OK)
          Serial.println("Mensaje enviado");
        else
          Serial.println("Error enviando");

        Serial.print("Nuevo Estado -> ");

        if (estadoActual)
          Serial.println("OCUPADA");
        else
          Serial.println("LIBRE");

      }

    }

    vTaskDelay(pdMS_TO_TICKS(100));

  }

}

//==================================================
// SETUP
//==================================================
void setup()
{

  Serial.begin(115200);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  digitalWrite(TRIG, LOW);

  WiFi.mode(WIFI_STA);

  Serial.print("MAC Nodo: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK)
  {

    Serial.println("Error inicializando ESP-NOW");

    while (true);

  }

  esp_now_register_send_cb(OnDataSent);

  memcpy(peerInfo.peer_addr,
         gatewayMAC,
         6);

  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK)
  {

    Serial.println("No se pudo registrar el Gateway");

    while (true);

  }

  xTaskCreatePinnedToCore(
      tareaSensor,
      "Sensor",
      4096,
      NULL,
      2,
      NULL,
      1);

  xTaskCreatePinnedToCore(
      tareaEstado,
      "Estado",
      4096,
      NULL,
      1,
      NULL,
      1);

  Serial.println();
  Serial.println("==============================");
  Serial.println("Nodo listo 2");
  Serial.println("==============================");

}

//==================================================
// LOOP
//==================================================
void loop()
{

}