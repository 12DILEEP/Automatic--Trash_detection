## Create Object Detection Datasets with Raspberry Pi and labelImg
# Introduction
In the [previous tutorial](https://gpiocc.github.io/learn/raspberrypi/ml/2020/04/18/martin-ku-using-raspberry-pi-and-tensorflow-lite-for-object-detection.html), we use TensorFlow Lite and pre-trained models to perform object detection on Raspberry Pi. Wouldn’t it be nice if we can train our own object detection models? While we don’t have something like the [Teachable Machine](https://teachablemachine.withgoogle.com/train) for object detection, we still can train custom object detection models relatively easily with the new [TensorFlow Lite Model Maker](https://www.tensorflow.org/lite/models/modify/model_maker/object_detection).
![img1](https://github.com/12DILEEP/Automatic--Trash_detection/assets/90190565/90d20f6a-05e6-42df-b018-0a9982958545)

Just like [what we did for image classification](https://gpiocc.github.io/learn/raspberrypi/ml/2020/06/20/martin-ku-custom-tensorflow-image-classification-with-teachable-machine.html), the first step of training a custom object detection model is to create a labelled dataset. However, taking and handling hundreds (or even thousands) of photos can be time-consuming. To speed up the workflow, we will take a few videos first, and then extract the photos from the videos. Specifically, we will:

=>capture videos with the Raspberry Pi camera
=>use ffmpeg to turn video frames into images
=>separate image files for training and testing
=>annotate images with labelImg
We can do all of the above on a Raspberry Pi. Let’s get started.

# Capture Videos with the Raspberry Pi Camera
Connect the camera module to the Raspberry Pi and enable it if you have not done so (see [this tutorial for the instructions](https://gpiocc.github.io/learn/raspberrypi/ml/2020/04/18/martin-ku-using-raspberry-pi-and-tensorflow-lite-for-object-detection.html). Once the camera is ready, we can use the "highlightwords.raspivid": {
    "default": 0
}raspivid command to capture videos. For example, the following command will record a video of size 640 x 480 at 25 FPS for 10 seconds.

