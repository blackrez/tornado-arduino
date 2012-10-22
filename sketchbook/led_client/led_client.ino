//Running LED display: Three LEDs connected to Digital Pin 9, 10 and 11.

int led_read = 0;
 
void setup()   
{                
  pinMode(13, OUTPUT);        // Initialize Arduino Digital Pins 9 as output
  pinMode(12, OUTPUT);       // Initialize Arduino Digital Pins 10 as output
  pinMode(11, OUTPUT);       // Initialize Arduino Digital Pins 11 as output
  Serial.begin(9600);
}
 
 
void loop()                     
{
  led_read = Serial.parseInt();
  if (led_read == 1){
    digitalWrite(13, !digitalRead(13));
    Serial.print(digitalRead(13));
  }
  if (led_read == 2){
    digitalWrite(12, !digitalRead(12));
    Serial.print(digitalRead(12));
  }
  delay(250);
  
}
