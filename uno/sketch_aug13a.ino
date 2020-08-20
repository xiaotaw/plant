/*
  单片机程序
*/
const int heartPin = A1;
const int n = 1000;
int i = 0;

void setup() {
  Serial.begin(115200);
  for(int i=0; i<500; i++) analogRead(heartPin); 
  Serial.flush();
}


void func_ori(){
  unsigned int val = analogRead(heartPin);
  Serial.print(val);
  Serial.print('\n');
  delayMicroseconds(162);
}

void func(){
  unsigned int val = analogRead(heartPin);
  Serial.print(char(val));
  Serial.print(char(val >> 8));
  if(i>n) {
    i = 0;
    Serial.println();
  }  i++;
  // change delay time, to get the frequence you want
  delayMicroseconds(78);
}

// 用于测试速度和采样频率
void test_speed(){
  long begt, runt;
  begt = micros();
  for(int i=0; i<n; i++){
    func_ori();
  }
  runt = micros() - begt;
  Serial.println();
  Serial.print(String("Time per sample: ")+runt/1.0/n +"us");
  Serial.println(String(", Frequency: ")+1000000.0/runt*n +" Hz");
  delay(5000);
}


void loop() {
  func_ori();
  //test_speed();
  //func();
}
