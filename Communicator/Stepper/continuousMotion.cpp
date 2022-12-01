#include <AccelStepper.h>
const int BASE = 48;
const int TURN_SPEED_DIV = 3;
const int FORWARD = 8 + BASE;
const int BACKWARD = 2 + BASE;
const int STOP = 5 + BASE;
const int FORWARD_LEFT = 7 + BASE;
const int FORWARD_RIGHT = 9 + BASE;
const int BACKWARD_LEFT = 1 + BASE;
const int BACKWARD_RIGHT = 3 + BASE;
const int LOOK_LEFT = 4 + BASE;
const int LOOK_RIGHT = 6 + BASE;
//const long DEFAULT_STEPS = 800;
const long DEFAULT_SPEED = 200;
long currentSpeed_Left = 0;
long currentSpeedRight = 0;
bool newData = false;

AccelStepper stepper_Left_(1, 3, 2);
AccelStepper stepper_Right(1, 5, 4);

void setup() {
    Serial.begin(115200);
    Serial.println("Initializing..");
    stepper_Left_.setMaxSpeed(1000);
    stepper_Left_.setAcceleration(1000);
    stepper_Right.setMaxSpeed(1000);
    stepper_Right.setAcceleration(1000);
    Serial.println("Ready");
    Serial.readString();
}

void checkInput()
{
    if (Serial.available() > 0)
    {
        int data = Serial.read();
        //Serial.println(data, DEC);
        switch (data)
        {
        case FORWARD:
            //Serial.print("FORWARD -> ");
            currentSpeed_Left = DEFAULT_SPEED;
            currentSpeedRight = DEFAULT_SPEED * -1;
            break;
        case BACKWARD:
            //Serial.print("BACKWARD -> ");
            currentSpeed_Left = -1 * DEFAULT_SPEED;
            currentSpeedRight = -1 * DEFAULT_SPEED * -1;
            break;
        case FORWARD_LEFT:
            //Serial.print("FORWARD_LEFT -> ");
            currentSpeed_Left = DEFAULT_SPEED / TURN_SPEED_DIV;
            currentSpeedRight = DEFAULT_SPEED * -1;
            break;
        case FORWARD_RIGHT:
            //Serial.print("FORWARD_RIGHT -> ");
            currentSpeed_Left = DEFAULT_SPEED;
            currentSpeedRight = DEFAULT_SPEED / 2 * -1;
            break;
        case LOOK_LEFT:
            //Serial.print("LEFT -> ");
            currentSpeed_Left = DEFAULT_SPEED / TURN_SPEED_DIV * -1;
            currentSpeedRight = DEFAULT_SPEED / TURN_SPEED_DIV * -1;
            break;
        case LOOK_RIGHT:
            //Serial.print("RIGHT -> ");
            currentSpeed_Left = DEFAULT_SPEED / TURN_SPEED_DIV;
            currentSpeedRight = DEFAULT_SPEED / TURN_SPEED_DIV * -1 * -1;
            break;
        case BACKWARD_LEFT:
            //Serial.print("FORWARD_LEFT -> ");
            currentSpeed_Left = DEFAULT_SPEED / TURN_SPEED_DIV * -1;
            currentSpeedRight = DEFAULT_SPEED * -1 * -1;
            break;
        case BACKWARD_RIGHT:
            //Serial.print("FORWARD_RIGHT -> ");
            currentSpeed_Left = DEFAULT_SPEED * -1;
            currentSpeedRight = DEFAULT_SPEED / TURN_SPEED_DIV * -1 * -1;
            break;
        case STOP:
            //Serial.print("STOP -> ");
            currentSpeed_Left = 0;
            currentSpeedRight = 0;
            break;
        default:
            //Serial.print("default -> ");
            currentSpeed_Left = 0;
            currentSpeedRight = 0;
            break;
        }
        newData = false;
    }
}

void moveIt()
{
    stepper_Left_.setSpeed(currentSpeed_Left);
    stepper_Right.setSpeed(currentSpeedRight);
    stepper_Left_.runSpeed();
    stepper_Right.runSpeed();
}

void loop() {
    checkInput();
    moveIt();
}