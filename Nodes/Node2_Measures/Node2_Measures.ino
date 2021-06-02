#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>


#include <Adafruit_MLX90614.h>   //for better communication with MLX90614 Temperature sensor
#include <Wire.h>                //for I2C communication  

// access point network credentials
const char* ssid = "Benas";
const char* password = "benas666";

// IP address or domain name with URL path
const char* ServerNameUID = "http://192.168.43.134/IdPatient";    // client will connect to the server(ESP32)

unsigned long previousMillis = 0;
const long interval = 2000;        // Every 2 seconds we send a request to the server(ESP32)

String id_patient;

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
float temperatureData; 
String temp_state;

int ten1;
int ten2;
String tension;
String tension_state;

int white_led = 12;    //D6 with resistor 1Kohm
int red_led = 13;      //D7 with resistor 1Kohm

int buzzer = 15;     //D8

int button = 14;     //D5
int buttonstate;




void setup()
{
  Serial.begin(9600);
  pinMode (buzzer, OUTPUT);
  pinMode(red_led, OUTPUT);          // led is an outout
  pinMode(white_led, OUTPUT);
  pinMode(button, INPUT_PULLUP);     // button is an input
  buttonstate = HIGH;                // we initialize the state of the button as "released"
  
  //Connect to WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("The local IP address of ESP8266 (the client): ");
  Serial.println(WiFi.localIP());
  Serial.println();
  
  // Start mlx90614
  mlx.begin();
}



 
void loop() 
{
  unsigned long currentMillis = millis();
  
  if(currentMillis - previousMillis >= interval) 
    {
     // Check WiFi connection status
     if (WiFi.status() == WL_CONNECTED)
      {
       id_patient = httpGETRequest(ServerNameUID);
       //Serial.println("ID Patient: " + id_patient);
       //id_patient = "CC 1E 0C 30";  // Just to test when there is no rfid
        
       if (id_patient != "None" && id_patient != "--")
         Get_Temperature();

       else
        { buttonstate = digitalRead(button); 
          if(buttonstate == LOW)
             {Serial.println("Temperature measurement: access denied!");
              Serial.println("Please scan your card:");
              Serial.println();
              delay(500);}
        }
      
       // save the last HTTP GET Request
       previousMillis = currentMillis;
      }
    else 
      Serial.println("WiFi Disconnected");
    }
}



String httpGETRequest(const char* serverName)
{
  WiFiClient client;
  HTTPClient http;
    
  // IP address with path or Domain name with URL path 
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "--"; 
  
  if (httpResponseCode>0) {
    /*Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);*/
    payload = http.getString();
  }
  else {
    /*Serial.print("Error code: ");
    Serial.println(httpResponseCode);*/
  }
  // Free resources
  http.end();

  return payload;
}



void Get_Temperature()
{
  buttonstate = digitalRead(button); 
  if(buttonstate == HIGH) // test if the button has a high logic level: released
    {
        digitalWrite(red_led, LOW); 
        digitalWrite(white_led, LOW);
        digitalWrite(buzzer, LOW);
    }
  else   // test if the button has a logic level other than HIGH (therefore low: pressed)
    {  Serial.println("ID Patient: " + id_patient);
    
       temperatureData = mlx.readObjectTempC(); 

       ten1 = random(80,181);    // values between 80 and 180
       ten2 = random(40,111);    // values between 40 and 110
       tension = String(ten1) + "/" + String(ten2);


       if (temperatureData > 40 || temperatureData < 30)
         {Serial.println("Temperature: " + String(temperatureData) + " °C,  URGENT STATE!!!");
          temp_state = "URGENT!";}     
       else
         {Serial.println("Temperature: " + String(temperatureData) + " °C,  Normal state.");
          temp_state = "Normal";}


       if (ten1< 100 || ten2<60)
         {Serial.println("Tension    : " + tension + " mmHg,  LOW!!!");   // millimeter of mercury
          tension_state = "LOW!";}     
       else if (ten1> 139 || ten2>89)
         {Serial.println("Tension    : " + tension + " mmHg,  HYPERTENSION!!!");  
          tension_state = "HYPERTENSION!";} 
       else 
          {Serial.println("Tension    : " + tension + " mmHg,  Normal.");   
          tension_state = "Normal";}

       

       if (temp_state == "URGENT!")
         {
          digitalWrite(buzzer, HIGH);
          digitalWrite(red_led, HIGH);
          delay(300);
          digitalWrite(red_led, LOW);
          delay(300);
          digitalWrite(red_led, HIGH);
          delay(300);
          digitalWrite(red_led, LOW);
          delay(300);
          digitalWrite(red_led, HIGH);
          delay(300);
          digitalWrite(red_led, LOW);
          delay(300);
          digitalWrite(buzzer, LOW);
          delay(1000);}     
       else
         {
          digitalWrite(white_led, HIGH);
          delay(1000);
          digitalWrite(white_led, LOW);
          delay(1000);} 
             
      Sending_To_phpmyadmindatabase(); 
      Serial.println();
    }
}

 

void Sending_To_phpmyadmindatabase()     // CONNECTING WITH MYSQL
{
  HTTPClient http;    //Declaring object of class HTTPClient
  
  http.begin("http://192.168.43.217:8080/www/asma/S7/measures.php");           // when we use localhost instead, we are trying to connect esp itself
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");        // Specifying content-type header
  
  String PostData = "id_patient=" + id_patient + "&temperature=" + String(temperatureData) + "&temp_state=" + temp_state + "&tension=" + tension + "&tension_state=" + tension_state;
  int httpResponseCode = http.POST(PostData);         // PostData should be string
  
  Serial.print("  Insertion of temperature value to the DataBase: ");
  String response = http.getString();
  Serial.println(response);
  
    if (httpResponseCode != -1) {
      Serial.print("  HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("  Error code: ");
      Serial.println(httpResponseCode);
    }
    
    // Free resources
    http.end();
}

 
