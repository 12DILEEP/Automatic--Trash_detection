# Create Object Detection Datasets with Raspberry Pi and labelImg
## Introduction
In the [previous tutorial](https://gpiocc.github.io/learn/raspberrypi/ml/2020/04/18/martin-ku-using-raspberry-pi-and-tensorflow-lite-for-object-detection.html), we use TensorFlow Lite and pre-trained models to perform object detection on Raspberry Pi. Wouldn’t it be nice if we can train our own object detection models? While we don’t have something like the [Teachable Machine](https://teachablemachine.withgoogle.com/train) for object detection, we still can train custom object detection models relatively easily with the new [TensorFlow Lite Model Maker](https://www.tensorflow.org/lite/models/modify/model_maker/object_detection).
![img1](https://github.com/12DILEEP/Automatic--Trash_detection/assets/90190565/90d20f6a-05e6-42df-b018-0a9982958545)

Just like [what we did for image classification](https://gpiocc.github.io/learn/raspberrypi/ml/2020/06/20/martin-ku-custom-tensorflow-image-classification-with-teachable-machine.html), the first step of training a custom object detection model is to create a labelled dataset. However, taking and handling hundreds (or even thousands) of photos can be time-consuming. To speed up the workflow, we will take a few videos first, and then extract the photos from the videos. Specifically, we will:

* capture videos with the Raspberry Pi camera
* use ffmpeg to turn video frames into images
* separate image files for training and testing
* annotate images with labelImg
We can do all of the above on a Raspberry Pi. Let’s get started.

# Capture Videos with the Raspberry Pi Camera
Connect the camera module to the Raspberry Pi and enable it if you have not done so (see [this tutorial for the instructions](https://gpiocc.github.io/learn/raspberrypi/ml/2020/04/18/martin-ku-using-raspberry-pi-and-tensorflow-lite-for-object-detection.html). Once the camera is ready, we can use the `raspivid` command to capture videos. For example, the following command will record a video of size 640 x 480 at 25 FPS for 10 seconds.

`pi@raspberrypi:~ $ raspivid -o video1.h264 -t 10000 -w 640 -h 480 -fps 25`
![image](https://github.com/12DILEEP/Automatic--Trash_detection/assets/90190565/6705e808-1c01-4d23-b3be-957dcc220ad2)
The video is stored in the `video1.h264` file. You should take a few more videos with the objects you want to detect to create a much more representative dataset for training a better model.
`Note: The Pi captures video as a raw H264 video stream. The VLC player can play it but other media players may not, or play it at an incorrect speed. Check out the [Raspberry Pi official documentation](https://www.raspberrypi.com/documentation/accessories/camera.html#raspivid) if you want to know more about this.`




