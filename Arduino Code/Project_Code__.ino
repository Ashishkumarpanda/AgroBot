#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN 2  
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int sensor_pin = A0; // Soil Sensor input at Analog PIN A0

int output_value ;

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT Sensor! and Reading from Moisture Sensor"));

  delay(2000);
  
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);
   output_value= analogRead(sensor_pin);

   output_value = map(output_value,550,0,0,100);


  Serial.print(F(" Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("C "));
  Serial.print(f);
  Serial.print(F("F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("C "));
  Serial.print(hif);
  Serial.println(F("F"));
  Serial.print("Mositure : ");
  Serial.print(output_value);
  Serial.println("%");

  delay(1000);
}
