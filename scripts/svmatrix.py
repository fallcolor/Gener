#! python2

class SglValMap(object):
    def __init__(self, signal, value, datatype, info2 = '', info1 = ''):
        self._signal = signal
        self._value  = value
        self._info1  = info1
        self._info2  = info2
        if datatype:
            self._type = datatype
        else:
            self._type = 'bool_T'

class SvMatrix(object):
    """docstring for SvMatrix"""
    def __init__(self):
        self._list = []

    def addMap(self, signal, value, datatype):
        self._list.append(SglValMap(signal, value, datatype))        

    def isHaveSignal(self, signal):
        for sv in self._list:
            if signal == sv._signal:
                return True

    def getSignalInfo(self, signal):
        for sv in self._list:
            if signal == sv._signal:
                return True, sv._value, sv._type
        return False, None, None
    def GetSignals(self, signal):
        relist = []
        for sv in self._list:
            if signal == sv._signal:
                relist.append([sv._value, sv._type])
        return relist