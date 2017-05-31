import time
import serial
s = serial.Serial('/dev/cu.usbmodem1411', timeout=0)
fileout = open('datalog-height-adjust.txt','w')
while True:
    output = s.readline()
    if len(output) > 0:
        fileout.write(output + '\n')
        print output
    time.sleep(1)
