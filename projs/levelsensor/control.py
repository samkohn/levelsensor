from subprocess import call
from datetime import datetime
import os
import sys
sys.path.append(os.environ.get('LS_DIR'))
import log_arduino

def log(message, flag='Info'):
    '''
    Helper to print messages with nice format
    '''
    time = str(datetime.now())
    printString = time + ' ' + flag + ': ' + message
    print printString
    return printString

def pwd():
    '''
    Helper to check current directory
    '''
    cwd = os.getcwd()
    log(cwd)
    return cwd

class cd:
    """
    Context manager for changing the current working directory
    """
    def __init__(self, newPath):
        self.newPath = newPath
        
    def __enter__(self):
        self.savedPath = os.getcwd()
        try: 
            os.chdir(self.newPath)
        except Exception as e:
            log('No directory specified - ' + e, 'Error')
        
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def find_and_replace(inputPath, outputPath, strToFind, strToReplace):
    '''
    Copies file at inputPath to file at outputPath with strToFind replaced by strToReplace
    '''
    with open(inputPath) as inputFile, open(outputPath, 'w') as outputFile:
        for line in inputFile:
            line = line.replace(strToFind, strToReplace)
            outputFile.write(line)
    return

def clean():
    '''
    Fresh plate for compiling
    '''
    with cd(os.environ.get('LS_DIR')):
        # Set CALIBRATION_MODE bit in arduino code
        try:
            if not call(['make','clean']) is 0:
                log('There was an error', 'Error')
                return
            os.remove('levelsensor.ino')
        except Exception as e:
            log('There was this error - ' + str(e), 'Error')
            return
    log('Done!')

def calibrate():
    '''
    Compiles, uploads, and runs arduino in calibration mode
    '''
    with cd(os.environ.get('LS_DIR')):
        # Set CALIBRATION_MODE bit in arduino code
        log('Setting CALIBRATION_MODE bit...')
        try: 
            find_and_replace('levelsensor.template', 'levelsensor.ino', '$CALIBRATION_BIT', '1')
        except Exception as e:
            log('Could not set bit! - ' + str(e), 'Error')
            return

        # Recompile and upload
        log('Uploading to arduino...')
        try:            
            if not call(['make','upload']) is 0:
                log('Could not compile or upload.', 'Error')
                return
        except Exception as e:
            log('Could not compile and upload - '+ str(e), 'Error')
            return

def run():
    '''
    Compiles, uploads, and runs arduino in standard running mode
    '''
    with cd(os.environ.get('LS_DIR')):
        # Set CALIBRATION_MODE bit in arduino code
        log('Setting CALIBRATION_MODE bit...')
        try:           
            find_and_replace('levelsensor.template', 'levelsensor.ino', '$CALIBRATION_BIT', '0')
        except Exception as e:
            log('Could not set bit! - ' + str(e), 'Error')
            return

        # Recompile and upload
        log('Uploading to arduino...')
        try:
            if not call(['make','upload']) is 0:
                log('Could not compile or upload.', 'Error')
                return
        except Exception as e:
            log('Could not compile and upload - '+ str(e), 'Error')
            return

def begin_run(outfile='datalog_0000.txt', force=False):
    '''
    Runs arduino in standard mode and records data to a .txt file
    force=True will overwrite datafile
    '''
    log('Starting run...')
    log('Output to ' + outfile)
    if os.path.isfile(outfile) and not force:
        log('File already exists, run with option force=True to overwrite','Warning')
        return

    run()

    port = os.environ.get('MONITOR_PORT')
    if port is None:
        log('Environment variables not set correctly', 'Error')
        return
    log('Begin run, use CTRL C to end run')
    log_arduino.main(outfile, port, force)

def main():
    if sys.flags.interactive:
        log('''\n
Begin levelsensor session!
User functions: clean(), run(), begin_run(<outputPath>), calibrate()
''')
    else:
        log('''\n
levelsensor control:
Use python -i control.py to enter interactive session
''')

if __name__ == '__main__':
    main()
