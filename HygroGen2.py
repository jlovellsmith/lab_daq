import visa

class HygroGen2(object):
    def __init__(self):
        rm = visa.ResourceManager()
        print(rm.list_resources())
        self.instrument = rm.open_resource("TCPIP::169.254.204.221::INSTR")
        self.instrument.open()

    def close(self):
        self.instrument.close()

    def readTemp(self):
        return self.instrument.query('Temp?')
    def readTempSP(self):
        return self.instrument.query('TempSP?')
    def readRH(self):
        return self.instrument.query('RH?')
    def readRHSP(self):
        return self.instrument.query('RHSP')
    def readParamQ(self,param):
        return self.instrument.query('paramQ')


def main():
    hg = HygroGen2()
    print("hg=")
    print('T',hg.readTemp())
    print('T_sp', hg.readTempSP())
    print('RH', hg.readRH())
    print('RH_sp', hg.readRHSP())

    hg.close()

if __name__ == '__main__':
    main()
