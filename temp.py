#!/usr/bin/python

import os

path = '/sys/bus/w1/devices'
fl = os.listdir(path)
for item in fl:
    if '28-' in item:
        ok = 1
        break
    else:
        ok = 0
while ok:
    for item in fl:
        if '28-' in item:
            f = '{0}/{1}/w1_slave'.format(path, item)
            try:
                fi = open(f, 'r')
            except OSError as e:
                print e.strerror
            except:
                print "some other error"
            lines = fi.readlines()
            fi.close()
            for thing in lines:
                if 't=' in thing:
                    temp = int(thing.rstrip("\n").split('=')[1])
                    print"C:{0}".format(temp*.001) #Celcius
                    print"F:{0}\n".format((temp*.001)*1.8+32) #Fahrenhiet
