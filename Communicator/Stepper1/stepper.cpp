#include <AccelStepper.h>

long receivedMMdistance = 0; //distance in mm from the computer
long receivedDelay = 0; //delay between two steps, received from the computer
long receivedAcceleration = 0; //acceleration value from computer
char receivedCommand; //character for commands
long defaultSteps = 800;
long defaultSpeed = 200;
long stepsToExecute_Left_ = 0;
long stepsToExecute_Right = 0;
/* s = Start (CCW) // needs steps and speed values
 * o = open (CCW) // needs steps and speed values
 * c = close (CW) //needs steps and speed values
 * a = set acceleration // needs acceleration value
 * n = stop right now! // just the 'n' is needed
 */

bool newData, runallowed = false; // booleans for new data from serial, and runallowed flag



// direction Digital 9 (CCW), pulses Digital 8 (CLK)
AccelStepper stepper_Left_(1, 3, 2);
AccelStepper stepper_Right(1, 5, 4);


void setup()
{
    Serial.begin(9600); //define baud rate
    Serial.println("Testing Accelstepper"); //print a message

    //setting up some default values for maximum speed and maximum acceleration
    stepper_Left_.setMaxSpeed(2000); //SPEED = Steps / second
    stepper_Left_.setAcceleration(1000); //ACCELERATION = Steps /(second)^2
    stepper_Left_.disableOutputs(); //disable outputs, so the motor is not getting warm (no current)

    stepper_Right.setMaxSpeed(2000); //SPEED = Steps / second
    stepper_Right.setAcceleration(1000); //ACCELERATION = Steps /(second)^2
    stepper_Right.disableOutputs(); //disable outputs, so the motor is not getting warm (no current)


}

void loop()
{

    checkSerial(); //check serial port for new commands

    continuousRun2(); //method to handle the motor

}


void continuousRun2() //method for the motor
{
    if (runallowed == true)
    {
        bool didntMove = true;

        if (abs(stepper_Left_.currentPosition()) < stepsToExecute_Left_) //abs() is needed because of the '<'
        {
            stepper_Left_.enableOutputs(); //enable pins
            stepper_Left_.run(); //step the motor (this will step the motor by 1 step at each loop)
            didntMove = false;
        }
        else
        {
            stepper_Left_.disableOutputs(); // disable power
            stepper_Left_.setCurrentPosition(0); //reset the position to zero
        }

        if (abs(stepper_Right.currentPosition()) < stepsToExecute_Right) //abs() is needed because of the '<'
        {
            stepper_Right.enableOutputs(); //enable pins
            stepper_Right.run(); //step the motor (this will step the motor by 1 step at each loop)
            didntMove = false;
        }
        else
        {
            stepper_Right.disableOutputs(); // disable power
            stepper_Right.setCurrentPosition(0); //reset the position to zero
        }

        if (didntMove) //program enters this part if the required distance is completed
        {
            runallowed = false; //disable running -> the program will not try to enter this if-else anymore
            Serial.print("POS: ");
            Serial.println(stepper_Left_.currentPosition()); // print pos -> this will show you the latest relative number of steps
            Serial.print("POS: ");
            Serial.println(stepper_Left_.currentPosition()); // print pos -> this will show you the latest relative number of steps; we check here if it is zero for real
        }


    }
    else //program enters this part if the runallowed is FALSE, we do not do anything
    {
        return;

    }
}

