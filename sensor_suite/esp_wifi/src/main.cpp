#include <Arduino.h>
#include <BMI160Gen.h>
#include <sstream>
#include <iostream>
#include <string>
#include <EEPROM.h>
#include "WiFi.h"
#include <PubSubClient.h>
#define MSG_BUFFER_SIZE 128
char msg[MSG_BUFFER_SIZE];

//----------------------------------------------------- Wifi & I2C ------------------------------------------------------------------------//
const char* ssid = "DFKI-LAB";//"sadda_wifi";//"TP-Link_EE56"; //
const char* password = "EN17831997SAF";//"56DuX#zpaQVK936c";//"87569216";//wifi password<redacted>
const int i2c_addr = 0x69;
const int interrupt_pin = 16; //16 für INT1, 17 for INT2
const int slave_select_pin = 27;//15; 

//----------------------------------------------------- MQTT Broker------------------------------------------------------------------------//
const char *mqtt_broker = "broker.emqx.io";
const char *topic = "esp32/ta_sensor1";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

//----------------------------------------------------Create instances--------------------------------------------------------------------//

WiFiClient espClient;
PubSubClient client(espClient);

//----------------------------------------------IMU and Measurement definitions-----------------------------------------------------------//
#define MEASUREMENT_FREQUENCY 25 //in Hz
#define DEVICE_NAME "IMU Huefte"
#define NO_CALIBRATION  "0"
#define DO_CALIBRATION "1"


//define EEPROM sizes and adresses for storing offset values
#define EEPROM_SIZE 12
#define X_GYRO_ADD 0
#define Y_GYRO_ADD 2
#define Z_GYRO_ADD 4

#define X_ACC_ADD 6
#define Y_ACC_ADD 8
#define Z_ACC_ADD 10

hw_timer_t * timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;


bool deviceConnected = false;
bool oldDeviceConnected = false;
bool calibrationInProgress = false;
bool published = false;



/**
 *  Store calibration values in flash memory
 */ 

void storeCalibrationOffsets() {
  EEPROM.writeShort(X_GYRO_ADD, BMI160.getGyroOffset(X_AXIS));
  delay(100);
  EEPROM.writeShort(Y_GYRO_ADD, BMI160.getGyroOffset(Y_AXIS));
  delay(100);
  EEPROM.writeShort(Z_GYRO_ADD, BMI160.getGyroOffset(Z_AXIS));
  delay(100);
  
  EEPROM.writeShort(X_ACC_ADD, BMI160.getAccelerometerOffset(X_AXIS));
  delay(100);
  EEPROM.writeShort(Y_ACC_ADD, BMI160.getAccelerometerOffset(Y_AXIS));
  delay(100);
  EEPROM.writeShort(Z_ACC_ADD, BMI160.getAccelerometerOffset(Z_AXIS));
  delay(100);

  //commit to store values in flash
  EEPROM.commit();
  Serial.println("Storing calibration values in flash memory done");
  delay(1000);
}


/**
 * function to load the stored calibration from memory and set them to sensor
 */
void loadCalibrationOffsetsFromFlashMemory() {
  
  BMI160.setGyroOffset(X_AXIS, EEPROM.readShort(X_GYRO_ADD));
  delay(100);
  BMI160.setGyroOffset(Y_AXIS, EEPROM.readShort(Y_GYRO_ADD));
  delay(100);
  BMI160.setGyroOffset(Z_AXIS, EEPROM.readShort(Z_GYRO_ADD));
  delay(100);
  
  BMI160.setAccelerometerOffset(X_AXIS, EEPROM.readShort(X_ACC_ADD));
  delay(100);
  BMI160.setAccelerometerOffset(Y_AXIS, EEPROM.readShort(Y_ACC_ADD));
  delay(100);
  BMI160.setAccelerometerOffset(Z_AXIS, EEPROM.readShort(Z_ACC_ADD));
  delay(100);
  Serial.println("loading of calibration values completed");
}


// void calibrateIMU() {
//   Serial.println("Starting calibration");
//   delay(200);
//   BMI160.autoCalibrateGyroOffset();
//   delay(200);
//   BMI160.autoCalibrateAccelerometerOffset(X_AXIS,0); //param = axis, target e [-1;0;1] : 0 = 0g, 1 = 1g, 2 = 2g
//   delay(200);
//   BMI160.autoCalibrateAccelerometerOffset(Y_AXIS,0);
//   delay(200);
//   BMI160.autoCalibrateAccelerometerOffset(Z_AXIS,1);
//   Serial.println("Calibration done");
//   delay(200);

//   storeCalibrationOffsets();
//   delay(200);
// }


void setup() {
  
 Serial.begin(9600);  // Set software serial baud to 9600;
 WiFi.begin(ssid, password); // connecting to a WiFi network

 while (WiFi.status() != WL_CONNECTED) {  //connecting to WiFi
     delay(500);
     Serial.println("Connecting to WiFi..");
 }

 Serial.println("Connected to the WiFi network");
 client.setServer(mqtt_broker, mqtt_port);  //connecting to a mqtt broker

 while (!client.connected())
  {
     String client_id = "esp32-client-";
     client_id += String(WiFi.macAddress());
     Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
     if (client.connect(client_id.c_str(), mqtt_username, mqtt_password))
      {
         Serial.println("Public emqx mqtt broker connected");
      } 
     else {
         Serial.print("failed with state ");
         Serial.print(client.state());
         delay(2000);
      }
 }

 // publish and subscribe

  client.subscribe(topic);
  EEPROM.begin(EEPROM_SIZE);

  // initialize device
  BMI160.begin(BMI160GenClass::I2C_MODE, i2c_addr, interrupt_pin);
  
  BMI160.setAccelerometerRate(MEASUREMENT_FREQUENCY);
  BMI160.setGyroRate(MEASUREMENT_FREQUENCY);
  

  loadCalibrationOffsetsFromFlashMemory();

  Serial.println("RANGE");
  Serial.println(BMI160.getAccelerometerRange()); //can also set
}

/**
 * Main loop to read and send data
 */
void loop() {
  
       Serial.println("Device in void loop");        
        
    
          int gx, gy, gz;         
          int ax, ay, az;

          // read raw gyro measurements from device
          BMI160.readGyro(gx, gy, gz);
          BMI160.readAccelerometer(ax, ay, az);
          Serial.println("Accelerometer values x,y,z");
          Serial.println(ax);
          Serial.println(ay);
          Serial.println(az);
 
          // pack into standard output stream c++
          std::ostringstream s;
          s << ax << ";" << ay << ";" << az << ";" << gx << ";" << gy << ";" << gz;
          std::string payload = s.str();

          // convert into c type array[... \0]
          int n = payload.length();
          char char_array[n + 1];
          strcpy(char_array, payload.c_str());
          client.publish("esp32/ta_sensor1",char_array);

        client.loop();
        delay(500);  
       
}


