import visa
import time
import msvcrt
import csv
import sys


last10 = []

baseHeader = ['DateTime', 'runtime', 'cycle']

profile = "profile.csv"

timeFormat = "%Y-%m-%d %H:%M:%S"
startTime = time.time()


def timeStamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def log(cycle, timeC, interval, instruments, file):
    changeTime = time.time()
    count = 0
    try:
        while int(time.time()) < int(changeTime+timeC):

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
                row.append(cycle)

                for instrument in instruments:
                    row.extend(instrument.log())

                #printout for vaisala only remove if not logging vaisala first
                print ("{}\t{}\t{}\t{}".format(row[1],row[4],row[9],row[5]))

                writer.writerow(row)
                storeLine(row)
            

    except KeyboardInterrupt:
        pass


def storeLine(line):
    global last10
    last10.insert(0, line)
    last10 = last10[:10]


def stablePoints(file):
    newLine = []
    for i in range(1, len(last10[0])):
        data = 0
        for line in last10:
            data = data + float(line[i])
            
        data = data/len(last10)
        newLine.insert(i, data)

    with open(file, 'a') as datafile:
        writer = csv.writer(datafile, delimiter=',', lineterminator='\n')
        writer.writerow(newLine)


def openInstruments(names):
    instrumentDict = {'VaisalaHMT330': VaisalaHMT330,
                'DewPointMirror473': DewPointMirror473}
    instruments = []
    for name in names:
        instrument = instrumentDict[name]()
        instruments.append(instrument)
    return instruments


def VaisalaHMT330():
    from VaisalaHMT330 import VaisalaHMT330
    return VaisalaHMT330()


def DewPointMirror473():
    from DewPointMirror473 import DewPointMirror473
    return DewPointMirror473()


def main():

    with open(profile, 'r') as setup:
        read = csv.reader(setup, delimiter=',')
        filename = next(read)[1]
        filenameAvg = next(read)[1]
        instrumentNames = []
        instrumentNames.extend(next(read)[1:])
        times = next(read)[1:]
        interval = float(next(read)[1])
        cycles = next(read)[1:]

        
    instruments = []
    instruments.extend(openInstruments(instrumentNames))

    dateTime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename = "Data\\"+filename.format(dateTime)
    filenameAvg = "Data\\"+filenameAvg.format(dateTime)
    
    headerInstruments = [None, None, None]
    headerValues = baseHeader

    for name, inst in zip(instrumentNames, instruments):
        while (len(headerInstruments)< len(headerValues)):
               headerInstruments.append(None)
        headerInstruments.insert(len(headerValues), name)
        headerValues.extend(inst.logHeader())

    with open(filenameAvg, 'w') as avgfile:
        avgfile.write('averages file,{}\n'.format(timeStamp()))

    with open(filename, 'w') as datafile:
        writer = csv.writer(datafile, delimiter=',', lineterminator='\n')
        writer.writerow(headerInstruments)
        writer.writerow(headerValues)

    global startTime
    startTime = time.time()

    for cycle, timeC in zip(cycles,times):

       
        
        timeC = (float)(timeC)
        global last10
        last10 = []

        print("logging cycle {}, for {} s"
              .format(cycle, timeC))

        print("time(s)\tRH\tTx\tTd")

        log(cycle=cycle, timeC=timeC, interval=interval,
            instruments=instruments, file=filename)

        stablePoints(filenameAvg)


if __name__ == '__main__':
    main()
