import time
import serial
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output log file name')
parser.add_argument('--port', help='address of serial port to read')
args = parser.parse_args()
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
            time.sleep(1)
