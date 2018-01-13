int freq;
double sped;

double speed_max = 40;
double speed_min = 0;
int freq_max = 100;
int freq_min;

#define ENERGY_MAX 500

#define ENERGY_PERCENT_GAINED 10
#define ENERGY_PERCENT_TROTTO_USED -5
#define ENERGY_PERCENT_GALOPPO_USED -15
#define ENERGY_PERCENT_RECOVER_AFTER 5
#define ENERGY_MAX 500
// the lower it is, more stable is the horse with speed.
#define HORSE_TRAINING 10

int minAccelleration = -5;
int maxAccelleration = 10;
double energy;
double energyMax = ENERGY_MAX;

void incrEnergy(int incr){
  if (energy + incr <= energyMax && energy + incr >= 0){
    
    energy += incr; 
  } else 
  if (energy + incr > energyMax){
    energy = energyMax;
  }else {
    energy = 0;
  }
  
}
void setup() {
  // put your setup code here, to run once:  
  sped = 0;
  energy = energyMax;
  freq = computeHeartRate(sped);
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

int computeHeartRate(double sped){
  if (sped >= 0 && sped < 5){
    Serial.println("passo");
    return int(2.5*sped+30);
  }else
  if (sped >= 5 && sped < 30){
    Serial.println("trotto");
    return int(5.57377*sped+24.5902);
  }else
  if (sped >= 30){
    Serial.println("galoppo");
    return int(( -1*((sped*sped)/5) + 18*sped -180));
  }
}



int computeIncrement(){
   double energyHalf = energyMax/2;
   double energyLeft = energyHalf - (energyMax/HORSE_TRAINING);
   double energyRight = energyHalf + (energyMax/HORSE_TRAINING);
   
   if (energy < energyLeft){ // left.
     return ((-(minAccelleration)/(energyLeft))*energy) + minAccelleration;
   }else if (energy > energyRight){ // right
     return ((energy-energyRight)/(energyMax - energyRight))*maxAccelleration;
   } else { // in the middle.
     return 0; // no variation. ideal case.
   }
}

void computeEnergy(){
  
 if (sped >= 0 && sped < 5){
    incrEnergy((energyMax*ENERGY_PERCENT_GAINED)/100);
  }else
  if (sped >= 5 && sped < 30){
    incrEnergy((energyMax*ENERGY_PERCENT_TROTTO_USED)/100);
  }else
  if (sped >= 30){
    // 
    incrEnergy((energyMax*ENERGY_PERCENT_GALOPPO_USED)/100);
    //return int(( -1*((sped*sped)/5) + 18*sped -180));
  }
  
}

void loop() {

  int increment = computeIncrement();
  
  
  
  sped += increment ; // calcola la variazione di velocità.
  
  // overflow.
  if (sped <= speed_min) {
    sped = speed_min;
  }else
  if (sped >= speed_max) {
    sped = speed_max;
  }
  if (increment < 0){
    incrEnergy((energyMax*ENERGY_PERCENT_RECOVER_AFTER)/100);
     // recover energy.
  }
  
  computeEnergy(); // after the effort fix energy.
  
  freq = computeHeartRate(sped);
  
  Serial.print(freq);
  Serial.print("|");
  
  Serial.print(sped);
  Serial.print("|");
  Serial.println(energy);
  
  
  //quando scrivo devo pure fare la post al server, rimane da gestire la cosa del capire a che trend mi sto riferendo per inviare le misurazioni

  delay(1000); // wait.
}

