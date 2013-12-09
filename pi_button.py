#!/usr/bin/python

import RPi.GPIO as gpio
import smtplib
import time
from datetime import datetime

def send_mail(STATUS, LED):
    if STATUS == 0:
        STATUS = "off"
    elif STATUS == 1:
        STATUS = "on"
    msg = "Someone turned "+STATUS+" "+str(LED)+" at "+str(datetime.now())+"!"
#    server = smtplib.SMTP('smtp.gmail.com:587')
#    server.starttls()
#    server.login("tbell@tombellnj.com", "&lu4ri$m")
#    server.sendmail("pi@tombellnj.com", "9739536588@vtext.com", msg)
    print msg

def beep():
    gpio.output(18, 1)
    time.sleep(.1)
    gpio.output(18, 0) 

def my_callback(channel):
    gpio.output(4, not gpio.input(4))
    beep() 
    send_mail(gpio.input(4), "LED 2")

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(23, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(24, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(18, gpio.OUT)
gpio.setup(4, gpio.OUT)
gpio.setup(25, gpio.OUT)
gpio.output(4, 0)
gpio.output(25, 0)
gpio.output(18, 0)
i = 2

gpio.add_event_detect(24, gpio.FALLING, callback=my_callback)

try:
    while i == 2:
        gpio.wait_for_edge(23, gpio.FALLING)
        gpio.output(25, not gpio.input(25))
        beep()
        send_mail(gpio.input(25), "LED 1")
except KeyboardInterrupt:
    gpio.cleanup()
gpio.cleanup()

