#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import subprocess

GPIO.setmode(GPIO.BCM)

ir_sense = 4
red_led = 24
speaker = 25
green_led = 22

GPIO.setwarnings(False)
GPIO.setup(ir_sense, GPIO.IN)
GPIO.setup(speaker, GPIO.OUT, initial=0)
GPIO.setup(red_led, GPIO.OUT, initial=0)
GPIO.setup(green_led, GPIO.OUT, initial=0)

def logtime():
    now = time.strftime("%Y_%m_%d-%H%M%S", time.localtime())
    return now

def capture():
    command = "fswebcam -q -d /dev/video0 -r 160x120 /home/pi/{0}.jpeg".format(logtime())
    dump = open(os.devnull, 'w')
    print("{0} Capturing...".format(logtime()))
    subprocess.call(command, shell=True, stdout=dump)
    print("{0} All Done!".format(logtime()))

def make_vid():
    print("{0} Generating GIF...".format(logtime()))
    command = "convert -delay 1 -loop 0 *.jpg {0}.gif".format(logtime())
    dump = open(os.devnull, 'w')
    subprocess.call(command, shell=True, stdout=dump)
    print("{0} All Done!".format(logtime()))
    clean_up()

def clean_up():
    print("{0} Cleaning Up".format(logtime()))
    for item in os.listdir('/home/pi'):
        if item.endswith('.jpg'):
            os.remove(item)
    print('{0} All Done!'.format(logtime()))

def file_count():
    count = os.listdir('/home/pi')
    for item in count:
        if item.endswith('.jpeg'):
            return 1
    return 0

def rename():
    print("{0} Renaming...".format(logtime()))
    i = 0
    files = os.listdir('/home/pi/')
    for item in files:
        if item.endswith('.jpeg'):
            filename = "{0}.jpg".format(i)
            os.rename(item, filename)
            print(filename)
            i += 1
    print("{0} All Done!".format(logtime()))
    make_vid()

def beep():
    GPIO.output(speaker, 1)
    time.sleep(1)
    GPIO.output(speaker, 0)

try:
    while True :
        while GPIO.input(ir_sense)==1:
            status = "{0} - Motion Detected".format(logtime())
            beep()
            print(status)
            capture()
        if file_count():
            rename()
        print("Sleeping")
        time.sleep(1)

except KeyboardInterrupt:
    print "\nQuitting"
    GPIO.cleanup()
