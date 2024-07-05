import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, in1, in2, in3, in4):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        
        self.setup_pins()

        # Define step sequence
        self.step_sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
# setup pins
    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

  # Rotate the stepper motoe in speified no of steps
    def rotate_stepper(self, steps, delay=0.01):
        for _ in range(steps):
            for step in self.step_sequence:
                GPIO.output(self.IN1, step[0])
                GPIO.output(self.IN2, step[1])
                GPIO.output(self.IN3, step[2])
                GPIO.output(self.IN4, step[3])
                time.sleep(delay)
# stops the motor 
    def stop_motor(self):
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 0)

    def cleanup(self):
        GPIO.cleanup()

if __name__ == '__main__':
    motor = StepperMotor(in1=17, in2=18, in3=27, in4=22)
    try:
        motor.rotate_stepper(512)  # Rotate 512 steps
        motor.stop_motor()  # Stop the motor
    finally:
        motor.cleanup()

