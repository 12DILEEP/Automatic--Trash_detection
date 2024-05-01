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
 Note: The Pi captures video as a raw H264 video stream. The VLC player can play it but other media players may not, or play it at an incorrect speed. Check out the [Raspberry Pi official documentation](https://www.raspberrypi.com/documentation/accessories/camera.html#raspivid) if you want to know more about this.

 ### Use ffmpeg to Turn Video Frames into Images
 Once we have recorded a few videos, we can extract the images from the videos with the `ffmpeg` program.
 Firstly, let’s create a new folder `raw_images` for storing the extracted images.

 > pi@raspberrypi:~ $ mkdir raw_images

 Then, we extract the images by using the `ffmpeg` command.
 
 > pi@raspberrypi:~ $ ffmpeg -i video1.h264 -vf fps=25 raw_images/video1_img%03d.jpg
 Do the same for the rest of the videos.
 ### Use Python to Create Training, Validating and Testing Datasets
 If a model memorizes the training data, it will perform extremely well during training but very poorly when non-training data are fed to the model. This problem is known as **overfitting**. A simple, effective way to prevent this problem is using **cross validation**. When training the model, we do not use the entire set of data. The data that have not been used during training are used for checking whether the model can generalize well. Generally, we can divide a dataset into the following three subsets:
- **Training** dataset: for training the model
- **Validation** dataset: for checking the model’s performance during after each iteration (epoch) of training
- **Testing** dataset: for evaluating the model’s performance after the training
We will use Python to help us randomly separate the images into 3 sets. We use 80% of the images for training, 10% of the images for validating and 10% of the image for testing.

First, we import a few Python modules.

> import os

> import pathlib

> import shutil
> import random
> 
 Next, we define a few variables for the paths of the folders that we are working on.

>working_dir = pathlib.Path.home() # the home director

>src_dir = os.path.join(working_dir, 'raw_images') # ~/raw_images

>src_dir = pathlib.Path(src_dir) # convert the path into a Path object

>data_dir = os.path.join(working_dir, 'data')

The data folder in the home directory will be used to store the images and the annotations later.

Then, we create the folders for storing the images and the annotations.
>folders = ["training", "validation", "testing"]
>dirs = [os.path.join(data_dir, f) for f in folders]
>img_dirs = [os.path.join(d, "images") for d in dirs]
>annotation_dirs = [os.path.join(d, "annotations") for d in dirs]

>pathlib.Path(data_dir).mkdir(exist_ok=True)

>for d in dirs + img_dirs + annotation_dirs:
    pathlib.Path(d).mkdir(exist_ok=True)

Inside the `data` folder, we create three folders `training`, `validation` and `testing`. In each of these folders, we create two folders `images` and `annotations`

Next, we get the list of files inside the raw_images folder and count the number of images.

>[]image_files = list(src_dir.glob("*.jpg"))
num_of_images = len(image_files)
print(f"Num of images: {num_of_images}")


 
 
 
 

 




