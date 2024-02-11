#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "JARVIS v2.4";
const char* password = "strongsecurepassword";
const char* mqtt_server = "test.mosquitto.org";
const int LED_pin = 16;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Check if the received message contains the word "orange"
  if (strstr((char*)payload, "speechBegin") != NULL) {
    Serial.println("speechBegin");
    speechBegin();
    digitalWrite(LED_pin, HIGH);
  } else if (strstr((char*)payload, "speechEnd") != NULL){
    Serial.println("speechEnd");
    speechEnd();
    digitalWrite(LED_pin, LOW);
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("")) {
      Serial.println("connected");
      client.subscribe("robot_buddy/movement");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(LED_pin, OUTPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  reconnect();
  client.loop();
}

void speechBegin(){
  if (Serial.available() > 0){
    Serial.println("speechBegin");
    delay(100);
    digitalWrite(LED_pin, HIGH);
  }
  delay(100);
}

void speechEnd(){
  if (Serial.available() > 0){
    Serial.println("speechEnd");
    delay(100);
    digitalWrite(LED_pin, LOW);
  }
  delay(100);
}
