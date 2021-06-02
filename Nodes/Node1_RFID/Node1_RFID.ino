//CC 1E 0C 30: UID of blue tag
//D7 68 20 62: UID of white tag

#include "WiFi.h"
#include "WiFiClient.h"
#include "HTTPClient.h"
#include "ESPAsyncWebServer.h"

#include "mbedtls/aes.h"              // For encryption and decryption
#include "ArduinoJson.h"              // For Json objects

#include <SPI.h>
#include <MFRC522.h>


const char* ssid = "Benas";      // Access point network credentials
const char* password = "benas666";

int red_led = 5;                      // D5 with resistor 680ohm
int blue_led = 15;                    // D15 with resistor 680ohm

const int RST_PIN = 22;               // Reset pin
const int SDA_PIN = 21;               // Slave select pin

MFRC522 mfrc522(SDA_PIN, RST_PIN);    // Create MFRC522 instance
MFRC522::MIFARE_Key key;
MFRC522::StatusCode status;

char* key1 = "abcdefghijklmnop";      // key of encryption and decryption
unsigned char encrypted_data[64][16];
mbedtls_aes_context aes;              // Create aes instance

String id_patient = "None";
String UID;

unsigned long previousMillis = 0;
const long interval = 3000;           // Every 3 seconds we send a request to the server

AsyncWebServer server(80);            // Create AsyncWebServer object on port 80



