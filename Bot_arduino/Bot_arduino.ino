#include "DHT.h" //Incluimos la libreria DHT para el control de el Sensor DHT 11.

#define PinOutDHT 3 //Definimos el Pin 3 para la lectura de el sensor.
#define TypeDHT DHT11 //Definimos el Tipo de Sensor.
DHT dht(PinOutDHT, TypeDHT); //Cramos un objeto dht con las variables definidas anteriormente.
#include "Musica.h"
const int led1=12; //Declaramos la variable led1.
const int led2=2; //Declaramos la variable led2.
const int LEDPin = 13;        // pin para el LED
const int PIRPin = 7;         // pin de entrada (for PIR sensor)
int pinAlarma = 5; 
Musica musica(pinAlarma);
int sensorPin = A0;
double sensorValue;
int pirState = LOW;           // de inicio no hay movimiento
int val = 0; 
unsigned int dato; //Declaramos una variable "dato" en donde se guardaran los valores recibidos desde Python.

void setup() {
  Serial.begin(9600); //Inicializamos la comunicacion Serial a 9600 Baudios
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(LEDPin, OUTPUT); 
  pinMode(PIRPin, INPUT);
    pinMode(pinAlarma,OUTPUT);//Definimos los pines de los leds como Salidas
 
}

void loop() {

   
    while(Serial.available()>0){  //Comprobamos que la comunicacion serial este disponible.
      dato=Serial.read(); //Leemos el puerto serial y guardamos los valores en la variable "dato"
      sensorValue =  (( 5.0 * analogRead(sensorPin) * 100.0) / 1024.0);  
      /*En el siguiente codigo se compara el valor de "dato" y segun sea el caso actua de distintas maneras*/
      //Enciende o apaga los leds
        if(dato=='Y')digitalWrite(led1,HIGH);
        if(dato=='N')digitalWrite(led1,LOW);
        if(dato=='E')digitalWrite(led2,HIGH);
        if(dato=='F')digitalWrite(led2,LOW);

      //Manda Temperatura o Humedad segun el caso
        if(dato=='T')Serial.println(sensorValue +String("°C"));
        if(dato=='H')Serial.println(sensorValue +String("%"));
        if(dato=='M')
        {
           musica.reproducir();
           
        }

       }

       val = digitalRead(PIRPin);
   if (val == HIGH)   //si está activado
   { 
      digitalWrite(LEDPin, HIGH);  //LED ON
      if (pirState == LOW)  //si previamente estaba apagado
      {
        //Serial.println("Sensor activado");
        pirState = HIGH;
      }
   } 
   else   //si esta desactivado
   {
      digitalWrite(LEDPin, LOW); // LED OFF
      if (pirState == HIGH)  //si previamente estaba encendido
      {
        
        pirState = LOW;
      }
   }     
       
 
}
