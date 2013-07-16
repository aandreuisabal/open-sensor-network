#include "XBee.h"
#include "unions.h"
#include "DHT.h"

#define DHTPIN 2 //data pin of the DHT sensor
#define DHTTYPE DHT22 //DHT 22

#define SOUND_SENSOR_PIN 0

#define SUCCESS_LED 13
#define ERROR_LED 13


/****************************************************
 ***** Initializes the main XBee object and DHT
 ***************************************************/

XBee xbee = XBee();
DHT dht(DHTPIN, DHTTYPE);


/****************************************************
 ***** PAYLOAD MEMORY ALLOCATION
 ***** 
 ***** More info on data types & their sizes:
 ***** http://arduino.cc/en/Reference/HomePage
 ***** http://docs.python.org/2/library/struct.html
 ***************************************************/

uint8_t payload[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; //number of bytes to be sent


/****************************************************
 ***** Specific ZigBee parameters
 ***************************************************/

XBeeAddress64 addr64 = XBeeAddress64(0x00000000, 0x00000000); //can be changed
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();



/****************************************************
 ***** VARIABLES THAT WILL BE SENT
 ***************************************************/

int METADATA = 999;
float temperature;
float humidity;
float noise;


/****************************************************
 ***** NECESSARY UNIONS
 ***************************************************/

float_union fu;
int_union iu;


/****************************************************
 ***** Auxiliary functions
 ***************************************************/

void flashLed(int iopin, int reps, int d)
{
    for (int i = 0; i<reps; i++) {
        // led ON
        digitalWrite(iopin, HIGH);
        // wait
        delay(d);
        // led OFF
        digitalWrite(iopin, LOW);

        // if not last iteration wait again
        if (i + 1 < reps) {
            delay(d);
        }
    }
}

float getAverage(int pin, int samples, int wait) {

    float avg = 0.0;

    for (int i=0; i<samples; i++) {
        avg += analogRead(pin);
        delay(wait);
    }

    return avg/samples;
}


/****************************************************
 ***** SETUP()
 ***************************************************/

void setup() {

    pinMode(SUCCESS_LED, OUTPUT);
    pinMode(ERROR_LED, OUTPUT);

    xbee.begin(9600);
}


/****************************************************
 ***** LOOP()
 ***************************************************/

void loop() {   

    int aux = 0;
    
    // DATA GATHERING
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    noise = getAverage(SOUND_SENSOR_PIN, 10, 50);

    iu.i = METADATA;
    for (int i=0; i<UNSIGNED_INT_SIZE; i++){
        payload[i]=iu.b[i];
        aux++;
    }
    
    // PAYLOAD FILLING
    fu.f = temperature;
    for (int i=0; i<FLOAT_SIZE; i++){
        payload[i+4]=fu.b[i];
        aux++;
    }

    fu.f = humidity;
    for (int i=0; i<FLOAT_SIZE; i++){
        payload[i+8]=fu.b[i];
        aux++;
    }

    fu.f = noise;
    for (int i=0; i<FLOAT_SIZE; i++){
        payload[i+12]=fu.b[i];
        aux++;
    } 

    xbee.send(zbTx);

    flashLed(SUCCESS_LED, 1, 100);

    if (xbee.readPacket(600)) {
        // Response must be ZX_TX_STATUS_RESPONSE
        if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {

            xbee.getResponse().getZBTxStatusResponse(txStatus);

            if (txStatus.getDeliveryStatus() == SUCCESS) {
                // SUCCESS, flash 5 times every 50ms
                flashLed(SUCCESS_LED, 5, 50);
            } else {
                // ERROR, flash 3 times in every 500ms
                flashLed(ERROR_LED, 3, 500);
            }
        }
    } else {
        // ERROR, flash 2 times in every 50ms
        flashLed(ERROR_LED, 2, 50);
    }

    delay(1000);
}
