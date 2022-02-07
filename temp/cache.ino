#include<Keyboard.h> 
void setup(){
	digitalWrite(1, HIGH);
	delay(10);
	Keyboard.print("Hello World");
	delay(1);
	Keyboard.print("It's me");
	digitalWrite(1, LOW);
	Keyboard.print("led");
	delay(909);
	digitalWrite(1, HIGH);
	Keyboard.print("heeeee");

}
void loop {}