void checkSerial() //method for receiving the commands
{
    //switch-case would also work, and maybe more elegant

    if (Serial.available() > 0) //if something comes
    {
        receivedCommand = Serial.read(); // this will read the command character
        newData = true; //this creates a flag
    }

    if (newData == true) //if we received something (see above)
    {
        //START - MEASURE
        if (receivedCommand == 's') //this is the measure part
        {
            runallowed = true; //allow running
            receivedMMdistance = Serial.parseFloat(); //value for the steps
            receivedDelay = Serial.parseFloat(); //value for the speed
            Serial.print(receivedMMdistance); //print the values for checking
            Serial.print(receivedDelay);
            Serial.println("Measure "); //print the action
            stepsToExecute_Left_ = defaultSteps;
            stepsToExecute_Right = defaultSteps;

            stepper_Left_.setMaxSpeed(defaultSpeed); //set speed
            stepper_Left_.move(stepsToExecute_Left_); //set distance
            stepper_Right.setMaxSpeed(defaultSpeed); //set speed
            stepper_Right.move(-1 * stepsToExecute_Right); //set distance

        }

        if (receivedCommand == 'w') //OPENING
        {
            runallowed = true; //allow running
            receivedMMdistance = Serial.parseFloat(); //value for the steps
            receivedDelay = Serial.parseFloat(); //value for the speed
            Serial.print(receivedMMdistance); //print the values for checking
            Serial.print(receivedDelay);
            Serial.println("OPEN "); //print the action
            stepsToExecute_Left_ = defaultSteps;
            stepsToExecute_Right = defaultSteps;
            stepper_Left_.setMaxSpeed(defaultSpeed); //set speed
            stepper_Left_.move(stepsToExecute_Left_); //set distance
            stepper_Right.setMaxSpeed(defaultSpeed); //set speed
            stepper_Right.move(-1 * stepsToExecute_Right); //set distance
        }

        if (receivedCommand == 'e') //OPENING
        {
            runallowed = true; //allow running
            receivedMMdistance = Serial.parseFloat(); //value for the steps
            receivedDelay = Serial.parseFloat(); //value for the speed
            Serial.print(receivedMMdistance); //print the values for checking
            Serial.print(receivedDelay);
            Serial.println("OPEN "); //print the action
            stepsToExecute_Left_ = defaultSteps / 2;
            stepsToExecute_Right = defaultSteps / 12;
            stepper_Left_.setMaxSpeed(defaultSpeed); //set speed
            stepper_Left_.move(stepsToExecute_Left_); //set distance
            stepper_Right.setMaxSpeed(defaultSpeed); //set speed
            stepper_Right.move(-1 * stepsToExecute_Right); //set distance
        }

        if (receivedCommand == 'q') //OPENING
        {
            runallowed = true; //allow running
            receivedMMdistance = Serial.parseFloat(); //value for the steps
            receivedDelay = Serial.parseFloat(); //value for the speed
            Serial.print(receivedMMdistance); //print the values for checking
            Serial.print(receivedDelay);
            Serial.println("OPEN "); //print the action
            stepsToExecute_Left_ = defaultSteps / 12;
            stepsToExecute_Right = defaultSteps / 2;
            stepper_Left_.setMaxSpeed(defaultSpeed); //set speed
            stepper_Left_.move(stepsToExecute_Left_); //set distance
            stepper_Right.setMaxSpeed(defaultSpeed); //set speed
            stepper_Right.move(-1 * stepsToExecute_Right); //set distance
        }

        //START - CLOSE
        if (receivedCommand == 'x') //CLOSING - Rotates the motor in the opposite direction as opening
        {
            runallowed = true; //allow running
            receivedMMdistance = Serial.parseFloat(); //value for the steps
            receivedDelay = Serial.parseFloat(); //value for the speed
            Serial.print(receivedMMdistance);  //print the values for checking
            Serial.print(receivedDelay);
            Serial.println("CLOSE "); //print action
            stepsToExecute_Left_ = defaultSteps;
            stepsToExecute_Right = defaultSteps;
            stepper_Left_.setMaxSpeed(defaultSpeed); //set speed
            stepper_Left_.move(-1 * defaultSteps); ////set distance - negative value flips the direction
            stepper_Right.setMaxSpeed(defaultSpeed); //set speed
            stepper_Right.move(defaultSteps); //set distance
        }

        //START - CLOSE
        if (receivedCommand == 'f') //CLOSING - Rotates the motor in the opposite direction as opening
        {
            //example c 2000 500 - 2000 steps (5 revolution with 400 step/rev microstepping) and 500 steps/s speed; will rotate in the other direction
            runallowed = true; //allow running
            //Serial.print(receivedMMdistance);  //print the values for checking
            //Serial.print(receivedDelay);
            stepper_Left_.move(defaultSteps / 6); ////set distance - negative value flips the direction
            //stepper_Right.setMaxSpeed(receivedDelay); //set speed
            stepper_Right.move(-1 * defaultSteps / 6); //set distance


        }

        //STOP - STOP
        if (receivedCommand == ' ') //immediately stops the motor
        {
            runallowed = false; //disable running

            stepper_Left_.setCurrentPosition(0); // reset position
            Serial.println("STOP "); //print action
            stepper_Left_.stop(); //stop motor
            stepper_Left_.disableOutputs(); //disable power
            stepper_Right.stop(); //stop motor
            stepper_Right.disableOutputs(); //disable power


        }

        //SET ACCELERATION
        if (receivedCommand == 'r') //Setting up a new acceleration value
        {
            runallowed = false; //we still keep running disabled, since we just update a variable

            receivedAcceleration = Serial.parseFloat(); //receive the acceleration from serial

            stepper_Left_.setAcceleration(receivedAcceleration); //update the value of the variable
            stepper_Right.setAcceleration(receivedAcceleration); //update the value of the variable

            Serial.println("ACC Updated "); //confirm update by message

        }

    }
    //after we went through the above tasks, newData becomes false again, so we are ready to receive new commands again.
    newData = false;


}