#include <WiFi.h>
#include <esp_now.h>
#include <WebServer.h> 


const char* ssid = "Nombre de red";
const char* password = "Password";

WebServer server(80); 


typedef struct
{
  int id;
  bool ocupada;
} Mensaje;

Mensaje datos;

bool estado_plazas[10] = {false};


String construirJSON() {
  String json = "{\"plazas\": [";
  json += "{\"id\": 1, \"estado\": \"" + String(estado_plazas[1] ? "ocupada" : "libre") + "\"},";
  json += "{\"id\": 2, \"estado\": \"" + String(estado_plazas[2] ? "ocupada" : "libre") + "\"}";
  json += "]}";
  return json;
}


void OnDataRecv(const esp_now_recv_info *info,
                const uint8_t *incomingData,
                int len)
{

  Serial.println();
  Serial.println("==================================");
  Serial.println("PAQUETE RECIBIDO");
  Serial.println("==================================");

  Serial.print("MAC Nodo: ");

  for (int i = 0; i < 6; i++)
  {
    Serial.printf("%02X", info->src_addr[i]);

    if (i < 5)
      Serial.print(":");
  }

  Serial.println();

  Serial.print("Longitud: ");
  Serial.println(len);

  // Verificar tamaño
  if (len != sizeof(Mensaje))
  {
    Serial.println("ERROR: Tamaño incorrecto");
    return;
  }

  memcpy(&datos, incomingData, sizeof(datos));

  Serial.print("Nodo ID: ");
  Serial.println(datos.id);

  Serial.print("Estado: ");

  if (datos.ocupada)
    Serial.println("OCUPADA");
  else
    Serial.println("LIBRE");

  // Actualizar el estado en memoria para la API HTTP
  if (datos.id >= 1 && datos.id < 10) {
    estado_plazas[datos.id] = datos.ocupada;
  }

  Serial.println("==================================");
}

//==================================================
// Setup
//==================================================
void setup()
{

  Serial.begin(115200);

  delay(2000);

  Serial.println();
  Serial.println("==================================");
  Serial.println("INICIANDO GATEWAY");
  Serial.println("==================================");

  // Modo Estación y Conexión Wi-Fi
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);
  
  Serial.print("Conectando a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("MAC Gateway: ");
  Serial.println(WiFi.macAddress());

  // Inicializar ESP-NOW
  esp_err_t resultado = esp_now_init();

  if (resultado != ESP_OK)
  {
    Serial.print("Error ESP-NOW: ");
    Serial.println(resultado);
    return;
  }

  Serial.println("ESP-NOW Inicializado");

  // Registrar callback
  esp_now_register_recv_cb(OnDataRecv);

  // <-- [HTTP] Configuración del servidor Web -->
  server.on("/api/estacionamiento", HTTP_GET, []() {
    server.send(200, "application/json", construirJSON());
  });
  server.begin();

  // IMPRESIÓN ÚNICA AL INICIAR
  Serial.println();
  Serial.println("----------------------------------");
  Serial.print("Servidor HTTP activo en: http://");
  Serial.print(WiFi.localIP());
  Serial.println("/api/estacionamiento");
  Serial.println("----------------------------------");

  Serial.println("Esperando paquetes...");
  Serial.println();
}

//==================================================
// Loop
//==================================================
void loop()
{
  server.handleClient(); // <-- [HTTP] Atiende silenciosamente las peticiones
}