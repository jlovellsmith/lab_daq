import visa
import time
import msvcrt
import csv
import sys

last10 = []

baseHeader = ['DateTime', 'runtime']
infoHeader="Monitoring RS232 from 2x373 and TS3900"
profile = "K6S13_TS1TS2_TS3900_profile.csv"
timeFormat = "%Y-%m-%d %H:%M:%S"
startTime = time.time()



def timeStamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def log(interval, instruments, file):
    """
    once the fileanme is created and file headers written, data is 
    appended to the file at intervals until logger stopped.
        interval: time between successive readings (of HG2 parameters and instruments
        parameters: Temp? , RH? , TempSP? , RHSP? , RHRef? , Desiccant1DP?,
                    Desiccant2DP? , WaterLevel?
        instruments: currently HMT337 and RHS473 are available
        file: filename
    """  
    changeTime = time.time()
    count = 0
    try:
        while 1==1:
            count = count+1
            next = (changeTime+interval*count)-(time.time())

            time.sleep(next)
            
            with open(file, 'a') as datafile:
                writer = csv.writer(datafile, delimiter=',',
                                    lineterminator='\n')
                timeString = timeStamp()
                runtime = int(time.time()-startTime)

                row = [timeString]
                row.append(runtime)

                for instrument in instruments:
                    row.extend(instrument.log())

                writer.writerow(row)
                storeLine(row)
                print(row)
#    return row
            

    except KeyboardInterrupt:
        pass


def storeLine(line):
    global last10
    last10.insert(0, line)
    last10 = last10[:10]

def openInstruments(names):
    instrumentDict = {
                    'TS3900': TS3900,
                    'TS1_MBW373LX': TS1_MBW373LX,
                    'TS2_RHS373LX': TS2_RHS373LX
                    }
    instruments = []
    for name in names:
        name=name.strip()
        instrument = instrumentDict[name]()
        instruments.append(instrument)
    return instruments

def TS3900():
    '''
    Import TS3900
    '''
    from TS3900 import TS3900
    return TS3900()

def TS1_MBW373LX():
    '''
    Import TS1_MBW373LX
    '''
    from TS1_MBW373LX import TS1_MBW373LX
    return TS1_MBW373LX()

def TS2_RHS373LX():
    '''
    Import TS2_MBW373LX
    '''
    from TS2_RHS373LX import TS2_RHS373LX
    return TS2_RHS373LX()


def main():

    # read profile and setup variables
    with open(profile, 'r') as setup:
        read = csv.reader(setup, delimiter=',')
        filename = next(read)[1]
        filenameAvg = next(read)[1]
        instrumentNames = []
        instrumentNames.extend(next(read)[1:])
#        times = next(read)[1:]
        interval = float(next(read)[1])
        baseHeader = ['DateTime', 'runtime']

    # setup list of instruments    
    instruments = []
    instruments.extend(openInstruments(instrumentNames))

    # setup file names
    dateTime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename = "C:\Data\py_data_K6prep\\"+filename.format(dateTime)
##    filenameAvg = "Data\py_data_K6prep\\"+filenameAvg.format(dateTime)

    #setup file headers
    headerInstruments = [filename, None, None, None]
    headerValues = baseHeader
   
    for name, inst in zip(instrumentNames, instruments):
        headerInstruments.insert(len(headerValues), name)
        headerValues.extend(inst.logHeader())

   # create log files
##     with open(filenameAvg, 'w') as avgfile:
##         avgfile.write('averages file,{}\n'.format(timeStamp()))

    with open(filename, 'w') as datafile:
        writer = csv.writer(datafile, delimiter=',', lineterminator='\n')
        writer.writerow(headerInstruments)
        writer.writerow(headerValues)
        print(headerInstruments)
        print(headerValues)
    # start time
    global startTime
    startTime = time.time()

    # repetitions 
    log(interval=interval,instruments=instruments, file=filename)
        # get avgs
 

if __name__ == '__main__':
    main()
