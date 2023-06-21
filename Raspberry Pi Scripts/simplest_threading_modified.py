#!/usr/bin/env python

import threading
from random import randint
import smbus
import time
import datetime
import os
import serial

# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number. Optional parameter 'decimals'
    # will round to specified number of decimal places.
    result=(data[1] + (256 * data[0])) / 1.2
    return (result)

def readLight(addr=DEVICE):
    # Read data from I2C interface
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

#Code given above is for light sensor

#Duration of the program
DURATION = 15

#Sleep time of threads (light sensor thread)
SLEEP_TIME = 3

#USB drive name
USB_LABEL_NAME = 'RAVINDU'


#Captures the GPS from the GPS sensor
def capture_gps():
    #Write the data in the ttyACM0 port to the GPSLog.txt file in each second. Data is supplied by the arduino. Initialization of serial port in python.
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    
    #Calculation of end time
    t_end = time.time()+DURATION
    
    #Creates the file GPSLog.txt in pendrive
    f=open("/media/pi/" + USB_LABEL_NAME + "/Data/GPSLog.txt","w+")
    
    #While the duration is not over, every data in serial port will be written to the text file
    while time.time()< t_end:
        x=ser.readline()
        f.write(x)
        print(x)
        
    #Close the text file
    f.close()        

def capture_photo():
    #Captures the photos from cameras using raspstill. command => raspstill <Duration> <Interval> -o <location>
    os.system("raspistill -t " + str((DURATION - SLEEP_TIME) * 1000) + " -tl " + str(SLEEP_TIME * 1000) + " -o /media/pi/" + USB_LABEL_NAME + "/Data/image%04d.jpg")

def detect_light():
    #Sleep the thread for SLEEP_TIME to make it synchronous with photo capture
    time.sleep(SLEEP_TIME)
    
    #Calculation of end time
    t_end = time.time()+DURATION
    
    #Creates the file IntensityLog.txt in pendrive
    f=open("/media/pi/" + USB_LABEL_NAME + "/Data/IntensityLog.txt","w+")
    
    #While the duration is not over, the recorded time and the light level will be written to the text file. 
    while time.time()< t_end:
        lightLevel=readLight()
        recordedTime = time.ctime()
        print(recordedTime + " --Light Level : " + format(lightLevel,'.2f') + " lx")
        f.write(recordedTime + ' ' + format(lightLevel,'.2f') + 'lx\n')
        time.sleep(SLEEP_TIME)

#Create threads
camera_thread = threading.Thread(target=capture_photo)
#light_sensor_thread = threading.Thread(target=detect_light)
gps_thread = threading.Thread(target=capture_gps)

#Start threads
camera_thread.start()
#light_sensor_thread.start()
gps_thread.start()

#Join threads to the deamon thread.
camera_thread.join()
#light_sensor_thread.join()
gps_thread.join()
# Demonstrates that the main process waited for threads to complete
print "Data acqusition complete"
