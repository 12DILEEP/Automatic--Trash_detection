"""To run the main file the command to excute is python main.py --modeldir ssd_mobilenet_v2_coco/saved_model --graph detect.tflite --labels labelmap.txt --threshold 0.5 --resolution 1280x720 --edgetpu
 """

from object_detection import ObjectDetection
from stepper_rotation import StepperMotor
import time

# Initialize the object detection and stepper motor
object_detection = ObjectDetection(modeldir='ssd_mobilenet_v2_coco/saved_model')
stepper_motor = StepperMotor(in1=17, in2=18, in3=27, in4=22)

try:
    while True:
        scores, classes = object_detection.detect_objects()

        # Check if any detection is above 90% confidence
        if scores is not None and any(score > 0.8 for score in scores):
            print("Object detected with high confidence. Stopping motor.")
            break

        # Rotate the stepper motor
        stepper_motor.rotate_stepper(1)
        time.sleep(0.1)  # Adding a small delay to control the motor speed

finally:
    object_detection.release()
    stepper_motor.cleanup()
