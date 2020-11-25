
#define NO_DEBUG 0
#define DEBUG_RW 1
#define DEBUG_STICK 2
#define SPEED_TEST 3
/*
 ********* PARAMS TO SET*************
*/

const int numGrid = 16;
const int debugMode = NO_DEBUG; // 0: no debug, 1: read/write debug, 2: stick debug
const float minX = 763.0;
const float maxX = 349.0;
const float minY = 686.0;
const float maxY = 240.0;
const float motorXGain = 1.0; // Scales the final output of motor X to balance both motors
const float motorYGain = 0.6; // Scales the final output of motor Y to balance both motors

/**************************/


#include <math.h>

const int vcaXP = 2; // forward vs backward
const int vcaXE = 3; // power (PWM)
const int potXPin = A15;
const int vcaYP = 4; // forward vs backward
const int vcaYE = 5; // power (PWM)
const int potYPin = A14;

// button pins
const int btnAPin = 31;
const int btnBPin = 32;
const int btnXPin = 30;
const int btnYPin = 29;


const int mapSize = numGrid * numGrid * 2 * sizeof(byte); // sizeof(byte) = 1 byte;
const int vectorSize = sizeof(byte) * 2;
const int numVectorInMap = mapSize / vectorSize;

typedef union force_map
{
  byte buf[mapSize];
  byte grid[numGrid][numGrid][2];
};

const int pointSize = sizeof(uint8_t) * 3;
typedef union force_point
{
  struct
  {
    byte x;
    byte y;
    byte useMap;
  } value;
  byte buf[pointSize];
};

static force_map forceMap;
static force_point forcePoint;

// code protocol
const char mapCode = 'm';
const char pointCode = 'p';
const char successCode = 's';

// value holders
int potXPos = 0;
int potYPos = 0;
int forceXP = 0;
int forceXE = 0;
int forceYP = 0;
int forceYE = 0;
int stickMode = 1;
// posistion values, -1~1
float posX = 0;
float posY = 0;
// button states. pressed : 1, not pressed : 0
int btnA = 0;
int btnB = 0;
int btnX = 0;
int btnY = 0;

// time checker for serial output rate
long timepassed = 0;
long serOutRate = 250; // 250Hz
bool stringComplete = false;

// prev pot value for damping
int prevPotX = -1000;
int prevPotY = -1000;

void setup() {

  pinMode(vcaXP, OUTPUT);
  pinMode(vcaXE, OUTPUT);
  pinMode(vcaYP, OUTPUT);
  pinMode(vcaYE, OUTPUT);

  pinMode(btnAPin, INPUT);
  pinMode(btnXPin, INPUT);
  pinMode(btnYPin, INPUT);
  pinMode(btnBPin, INPUT);

  // Modify PWM frequency & resolution
  analogWriteFrequency(vcaXE, 20000); // pwm freq: 20kHz (lower than teensy freq.'s half), 50kHz made noise
  analogWriteFrequency(vcaYE, 20000);
  analogWriteResolution(7); // pwm value range: 0~127

  for (int i = 0; i < numGrid; i++) {
    for (int j = 0; j < numGrid; j++) {
      forceMap.grid[i][j][0] = 0;
      forceMap.grid[i][j][1] = 0;
    }
  }

  forcePoint.value.x = 0;
  forcePoint.value.y = 0;
  forcePoint.value.useMap = 1;


  Serial.begin(115200);
  while (!Serial);

  timepassed = micros();
}

void loop() {

  char code = '?';

  if (Serial.available())
  {
    code = Serial.read();
  }

  if (code == mapCode)
  {
    updateForceMap();
  }
  else if (code == pointCode)
  {
    updateForcePoint();
  }

  updateButtons();
  updateStick();

  if (micros() - timepassed > pow(10, 6) / serOutRate)
  {
    sendControllerState();
    timepassed = micros();
  }
}


void updateButtons()
{
  btnA = getButtonPressed(btnAPin);
  btnB = getButtonPressed(btnBPin);
  btnX = getButtonPressed(btnXPin);
  btnY = getButtonPressed(btnYPin);
}

int getButtonPressed(int pin)
{
  int val = digitalRead(pin);
  if (val == 0) // LOW
  {
    return 1;
  }
  else // HIGH
  {
    return 0;
  }
}

void updateStick()
{
  int potX = analogRead(potXPin); // raw potentiometer value (0~1024)
  int potY = analogRead(potYPin);
  int dX;
  int dY;

  posX = pot2PosX(potX);  // convert raw pot value to position value (0~numGrid-1)
  posY = pot2PosY(potY);

  // Apply force point's value
  int forceX = ubyte2sint(forcePoint.value.x);
  int forceY = ubyte2sint(forcePoint.value.y);

  // Apply force map's value if available.
  // calculates the interpolated vector of surrounding 4 grids.
  if (forcePoint.value.useMap)
  {
    interpForceMap(posX, posY, forceX, forceY); // forceX is PWM value, 0 to 127

    /*
    if(prevPotX == -1000){
      prevPotX = potX;
      dX = -1000;
    }
    else{
      dX = potX - prevPotX;
      prevPotX = potX;
    }
    if(prevPotY == -1000){
      prevPotY = potY;
      dY = -1000;
    }
    else{
      dY = potY - prevPotY;
      prevPotY = potY;
    }

    raw_damping(dX, dY,&forceX, &forceY);
    */
  }

  if (debugMode == DEBUG_STICK)
  {

    Serial.print(potX);
    Serial.print(',');
    Serial.print(potY);
    Serial.print(',');

    Serial.print(posX);
    Serial.print(',');
    Serial.print(posY);
    Serial.print('\n');
    delay(100);
  }
  else if (debugMode == NO_DEBUG)
  {
    forceStickX(forceX);
    forceStickY(forceY);
  }
}

