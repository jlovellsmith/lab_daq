import visa


class TS1_MBW373LX(object):

    def __init__(self):
        rm = visa.ResourceManager()
        print(rm.list_resources())
        self.instrument = rm.open_resource('ASRL4',
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

    def readT_Mirror(self):
        return self.instrument.query('Tm?')

    def readT_Head(self):
        return self.instrument.query('Tx?')



    def readData(self):
        data = []
        data.append(self.instrument.query('DP?'))
        data.append(self.instrument.query('FP?'))
        data.append(self.instrument.query('Tm?'))
        data.append(self.instrument.query('VP?'))
        data.append(self.instrument.query('P?'))
        data.append(self.instrument.query('Flow?'))
        data.append(self.instrument.query('Tp?'))
        data.append(self.instrument.query('Th?'))
        data.append(self.instrument.query('Stable?'))
        return data

    def log(self):
        return self.readData()

    def logHeader(self):
        return 'DP_TS1,FP_TS1,Tm_TS1,Vp_TS1,p_TS1 head,Q_TS1,Tp_TS1 precooler,Th_TS1 head,Stable_TS1'.split(',')


def main():
    TS1_373 = TS1_MBW373LX()
    print(TS1_373.logHeader())
    # print(TS1_373.readDewPoint())
    # print(TS1_373.instrument.query('FP?'))
    print(TS1_373.readData())

    TS1_373.close()

if __name__ == '__main__':
    main()
