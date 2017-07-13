import visa


class DewPointMirror473(object):

    def __init__(self):
        rm = visa.ResourceManager()
        print(rm.list_resources())
        self.instrument = rm.open_resource('ASRL25',
                                           baud_rate=9600,
                                           write_termination='\r',
                                           read_termination='\r\n')
        self.instrument.open()

    def close(self):
        self.instrument.close()

    def readDewPoint(self):
        return self.instrument.query('DP?')

    def readFrostPoint(self):
        return self.instrument.query('FP?')

    def readRelitiveHumidity(self):
        return self.instrument.query('RH?')

    def readHeadPressure(self):
        return self.instrument.query('P?')

    def readTempreatureExternal(self):
        return self.instrument.query('Tx?')

    def readTempreatureMirror(self):
        return self.instrument.query('Tm?')

    def readTempreatureHead(self):
        return self.instrument.query('Tx?')

    def readRequiredData(self):
        data = []
        data.append(self.readDewPoint())
        data.append(self.readFrostPoint())
        data.append(self.readRelitiveHumidity())
        data.append(self.readHeadPressure())
        data.append(self.readTempreatureExternal())
        data.append(self.readTempreatureMirror())
        data.append(self.readTempreatureHead())
        return data

    def readAllData(self):
        data = []
        data.append(self.instrument.query('DP?'))
        data.append(self.instrument.query('FP?'))
        data.append(self.instrument.query('RH?'))
        data.append(self.instrument.query('RHw?'))
        data.append(self.instrument.query('PPMv?'))
        data.append(self.instrument.query('PPMw?'))
        data.append(self.instrument.query('AH?'))
        data.append(self.instrument.query('SH?'))
        data.append(self.instrument.query('VP?'))
        data.append(self.instrument.query('P?'))
        data.append(self.instrument.query('Tx?'))
        data.append(self.instrument.query('Tm?'))
        data.append(self.instrument.query('Th?'))
        data.append(self.instrument.query('Om?'))
        data.append(self.instrument.query('Ox?'))
        return data

    def log(self):
        return self.readRequiredData()

    def logHeader(self):
        return 'DP,FO,RH,HP,Tx,Tm,Th'.split(',')


def main():
    dpm473 = DewPointMirror473()

    print(dpm473.readRelitiveHumidity())

    dpm473.close()

if __name__ == '__main__':
    main()
