'''
Manage the data coming out of the level sensor.

'''
import time

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
        timestamp = int(time.time())
        self.timestamps.append(timestamp)
        if type(serial_readline) == bytes:
            serial_readline = serial_readline.decode()
        parsed_output = serial_readline.split(' ')
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
            return
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

    def get_last_record_str(self):
        return self.get_record_str(self.size-1)
