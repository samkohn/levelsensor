import time
import serial
import argparse
import os.path
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output log file name')
parser.add_argument('--port', help='address of serial port to read')
parser.add_argument('-f', '--force', action='store_true', help='overwrite existing log file')
args = parser.parse_args()
if os.path.isfile(args.output) and not args.force:
    print "Warning: file already exists. Run with -f to overwrite!"
    sys.exit(0)
fileout = open(args.output,'w')
while True:
    # Weird serial read issue (duplicated across software)
    # causes us to close and reopen serial port once per minute.
    with serial.Serial(args.port, timeout=0) as s:
        for i in xrange(60):
            output = s.readline()
            if len(output) > 0 and i != 0:
                fileout.write(output)
                print output
            time.sleep(0.5)
