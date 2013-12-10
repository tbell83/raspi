#!/usr/bin/python

import os
import gspread
import logging
import sys
from datetime import datetime

logging.basicConfig(filename='/var/log/temp.log', level=logging.INFO)
path = '/sys/bus/w1/devices'
login = 'tbell@tombellnj.com'
passwd = '&lu4ri$m'
metric_name = 'temp_data'


def get_files():
    try:
        file_list = os.listdir(path)
    except:
        logging.info('No Such Directory')
        sys.exit(1)
    for item in file_list:
        if '28-' in item:
            return file_list
    logging.info('No Probe Data')
    sys.exit(1)


def publish(timestamp, metric_name, metric_value):
    gdrive = gspread.login(login, passwd)
    sheet = gdrive.open(metric_name).sheet1
    lista = [timestamp, metric_value]
    logging.info('Pushing %s : %d' % (timestamp, metric_value))
    sheet.append_row(lista)


def get_temp(probe):
    with open(probe) as file:
        for item in file:
            if 't=' in item:
                temp = int(item.rstrip("\n").split('=')[1])*.001
                return temp
        logging.info('No Temperature Data')
        sys.exit(1)

probe_files = get_files()

for item in probe_files:
    if '28-' in item:
        log = '{0}/{1}/w1_slave'.format(path, item)
        try:
            logging.info('Getting Temp')
            temp = get_temp(log)
        except:
            logging.error("Couldn't get Temp")
        time = datetime.now()
        publish(time, metric_name, temp)
