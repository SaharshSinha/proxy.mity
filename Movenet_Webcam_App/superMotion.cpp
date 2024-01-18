#include <AccelStepper.h>

int _base_speed_LEFT = 20;
int _base_speed_RITE = 20;
int _base_speed_X_RT = 20;
int _base_speed_Y_RT = 20;

AccelStepper stepper_LEFT(1, 3, 2);
AccelStepper stepper_RITE(1, 5, 4);
AccelStepper stepper_X_RT(1, 6, 7);
AccelStepper stepper_Y_RT(1, 6, 7);

int stepper_MUX_LEFT = 0;
int stepper_MUX_RITE = 0;
int stepper_MUX_X_RT = 0;
int stepper_MUX_Y_RT = 0;
const int BASE_MARK = 10000;
const int BASE_MARK_LEFT = 10001;
const int BASE_MARK_RITE = 10002;
const int BASE_MARK_X_RT = 10003;
const int BASE_MARK_Y_RT = 10004;
const int SKIP_MARK = 11000;

void setup() {
    Serial.begin(115200);
    Serial.println("Initializing..");
    stepper_LEFT.setMaxSpeed(1000);
    stepper_LEFT.setAcceleration(1000);
    stepper_RITE.setMaxSpeed(1000);
    stepper_RITE.setAcceleration(1000);
    stepper_X_RT.setMaxSpeed(10000);
    stepper_X_RT.setAcceleration(1000);
    stepper_Y_RT.setMaxSpeed(10000);
    stepper_Y_RT.setAcceleration(1000);
    Serial.println("Ready");
    Serial.readString();
}

void checkIt()
{
    while (Serial.available() > 0)
    {
        int value_1 = Serial.parseInt();
        int value_2 = Serial.parseInt();
        int value_3 = Serial.parseInt();
        int value_4 = Serial.parseInt();
        if (Serial.read() == '\n') {
            
            if (value_1 == BASE_MARK && value_2 == BASE_MARK) 
            {
              if( value_3 == BASE_MARK_X_RT) { _base_speed_X_RT = value_4; }
              if( value_3 == BASE_MARK_Y_RT) { _base_speed_Y_RT = value_4; }
              if( value_3 == BASE_MARK_LEFT) { _base_speed_LEFT = value_4; }
              if( value_3 == BASE_MARK_RITE) { _base_speed_RITE = value_4; }
            }

            if (value_1 != SKIP_MARK) { stepper_MUX_X_RT = value_1; }
            if (value_2 != SKIP_MARK) { stepper_MUX_Y_RT = value_2; }
            if (value_3 != SKIP_MARK) { stepper_MUX_LEFT = value_3; }
            if (value_4 != SKIP_MARK) { stepper_MUX_RITE = value_4; }
            Serial.println(String(stepper_MUX_X_RT) + "; " + String(stepper_MUX_Y_RT) + "; " + String(stepper_MUX_LEFT) + "; " + String(stepper_MUX_RITE) );
        }
    }
}

void moveIt()
{
    stepper_LEFT.setSpeed(stepper_MUX_LEFT * _base_speed);
    stepper_RITE.setSpeed(stepper_MUX_RITE * _base_speed);
    stepper_X_RT.setSpeed(stepper_MUX_X_RT * _base_speed);
    stepper_Y_RT.setSpeed(stepper_MUX_Y_RT * _base_speed);

    stepper_LEFT.runSpeed();
    stepper_RITE.runSpeed();
    stepper_X_RT.runSpeed();
    stepper_Y_RT.runSpeed();
}

void loop() {
    checkIt();
    moveIt();
}