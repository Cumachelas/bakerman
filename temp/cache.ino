#include<Keyboard.h> 
void setup(){
	digitalWrite(1, HIGH);
	delay(10);
	Keyboard.print("Hello Worlds, hello");
	delay(1);
	Keyboard.print("It's me, my frieeeeend");
	digitalWrite(1, LOW);
	Keyboard.print("led");
	delay(909);
	digitalWrite(1, HIGH);
	Keyboard.print("heeheheheeee");

}
void loop {}