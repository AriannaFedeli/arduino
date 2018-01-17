int freq;
double sped;

double speed_max = 50;
double speed_min = 0;
int freq_max = 100;
int freq_min;
double distance=0;
int ENERGY_PERCENT_GAINED;
int ENERGY_PERCENT_TROTTO_USED;
int ENERGY_PERCENT_GALOPPO_USED;
int ENERGY_PERCENT_RECOVER_AFTER;
int ENERGY_MAX=80;
// the lower it is, more stable is the horse with speed.
int HORSE_TRAINING;
//horse training speed is beetween 1 and 2
int HORSE_TRAINING_SPEED;
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
    randomSeed(analogRead(0));
  // put your setup code here, to run once:  

  ENERGY_PERCENT_GAINED = random(15,25);
  ENERGY_PERCENT_TROTTO_USED =random(-7,-1);
  ENERGY_PERCENT_GALOPPO_USED=random(-12,-6);
  ENERGY_PERCENT_RECOVER_AFTER=25;
  ENERGY_MAX=random(80,120);
  HORSE_TRAINING=random(7,11);
  HORSE_TRAINING_SPEED=2;
  sped = 0;
  energy = energyMax;
  freq = computeHeartRate(sped);
  Serial.begin(9600);

}

int computeHeartRate(double sped){
  if (sped >= 0 && sped < 5){
    //Serial.println("passo");
    return int(2.5*sped+30);
  }else
  if (sped >= 5 && sped < 20){
    //Serial.println("trotto");
    return int(5.57377*sped+24.5902);
  }else
  if (sped >= 20){
    //Serial.println("galoppo");
    return int(( -1*((sped*sped)/5) + 18*sped -180));
  }
}



int computeIncrement(){
   double energyHalf = energyMax/HORSE_TRAINING_SPEED;
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
  distance = distance + (sped*1000)/3600;
  Serial.print(freq);
  Serial.print(",");
  Serial.print(sped);
  Serial.print(",");
  Serial.println(distance);
  delay(1000); // wait.
}

