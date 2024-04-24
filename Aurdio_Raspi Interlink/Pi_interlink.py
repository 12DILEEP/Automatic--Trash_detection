""" 
The below code is used to check whether the serial communication has been established or not between the aurdino & raspberry pi

In raspi check whether the raspi has a permission for serial communication or not by simply typing  groups in terminal of raspi if there is dialout (it means connected to output port)

  if not
    TYPE "sudo adduser pi(username) dialout"

To Know which port it is connected then type command " ls/dev/tty* " 

"""
import serial

import time

ser = serial.serial('/dev/ttyACM0',11520, time.out=1.0) # port path, speed , time to connect
time.sleep(3)    # There will be some time taken by the interlink serial connection

ser.reset_input_buffer()       # erases the data if it sends the data before the code exutes.

print("serial ok")

ser.close()


