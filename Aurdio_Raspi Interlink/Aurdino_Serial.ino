/* 
This code is used to test whether the serial communication is bridged or not. 

*/




void setup() {
Serial.begin(115200);
while (!Serial) {}
}

void loop() {
Serial.println("Hello from Arduino");
delay(1000);

}
