from __future__ import print_function
import time
import serial
import argparse
import os.path
import sys
from levelsensor import LevelSensor

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', required=True, help='Output log file name')
parser.add_argument('--port', help='address of serial port to read')
parser.add_argument('-f', '--force', action='store_true', help='overwrite existing log file')
args = parser.parse_args()
if os.path.isfile(args.output) and not args.force:
    print("Warning: file already exists. Run with -f to overwrite!")
    sys.exit(0)
fileout = open(args.output,'w')
sensor = LevelSensor()
with serial.Serial(args.port, timeout=1) as s:
    try:
        while True:
            output = s.readline()
            if len(output) > 0:
                sensor.record(output)
                strtoprint = sensor.get_last_record_str()
                fileout.write(strtoprint)
                print(strtoprint, end='')
    except KeyboardInterrupt:
        sys.exit(0)
