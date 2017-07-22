from __future__ import print_function
import time
import serial
import argparse
import os.path
import sys
import datetime

def main(outfile, port, force):
    if os.path.isfile(outfile) and not force:
        print("Warning: file already exists. Run with -f or force=True to overwrite!")
        return 1
    print(' -- START -- ')
    print('time                       usec  cm  ')
    fileout = open(outfile,'w')
    with serial.Serial(port, timeout=1) as s:
        while True:
            try:
                output = s.readline()
                time = str(datetime.datetime.now())
                if len(output) > 0:
                    fileout.write(time + ' ' + output)
                    print(time, output, end='')
            except KeyboardInterrupt:
                break
    print(' -- END -- ')
    fileout.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='Output log file name')
    parser.add_argument('--port', help='address of serial port to read')
    parser.add_argument('-f', '--force', action='store_true', help='overwrite existing log file')
    args = parser.parse_args()
    main(args.output, args.port, args.force)

