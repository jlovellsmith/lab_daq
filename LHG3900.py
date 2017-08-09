import visa


class LowHumidityGenerator3900(object):
    def __init__(self):
        rm = visa.ResourceManager()
        print(rm.list_resources())
        self.instrument = rm.open_resource('COM7',
                                           baud_rate=2400,
                                           write_termination='\r',
                                           read_termination='\r\n')
        self.instrument.open()

    def close(self):
        self.instrument.close()

    def readActual(self):
        return self.instrument.query('?')

    def readActualDict(self):
        values = self.instrument.query('?')
        values = values.split(',')
        actualHeader = ['Frost Point', 'Dew Point', 'PPMv', 'PPMw',
                        '% Relative Humidity', 'Saturation Pressure',
                        'Saturation Tempreature', 'Test Pressure',
                        'Test Tempreature', 'FlowRate', 'System Status']
        dictionary = dict(zip(actualHeader, values))
        return dictionary

    def readSetpoints(self):
        return self.instrument.query('?SP')

    def setFlowRate(self, flow):
        if flow > 4.5 or flow < 0:
            return "error flow cant be less than 0 or greater than 4.5"
        else:
            self.instrument.query('FL='+str(flow))

    def readActualFlowRate(self):
        return self.instrument.query('?FL')


def main():
    hg = LowHumidityGenerator3900()

    # print(hg.readActual())
    # print(hg.readActualDict())
    print(hg.readSetpoints())
    print(hg.setFlowRate(flow=0.5))
    print(hg.readSetpoints())
    hg.close()

if __name__ == '__main__':
    main()
