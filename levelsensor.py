# coding: utf-8
'''
Manage the data coming out of the level sensor.

'''
import datetime
import h5py
import numpy as np

class LevelSensor(object):
    def __init__(self):
        self.timestamps = []
        self.time_reads = []
        self.time_errors = []
        self.position_reads = []
        self.position_errors = []
        self.size = 0

    def check_integrity(self):
        if len(self.timestamps) != self.size:
            return False
        if len(self.time_reads) != self.size:
            return False
        if len(self.time_errors) != self.size:
            return False
        if len(self.position_reads) != self.size:
            return False
        if len(self.position_errors) != self.size:
            return False
        return True

    def record(self, serial_readline):
        timestamp = datetime.datetime.now().timestamp()
        self.timestamps.append(timestamp)
        if type(serial_readline) == bytes:
            serial_readline = serial_readline.decode()
        parsed_output = serial_readline.split(' ')
        if len(parsed_output) != 4:
            print(parsed_output)
            return False
        time_read = parsed_output[0]
        time_error = parsed_output[1]
        position_read = parsed_output[2]
        position_error = parsed_output[3]
        self.time_reads.append(time_read)
        self.time_errors.append(time_error)
        self.position_reads.append(position_read)
        self.position_errors.append(position_error)
        self.size += 1
        if self.check_integrity():
            return True
        else:
            raise ValueError("Data arrays out of sync!")

    def get_record(self, index):
        if index >= self.size:
            raise ValueError("Index too big!")
        return (self.timestamps[index],
                self.time_reads[index],
                self.time_errors[index],
                self.position_reads[index],
                self.position_errors[index])

    def get_record_str(self, index):
        record = self.get_record(index)
        formatted_string = ("Timestamp: {0[0]}, Risetime: {0[1]}±{0[2]}, " +
                "Level: {0[3]}±{0[4]}").format(record)
        return formatted_string

    def get_record_csv(self, index):
        record = self.get_record(index)
        return ','.join(map(str,record))

    def get_last_record_csv(self):
        return self.get_record_csv(self.size-1)

    def get_last_record_str(self):
        return self.get_record_str(self.size-1)

    def get_records(self):
        records = np.empty((self.size, 5), dtype=float)
        records[:,0] = self.timestamps
        records[:,1] = self.time_reads
        records[:,2] = self.time_errors
        records[:,3] = self.position_reads
        records[:,4] = self.position_errors
        return records

    def h5write(self, filename):
        fout = h5py.File(filename, 'w')
        dset = fout.create_dataset('measurements', data=self.get_records())
        dset.attrs['description'] = ("column 0: timestamp; 1: time " +
                "reads [us]; 2: time errors; 3: position[cm]; 4: " +
                "position error")
        fout.close()
