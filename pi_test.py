#!/usr/bin/python

import RPi.GPIO as gpio
import smtplib
import time
from datetime import datetime

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(25, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(22, gpio.OUT)

gpio.output(25, 0)
gpio.output(23, 0)
gpio.output(22, 0)

print gpio.input(22)
print gpio.input(23)
print gpio.input(25)
