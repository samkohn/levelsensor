'''
A simple utility that plots level vs. time for the standard h5 (or csv)
level sensor output files.

'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('infile', help='The .h5 or .csv input file to plot')
parser.add_argument('-i', '--interactive', action='store_true',
        help='interactive plotting')
parser.add_argument('-o', '--output', default=None, help='output file')
args = parser.parse_args()

import h5py
import csv
import numpy as np
import matplotlib

if args.interactive:
    pass
else:
    matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mpldates
import os
import datetime

from autodateminorlocator import AutoDateMinorLocator

infilename = args.infile
basename, extension = os.path.splitext(infilename)
if args.output:
    outfilename = args.output
else:
    outfilename = basename + '.pdf'
if extension == '.h5':
    with h5py.File(infilename, 'r') as infile:
        data = infile['measurements'][:]
elif extension == '.csv':
    with open(infilename, 'r') as infile:
        reader = csv.reader(infile)
        firstrow = next(reader)
        data = []
        for row in reader:
            data.append(list(map(float,row)))
        data = np.array(data, dtype=float)
        print(data.shape)
else:
    raise ValueError("Invalid file extension. Must be .h5 or .csv")

timestamps = data[:,0]
risetimes = data[:,1]
risetimes_err = data[:,2]
positions = data[:,3]
positions_err = data[:,4]

fig, ax1 = plt.subplots()
locator = mpldates.AutoDateLocator();
formatter = mpldates.AutoDateFormatter(locator)
formatter.scaled[1/(24*60.)] = '%H:%M'
ax1.xaxis.set_major_formatter(formatter)
ax1.xaxis.set_major_locator(locator)
ax1.xaxis.set_minor_locator(AutoDateMinorLocator())
ax2 = ax1.twinx()

xvalues = list(map(datetime.datetime.fromtimestamp, timestamps))
ax2.plot(xvalues, risetimes)
ax1.plot(xvalues, positions, 'w')
ax1.set_ylabel(r'Liquid level [cm]')
ax2.set_ylabel(r'$RC$ Rise Time [$\mu$s]')
ax1.set_xlabel('Clock time')
#fig.tight_layout()
if args.interactive:
    plt.show()
else:
    plt.savefig(outfilename)
