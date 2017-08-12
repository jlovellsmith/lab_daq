import visa


class TS2_RHS373LX(object):

    def __init__(self):
        rm = visa.ResourceManager()
        print(rm.list_resources())
        self.instrument = rm.open_resource('ASRL6',
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
        return 'DP_TS2,FP_TS2,Tm_TS2,Vp_TS2,p_TS2 head,Q_TS2,Tp_TS2 precooler,Th_TS2 head,Stable_TS2'.split(',')


def main():
    TS2_373 = TS2_RHS373LX()
    print(TS2_373.logHeader())
    # print(TS2_373.readDewPoint())
    # print(TS2_373.instrument.query('FP?'))
    print(TS2_373.readData())

    TS2_373.close()

if __name__ == '__main__':
    main()
