int freq;
double sped;

double speed_max = 130;
double speed_min = 0;
int freq_max = 100;
int freq_min;

int freq_var = 0;
int speed_var = 0;


int clk = 0;
void setup() {
  // put your setup code here, to run once:
  randomSeed(analogRead(0));
  freq_min= random(30,40);
  freq = random(freq_min,freq_max);
  sped = random(speed_min,speed_max);
  Serial.begin(9600);

  
}

void loop() {   
  speed_var = random(10);
  
  if (clk == 59 ){
     // effettua la misura del valore di frequenza cardiaca.
    freq_var = random(10);
    freq += (random(2)==1)?+1:-1 * freq_var;
  }
  clk++;
  
  speed_var = random(10,20) ;
  int increment = (random(100)>80)?+1:-1;
  
  if (sped < 2){
    increment = +1;
  }
  if (sped > speed_max - 30){
    increment = -1;
  }
  
  sped += ( increment * speed_var ); // calcola la variazione di velocità.

  // overflow.  
  
  if (freq < freq_min){
    freq = freq_min;
  }
  if (freq > freq_max){
    freq = freq_max;
  }
  
  if (sped < speed_min){
    sped = speed_min;
  }
  if (sped > speed_max){
    sped = speed_max;
  } 
  Serial.println(String(freq)+"|"+String(sped)); // invia il valore al pc.
  
  delay(1000); // wait.
}
