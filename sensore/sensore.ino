int freq;
double sped;

double speed_max = 130;
double speed_min = 0;
int freq_max = 100;
int freq_min;

int speed_var = 0;


int clk = 0;
void setup() {
  // put your setup code here, to run once:  
  sped = 0;
  freq = computeHeartRate(sped);
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

int computeHeartRate(double sped){
  if (sped >= 0 && sped < 5){
    return int(2.5*sped+30);
  }else
  if (sped >= 5 && sped < 30){
    return int(5.57377*sped+24.5902);
  }else
  if (sped >= 30){
    return int(( -1*((sped*sped)/5) + 18*sped -180));
  }
  
}

void loop() {
  if (sped < 10){
    speed_var = random(3,6);
  }
  if (sped >= 10 && sped < 20){
    speed_var = random(3,6);
  }
  if (sped >= 20 && sped < 30){
    speed_var = random(3,6);
  }
  
  int increment = (random(100) > 80) ? +1 : -1;

  if (sped < 2) {
    increment = +1;
  }
  if (sped > speed_max - 30) {
    increment = -1;
  }

  sped += ( increment * speed_var ); // calcola la variazione di velocità.

  // overflow.

  if (sped < speed_min) {
    sped = speed_min;
  }
  if (sped > speed_max) {
    sped = speed_max;
  }
  freq = computeHeartRate(sped);
  
  Serial.println(String(freq) + "|" + String(sped)); // invia il valore al pc.

  delay(1000); // wait.
}

