#!/usr/bin/python

import os
import gspread
from datetime import datetime

path = '/sys/bus/w1/devices'
login = 'tbell@tombellnj.com'
passwd = '&lu4ri$m'
metric_name = 'temp_data'

def get_files():
    try:
        file_list = os.listdir(path)
    except:
        print "No Such Directory"
        return
    for item in file_list:
        if '28-' in item:
            return file_list
    print "No Probe Data"
    return{}

def publish(timestamp, metric_name, metric_value):
    gdrive = gspread.login(login, passwd)
    sheet = gdrive.open(metric_name).sheet1
    lista = [timestamp, metric_value]
    sheet.append_row(lista)

def get_temp(probe):
    print 'stuff'
    print probe
    with open(probe) as file:
        for item in file:
            print item
            if 't=' in item:
                temp = int(item.rstrip("\n").split('=')[1])*.001
                return temp
        print "No Temperature Data"
        return{}

probe_files = get_files()
print probe_files

for item in probe_files:
    if '28-' in item:
        log = '{0}/{1}/w1_slave'.format(path, item)
        try:
            print 'Getting Temp'
            temp = get_temp(log)
        except:
            print "Couldn't get Temp"
        time = datetime.now()
        publish(time, metric_name, temp)
