# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util

class VideoStream:
    """Camera object that controls video streaming from the webcam"""
    def __init__(self, resolution=(640, 480), framerate=30):
        self.stream = cv2.VideoCapture(0)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.stream.set(3, resolution[0])
        self.stream.set(4, resolution[1])
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stream.release()
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

class ObjectDetection:
    def __init__(self, args):
        self.MODEL_NAME = args.modeldir
        self.GRAPH_NAME = args.graph
        self.LABELMAP_NAME = args.labels
        self.min_conf_threshold = float(args.threshold)
        self.resW, self.resH = map(int, args.resolution.split('x'))
        self.use_TPU = args.edgetpu
        
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter
            if self.use_TPU:
                from tflite_runtime.interpreter import load_delegate
        else:
            from tensorflow.lite.python.interpreter import Interpreter
            if self.use_TPU:
                from tensorflow.lite.python.interpreter import load_delegate

        if self.use_TPU:
            if self.GRAPH_NAME == 'detect.tflite':
                self.GRAPH_NAME = 'edgetpu.tflite'
        
        CWD_PATH = os.getcwd()
        PATH_TO_CKPT = os.path.join(CWD_PATH, self.MODEL_NAME, self.GRAPH_NAME)
        PATH_TO_LABELS = os.path.join(CWD_PATH, self.MODEL_NAME, self.LABELMAP_NAME)
        
        with open(PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
        if self.labels[0] == '???':
            del(self.labels[0])
        
        if self.use_TPU:
            self.interpreter = Interpreter(model_path=PATH_TO_CKPT, experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        else:
            self.interpreter = Interpreter(model_path=PATH_TO_CKPT)
        
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)
        self.input_mean = 127.5
        self.input_std = 127.5
        self.outname = self.output_details[0]['name']
        if 'StatefulPartitionedCall' in self.outname:
            self.boxes_idx, self.classes_idx, self.scores_idx = 1, 3, 0
        else:
            self.boxes_idx, self.classes_idx, self.scores_idx = 0, 1, 2

        self.videostream = VideoStream(resolution=(self.resW, self.resH), framerate=30).start()

    def run_detection(self):
        while True:
            frame1 = self.videostream.read()
            frame_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
            input_data = np.expand_dims(frame_resized, axis=0)
            
            if self.floating_model:
                input_data = (np.float32(input_data) - self.input_mean) / self.input_std
            
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            boxes = self.interpreter.get_tensor(self.output_details[self.boxes_idx]['index'])[0]
            classes = self.interpreter.get_tensor(self.output_details[self.classes_idx]['index'])[0]
            scores = self.interpreter.get_tensor(self.output_details[self.scores_idx]['index'])[0]

            for i in range(len(scores)):
                if self.min_conf_threshold < scores[i] <= 1.0:
                    print(f"Detected object {self.labels[int(classes[i])]} with score: {scores[i]}")
            
            if cv2.waitKey(1) == ord('q'):
                break

        self.videostream.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--modeldir', help='Folder the .tflite file is located in', required=True)
    parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite', default='detect.tflite')
    parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt', default='labelmap.txt')
    parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects', default=0.5)
    parser.add_argument('--resolution', help='Desired webcam resolution in WxH', default='1280x720')
    parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection', action='store_true')
    args = parser.parse_args()

    od = ObjectDetection(args)
    od.run_detection()

