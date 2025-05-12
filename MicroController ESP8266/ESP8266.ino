// my_esp8266_code.cpp

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Definición de las credenciales de la red WiFi
const char* ssid = "ACC";
const char* password = "1234567890.";

// Instanciación de un web server que escucha el puerto 80
ESP8266WebServer server(80);

// Pines para el LED de éxito y fallo
// const int ledSuccess = D2;  // Pin D2
// const int ledFail = D3;     // Pin D3

// Pin que será controlado cuando se reciba la solicitud
const int gpioPin = D1;     // Pin D1

// Configuración de la IP estática
IPAddress local_IP(192, 168, 1, 183);  // Define la IP que quieres asignar
IPAddress gateway(192, 168, 1, 1);     // Puerta de enlace (usualmente la IP del router)
IPAddress subnet(255, 255, 255, 0);    // Máscara de subred
IPAddress primaryDNS(8, 8, 8, 8);      // DNS primario (puedes usar el de Google)
IPAddress secondaryDNS(8, 8, 4, 4);    // DNS secundario (opcional)

// Función por ejecutar cuando recibe /pulse
void handleGpioPulse() {
    digitalWrite(gpioPin, HIGH);
    delay(500);
    digitalWrite(gpioPin, LOW);
    server.send(200, "text/plain", "GPIO Pin Activated");
}

void setup() {
    // Inicializa la comunicación serie a 115200 baudios
    Serial.begin(115200);

    // Configura los pines
    pinMode(gpioPin, OUTPUT);
    // pinMode(ledSuccess, OUTPUT);
    // pinMode(ledFail, OUTPUT);

    // Apaga los LEDs al inicio
    // digitalWrite(ledSuccess, LOW);
    // digitalWrite(ledFail, LOW);

    // Configura la IP estática antes de conectar al WiFi
    if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
        Serial.println("Error al configurar la IP estática");
    }

    // Conecta el ESP8266 a la red WiFi
    WiFi.begin(ssid, password);
    
    // Espera hasta que el WiFi esté conectado o se agote el tiempo
    int maxRetries = 10; // Tiempo límite (10 segundos)
    int retryCount = 0;

    while (WiFi.status() != WL_CONNECTED && retryCount < maxRetries) {
        delay(1000);
        Serial.println("Conectando a WiFi...");
        retryCount++;
    }

    // Verifica si la conexión fue exitosa o fallida
    if (WiFi.status() == WL_CONNECTED) {
        // Éxito: enciende el LED de éxito y muestra la IP
        Serial.println("Conexión WiFi exitosa");
        Serial.println(WiFi.localIP());
        // digitalWrite(ledSuccess, HIGH);  // LED de éxito encendido
        // digitalWrite(ledFail, LOW);      // Asegura que el LED de fallo esté apagado
    } else {
        // Fallo: enciende el LED de fallo
        Serial.println("Fallo en la conexión WiFi");
        // digitalWrite(ledSuccess, LOW);   // Asegura que el LED de éxito esté apagado
        // digitalWrite(ledFail, HIGH);     // LED de fallo encendido
    }

    // Configuración del servidor web
    server.on("/pulse", handleGpioPulse);
    server.begin();
    Serial.println("Servidor web iniciado");
}

void loop() {
    // Procesa las solicitudes HTTP entrantes
    server.handleClient();
}