void updateForcePoint()
{
  if (Serial.available())
  {
    Serial.readBytes((char*) forcePoint.buf, pointSize);

    if (debugMode == DEBUG_RW)
    {
      Serial.print(forcePoint.value.x);
      Serial.print(',');
      Serial.print(forcePoint.value.y);
      Serial.print(',');
      Serial.print(forcePoint.value.useMap);
      Serial.print('\n');
    }
    else if (debugMode == SPEED_TEST)
    {
      Serial.write('s');
    }
  }
}

void updateForceMap()
{
  if (Serial.available())
  {
    Serial.readBytes((char*) forceMap.buf, mapSize);

    if (debugMode == DEBUG_RW)
    {
      for (int i = 0; i < numVectorInMap; i++)
      {
        int row = i / numGrid;
        int col = i - row * numGrid;
        Serial.print(row);
        Serial.print(',');
        Serial.print(col);
        Serial.print(',');
        Serial.print(forceMap.grid[row][col][0]);
        Serial.print(',');
        Serial.print(forceMap.grid[row][col][1]);
        Serial.print('\n');
      }
    }
    else if (debugMode == SPEED_TEST)
    {
      Serial.write('s');
    }
  }
}

float filterX(float delta){ // filter for X value for dead zone
  if(delta < 1.5 && delta >-1.5){
    return 0;
  }
  else{
    return delta;
  }
}

float filterY(float delta){ // filter for Y value for dead zone
  if(delta < 3 && delta >-3){
    return 0;
  }
  else{
    return delta;
  }
}

void raw_damping(float dX, float dY, int* forceX, int* forceY){ //raw_damping(dX, dY, &forceX, &forceY);
  if(dX != -1000){
    *forceX -= 10 * filterX(dX);
  }
  if(dY != -1000){
    *forceY -= 12 * filterY(dY);
  }
}

void sendControllerState()
{
  if (debugMode == NO_DEBUG)
  {
    char line[18];
    sprintf(line, "%.2f,%.2f,%d,%d,%d,%d\n", posX, posY, btnA, btnB, btnX, btnY);
    Serial.print(line);
  }
}

int ubyte2sint(byte val)
{
  return (int)(-(val & 0x80) + (val & 0x7F));
}

float pot2PosX(float potVal)
{
  // float posVal = -0.0044 * potVal + 2.0911;
  float posVal = 2 / (maxX - minX) * potVal + (minX + maxX) / (minX - maxX);
  if (posVal > 1)
    posVal = 1;
  else if (posVal < -1)
    posVal = -1;
  return -posVal;
}

float pot2PosY(float potVal)
{
  // float posVal = -0.0049 * potVal + 2.6422;
  float posVal = 2 / (maxY - minY) * potVal + (minY + maxY) / (minY - maxY);
  if (posVal > 1)
    posVal = 1;
  else if (posVal < -1)
    posVal = -1;
  return -posVal;
}

void interpForceMap(float x, float y, int& outputX, int& outputY)
{
  float gridCoordX = (numGrid - 1) / 2 * x + (numGrid - 1) / 2;
  float gridCoordY = (numGrid - 1) / 2 * y + (numGrid - 1) / 2;
  int floorX = (int)floor(gridCoordX);
  int floorY = (int)floor(gridCoordY);
  float ratioX = gridCoordX - (float)floorX;
  float ratioY = gridCoordY - (float)floorY;
  int ceilX = floorX > 15 ? floorX : floorX + 1;
  int ceilY = floorY > 15 ? floorY : floorY + 1;
  floorX = floorX < 0 ? 0 : floorX;
  floorY = floorY < 0 ? 0 : floorY;

  // bilinear interpolation
  outputX += ubyte2sint(forceMap.grid[floorX][floorY][0]) * (1 - ratioX) * (1 - ratioY) +
             ubyte2sint(forceMap.grid[floorX][ceilY][0]) * (1 - ratioX) * ratioY +
             ubyte2sint(forceMap.grid[ceilX][floorY][0]) * ratioX * (1 - ratioY) +
             ubyte2sint(forceMap.grid[ceilX][ceilY][0]) * ratioX * ratioY;
  outputY += ubyte2sint(forceMap.grid[floorX][floorY][1]) * (1 - ratioX) * (1 - ratioY) +
             ubyte2sint(forceMap.grid[floorX][ceilY][1]) * (1 - ratioX) * ratioY +
             ubyte2sint(forceMap.grid[ceilX][floorY][1]) * ratioX * (1 - ratioY) +
             ubyte2sint(forceMap.grid[ceilX][ceilY][1]) * ratioX * ratioY;

  return;
}

void forceStickX(int val)
{
  val = (int)((float)val * motorXGain);
  forceStick(vcaXP, vcaXE, val, HIGH);
}

void forceStickY(int val)
{
  val = (int)((float)val * motorYGain);
  forceStick(vcaYP, vcaYE, val, HIGH);
}

void forceStick(int phasePin, int enablePin, int val, int plusPhase)
{
  int absVal = 0;
  int minusPhase = LOW;
  if (plusPhase == LOW)
  {
    minusPhase = HIGH;
  }

  if (val < 0)
  {
    digitalWrite(phasePin, minusPhase);
    absVal = abs(val);
  }
  else
  {
    digitalWrite(phasePin, plusPhase);
    absVal = val;
  }
  analogWrite(enablePin, absVal);
}
