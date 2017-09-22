from __future__ import print_function
import datetime
import serial
import argparse
import os.path
import sys
from levelsensor import LevelSensor

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', required=True, help='Output log file name')
parser.add_argument('--port', help='address of serial port to read')
parser.add_argument('-f', '--force', action='store_true', help='overwrite existing log file')
parser.add_argument('--h5-save-interval', default=60, type=int,
        help='num seconds between hdf5 saves')
args = parser.parse_args()
h5name = os.path.splitext(args.output)[0] + '.h5'
csvname = os.path.splitext(args.output)[0] + '.csv'
if os.path.isfile(args.output) and not args.force:
    print("Warning: file already exists. Run with -f to overwrite!")
    sys.exit(0)
fileout = open(args.output,'w')
csvout = open(csvname,'w')
csvout.write('"timestamp","risetime_us","risetime_err_us","position_cm","position_err_cm"')
sensor = LevelSensor()
with serial.Serial(args.port, timeout=1) as s:
    try:
        t0 = datetime.datetime.now().timestamp()
        while True:
            output = s.readline()
            if len(output) > 0:
                sensor.record(output)
                strtoprint = sensor.get_last_record_str()
                fileout.write(strtoprint)
                csvout.write(sensor.get_last_record_csv())
                print(strtoprint, end='')
            if datetime.datetime.now().timestamp() - t0 > args.h5_save_interval:
                t0 = datetime.datetime.now().timestamp()
                sensor.h5write(h5name)
    except KeyboardInterrupt:
        if sensor.check_integrity():
            sensor.h5write(h5name)
        else:
            print("Lost data integrity since last save.")
            print("Last save was at ", datetime.datetime.fromtimestamp(t0))
            print("Save h5 file even though we've lost data integrity?")
            answer = str(input("[y/N] "))
            # assume "no" if answer is N, n, or only whitespace
            if answer.lower() == 'n' or ''.join(answer.split) == '':
                pass
            else:
                sensor.h5write(h5name)
        sys.exit(0)
