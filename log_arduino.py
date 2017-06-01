from __future__ import print_function
import time
import serial
import argparse
import os.path
import sys
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output log file name')
parser.add_argument('--port', help='address of serial port to read')
parser.add_argument('-f', '--force', action='store_true', help='overwrite existing log file')
args = parser.parse_args()
if os.path.isfile(args.output) and not args.force:
    print("Warning: file already exists. Run with -f to overwrite!")
    sys.exit(0)
fileout = open(args.output,'w')
with serial.Serial(args.port, timeout=1) as s:
    while True:
        output = s.readline()
        if len(output) > 0:
            fileout.write(str(datetime.datetime.now()) + ' ' + output)
            print(datetime.datetime.now(), output, end='')
        