/************************************************************************************************/
void setup(){
  Serial.begin(9600);                 // Serial port for debugging purposes
  
  pinMode(red_led, OUTPUT);        
  pinMode(blue_led, OUTPUT);
  
  SPI.begin();                        // Init SPI bus
  mfrc522.PCD_Init();                 // Init MFRC522
  
  connect_to_wifi();                  // Connect to WiFi network

  server.on("/IdPatient", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", id_patient.c_str()); });

  server.begin();                     // Start server
  
  Serial.println("Please scan your card:");
}



/************************************************************************************************/
void loop(){
  UID = "";

  // Prepare key of aes method - all keys(A & B) are set to FFFFFFFFFFFFh at chip delivery from the factory
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;
 
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
    {
     return;
    } 
    
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
    {
     return;
    }

  Serial.println(F("\n    **Card Detected**\n"));
    
  //Show UID on serial monitor
  Serial.print(" Patient ID tag:");
  for (byte i = 0; i < mfrc522.uid.size; i++) 
    {
       UID.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
       UID.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
  UID.toUpperCase();
  Serial.println(UID);

  // Access control
  Serial.print(" Controling access...");
  String name_patient = verify_id_patient();
  if (name_patient != "--" && name_patient != "Error!" && name_patient != " None")  
    {
      Serial.println(" Access Granted ");
      Serial.println(" Welcome" + name_patient + " ^_^");
      digitalWrite(blue_led, HIGH);   
      delay(1000);
      digitalWrite(blue_led, LOW); 
      id_patient = UID.substring(1);      // substring(1): it means from UID[1] to the end
      Writing_Personal_Data();
      Reading_Personal_Data();
    }
  else
    {
     Serial.println(" Access Denied! ");
     digitalWrite(red_led, HIGH);   
     delay(1000);
     digitalWrite(red_led, LOW);
     id_patient = "None";                 // Just to prepare another reading of id_patient
     delay(2000);                         // delay of 2s to avoid reading cards several times         
    }

   Sending_ID_Patient(UID.substring(1));
}



/************************************************************************************************/
void connect_to_wifi(){
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
  Serial.print("The local IP address of ESP32 (the server): ");
  Serial.println(WiFi.localIP());    // Clients must reach this address to obtain IdPatient: 192.168.43.134
  Serial.println();
}



/************************************************************************************************/
String verify_id_patient()     
{
  HTTPClient http;    //Declaring object of class HTTPClient
  
  http.begin("http://192.168.43.217:8080/www/asma/S7/access_control.php");    // when we use localhost instead, we are trying to connect esp itself
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");        // Specifying content-type header
  
  String PostData = "id_patient=" + UID.substring(1);
  int httpResponseCode = http.POST(PostData);                                 // PostData should be string

  String response = "--";
  
    if (httpResponseCode != -1) {
      Serial.print("  HTTP Response code: ");
      Serial.println(httpResponseCode);
      response = http.getString();
    }
    else {
      Serial.print("  Error code: ");
      Serial.println(httpResponseCode);
    }
    
    // Free resources
    http.end();

    return response;
}



/************************************************************************************************/
void Sending_ID_Patient(String uid){
    HTTPClient http;    //Declare object of class HTTPClient

    String postData = "UIDresult=" + uid;

    http.begin("http://192.168.43.217:8080/NodeMCU/getUID.php");  //Specify request destination
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header

    int httpCode = http.POST(postData);   //Send the request
    Serial.print("  Sending ID Patient: ");
    Serial.println(httpCode);   //Print HTTP return code

    http.end();  //Close connection
}



/************************************************************************************************/
void Writing_Personal_Data(){
  String input = httpGETRequest();                    // to get json object of data

  if(input != "--"){
          DynamicJsonDocument doc(1024);
          deserializeJson(doc, input);
          JsonObject obj = doc.as<JsonObject>();
          String id = obj["RFID"];
          if (id == id_patient){
            Serial.println("\nWriting personal data on a MIFARE PICC:");
            String firstname = obj["Firstname"];
            String lastname = obj["Lastname"];
            String cin = obj["Cin"];
            String state = obj["State"];
            String temperature = obj["Temperature"];
            String tension = obj["Tension"];

            String enc1 = encrypt(1, firstname);
            byte blockcontent1[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
            enc1.getBytes(blockcontent1, 16);
            write_block(1, blockcontent1);
            String enc2 = encrypt(2, lastname);
            byte blockcontent2[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
            enc2.getBytes(blockcontent2, 16);
            write_block(2, blockcontent2);
            String enc4 = encrypt(4, cin);
            byte blockcontent4[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
            enc4.getBytes(blockcontent4, 16);
            write_block(4, blockcontent4);
            String enc5 = encrypt(5, state);
            byte blockcontent5[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
            enc5.getBytes(blockcontent5, 16);
            write_block(5, blockcontent5);
            String enc6 = encrypt(6, temperature);
            byte blockcontent6[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
            enc6.getBytes(blockcontent6, 16);
            write_block(6, blockcontent6);
            String enc8 = encrypt(8, tension);
            byte blockcontent8[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
            enc8.getBytes(blockcontent8, 16);
            write_block(8, blockcontent8);
            
            Serial.println(F("\n    **End Writing**\n")); 
            }
          }
  
  // deleting hole data from the card
  /*byte blockcontent[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};//all zeros. This can be used to delete a block.
  for (byte block = 1; block <64 ; block++)
      writeBlock(block, blockcontent);*/
}



/************************************************************************************************/
String httpGETRequest()
{
  HTTPClient http;
    
  // IP address with path or Domain name with URL path 
  http.begin("http://192.168.43.217:8080/NodeMCU/insertData.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); //Specify content-type header

  // Send HTTP POST request
  int httpResponseCode = http.GET();
  String payload = "--"; 

  //Serial.print("  Getting json object of data: ");
  Serial.println(httpResponseCode);   //Print HTTP return code
  if (httpResponseCode != -1)
      payload = http.getString();
      //Serial.println(payload);

  // Free resources
  http.end();

  return payload;
}



/************************************************************************************************/
String encrypt(byte block, String msg){
  int len = msg.length() + 1; 
  char char_array[len];
  msg.toCharArray(char_array, len);
 
  mbedtls_aes_init( &aes );     // Initialize of aes object
  mbedtls_aes_setkey_enc( &aes, (const unsigned char*) key1, strlen(key1) * 8 );      // 8 bits
  mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_ENCRYPT, (const unsigned char*)char_array, encrypted_data[block]);
  mbedtls_aes_free( &aes );
  
  int result = int((const char *)encrypted_data[block]);
  return String(result);
  //return String((char*)encrypted_data[block]);
}



/************************************************************************************************/
int write_block(int blockNumber, byte arrayAddress[]) 
{
  //this makes sure that we only write into data blocks. Every 4th block is a trailer block for the access/security info.
  int largestModulo4Number = blockNumber/4*4;
  int trailerBlock = largestModulo4Number + 3;        //determine trailer block for the sector
  if (blockNumber > 2 && (blockNumber + 1)%4 == 0){
          /*Serial.print(blockNumber);
          Serial.println(" is a trailer block!!");*/
          return 2;       //block number is a trailer block (modulo 4); quit and send error code 2
  }
  
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
         /*Serial.print("PCD_Authenticate() failed: ");
         Serial.println(mfrc522.GetStatusCodeName(status));*/
         return 3;//return "3" as error message
  }
 
  status = mfrc522.MIFARE_Write(blockNumber, arrayAddress, 16);
  if (status != MFRC522::STATUS_OK) {
           /*Serial.print("Writing failed: ");
           Serial.println(mfrc522.GetStatusCodeName(status));*/
           return 4;//return "4" as error message
  }

  Serial.print(blockNumber);
  Serial.print(" is a data block, ");
  
  Serial.println(String((char*)arrayAddress) + " this data was written.");
  return 1;
}



/************************************************************************************************/
void Reading_Personal_Data(){
  Serial.println(F("Reading of personal data on a MIFARE PICC:"));        // shows in serial that it is ready to read
  
  for (byte block = 1; block <9 ; block++){
    String reading = read_block(block);
    if (reading != " is a trailer block" && reading != "")                // "" for error or empty block
        {//Serial.println(reading);                                       // showing data without decryption
        Serial.println(decrypt(block));}                                  // showing data with decryption
  }
  
  Serial.println(F("\n    **End Reading**\n")); 
}



/************************************************************************************************/
String decrypt(byte block){
  /*int len = msg.length() + 1; 
  char char_array[len];
  msg.toCharArray(char_array, len);*/

  unsigned char decrypted_data[16];
  
  mbedtls_aes_init( &aes );                  // Initialize of aes object
  mbedtls_aes_setkey_enc( &aes, (const unsigned char*) key1, strlen(key1) * 8 );  
  mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_DECRYPT, (unsigned char*)encrypted_data[block], decrypted_data);
  mbedtls_aes_free( &aes );
  
  return String((const char *)decrypted_data).substring(0,16);
}



/************************************************************************************************/
String read_block(byte block)
{
  //this makes sure that we only read from data blocks. Every 4th block is a trailer block for the access/security info.
  int largestModulo4Number = block/4*4;
  int trailerBlock = largestModulo4Number + 3;        //determine trailer block for the sector
  if (block > 2 && (block + 1)%4 == 0){
          //Serial.print(block);
          return " is a trailer block";         //block number is a trailer block (modulo 4) quit and send error code 2
  }
  
  byte buffer1[18];
  byte len = 18; 
 
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return "";
  }
 
  status = mfrc522.MIFARE_Read(block, buffer1, &len);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(status));
    return "";
  }

  Serial.print(block);
  Serial.print(" is a data block: ");
 
  String value = "";
  for (uint8_t i = 0; i < 16; i++)
  {
      value += (char)buffer1[i];
  }
  value.trim();
  if (value == "")
      Serial.println();
  return value;
}



/************************************************* END ******************************************/
