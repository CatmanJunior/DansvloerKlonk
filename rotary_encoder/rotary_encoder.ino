/*     Arduino Rotary Encoder Tutorial
 *      
 *  by Dejan Nedelkovski, www.HowToMechatronics.com
 *  
 */
 
 #define outputA 2
 #define outputB 3
 int counter = 0; 
 int aState;
 int aLastState;  
 void setup() { 
   pinMode (outputA,INPUT);
   pinMode (outputB,INPUT);
   pinMode(7,OUTPUT);
   
   Serial.begin(9600);
   Serial.println("so gay");
   // Reads the initial state of the outputA
   aLastState = digitalRead(outputA);   
 } 
 void loop() { 
  int toonh = map(counter,100, -100, 0, 2000);
   aState = digitalRead(outputA); // Reads the "current" state of the outputA
   // If the previous and the current state of the outputA are different, that means a Pulse has occured
   if (aState != aLastState){     
     // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
     if (digitalRead(outputB) != aState) { 
       counter ++;
     } else {
       counter --;
     }
   // Serial.print("Position: ");
     //Serial.println(counter);
     
     Serial.write(toonh);
     delay(10);
     //tone(7, toonh, 50);
   }  
   aLastState = aState; // Updates the previous state of the outputA with the current state
   //Serial.write(1);
  // delay(100);
 }
