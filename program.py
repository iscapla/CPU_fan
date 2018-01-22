#!/usr/bin/env python3
from __future__ import division
import os
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO
import random
import configparser

Config = configparser.ConfigParser()
Config.read("/home/pi/Programs/config.ini")
section = "Fan"
if not Config:
    pin = 19
    waitTime_sec = 5
    avg_list_num = 4
    minTMP = 46 # The temperature where the fan will has the minimum speed.
    maxTMP = 48 # The temperature where the fan will has the maximum speed.
else:
    pin = int(Config.get(section,"pin"))
    waitTime_sec = int(Config.get(section,"waitTime_sec"))
    avg_list_num = int(Config.get(section,"avg_list_num"))
    # The temperature where the fan will has the minimum speed.
    minTMP = float(Config.get(section,"minTMP"))
    # The temperature where the fan will has the maximum speed.
    maxTMP = float(Config.get(section,"maxTMP"))


global temp_list
temp_list = []

verbose=True

global pwm_pin
pwm_pin = None
pwm_speeds = [0,25,50,75,100]
freq= 4 #in Hz

# Do not change this values. They are used to implement the appropiate speed.
global allocate_const
allocate_const = None


def setup():
    global allocate_const
    allocate_const = (maxTMP-minTMP)/(len(pwm_speeds)-2)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    global pwm_pin
    pwm_pin = GPIO.PWM(pin, freq)
    pwm_pin.start(0)

    global temp_list
    for i in range(avg_list_num):
        temp_list.append(getCPUtemperature())

    return()

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    #print(“temp is {0}”.format(temp)) #Uncomment here for testing
    return float(temp)

def fanPWM(temp):
#    temp = round(random.uniform(minTMP-1, maxTMP+1), 2)

    global temp_list
    temp_list.append(temp)
    temp_list.pop(0)
    temp_avg = round(sum(temp_list) / len(temp_list),2)


    if (temp_avg <= minTMP):
        setSpeed = pwm_speeds[0]
    elif (temp_avg >= maxTMP):
        setSpeed = pwm_speeds[-1]
    else:
        aux_temp = temp_avg - minTMP
        global allocate_const
        setSpeed = pwm_speeds[(int)(aux_temp/allocate_const) + 1]

    global pwm_pin
    pwm_pin.ChangeDutyCycle(setSpeed)
    
    if verbose==True:
        print("Current: ", temp, "\tAvg: ", temp_avg, "\tSpeed(%): ", setSpeed)
    return()

def getTEMP():
    CPU_temp = float(getCPUtemperature())
    fanPWM(CPU_temp)
    return()


def main():
    try:
        setup() 
        while True:
            getTEMP()
            sleep(waitTime_sec) # Read the temperature every 5 sec, increase or decrease this limit if you want
    except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt 
        print("Stoping CPU cooler controler.")
        global pwm_pin
        pwm_pin.stop()
        GPIO.cleanup() # resets all GPIO ports used by this program
        

if __name__ == "__main__":
    main()
