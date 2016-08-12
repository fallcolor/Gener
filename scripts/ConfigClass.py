'''
    config file class:
    class AppConfig()
    class HwConfig()
    class MapConfig()

'''
import json

class AppConfig(object):
    '''
    contain app configuration, with following attributes:
        _version
        _prj: project name
        _var: a list of variable, like [["Bat.BusVolt": "float"],["Bat.BusVolt": "float"]]
    ]
    '''
    def __init__(self, ver = '0.1', prj = ''):
        self._version = ver
        self._prj = prj
        self._vars = []
    def AddVersion(self, ver):
        self._version = ver
    def AddProjectName(self, prj):
        self._prj = prj
    def AddVariable(self, var):
        self._vars.append(var)
    def ImportFromFile(self, infile):
        f = open(infile, 'rb')
        data = json.loads(f.read())
        self._version = data['version']
        self._prj = data['project']
        self._vars = data['var']


class HwConfig(object):
    '''
    contain hardware configuration, with following attributes:
        _version
        _can: option can config, consisting of nodelist, baudrate, sample point
        _DI : contain digital input pin name
        _DO : contain digital output pin name
        _PWM: contain PWM output pin name
        _AI : contain Analog input pin name
    '''
    def __init__(self, ver = '0.1'):
        self._version = ver
        self._can = {}
        self._DI  = []
        self._DO  = []
        self._PWM = []
        self._AI  = []
    def ImportFromFile(self, infile):
        f = open(infile, 'rb')
        data = json.loads(f.read())
        self._can = data['CAN']
        self._DI = data['DI']
        self._DO = data['DO']
        self._PWM = data['PWM']
        self._AI = data['AI']

class MapConfig(object):
    '''
    contain all configuration of project, with following attributes:
        _time: file generate time
        _hwver: from hardware config
        _appver: from app config
        _prj: from app config
        _ecu: reference ecu, from dbc
        _cancfg: custom config of can module
        _msgcfg: config of each message
        _map: map of app variable and either of can signal and controler PIN
    '''
    def __init__(self):
        self._time = ''
        self._hwver = ''
        self._appver = ''
        self._prj = ''
        self._ecu = {}
        self._cancfg = {}
        self._msgcfgs = []
        self._maps = []

    def EditMap(self, num, sgl, st, tt, uniq):
        for mp in self._maps:
            if mp._num == num:
                self._signal = sgl
                self._sgltype = st
                self._transtype = tt
                self._uniq = uniq
                return True
        return False
    def ImportFromFile(self, infile):
        f = open(infile, 'rb')
        data = json.loads(f.read())
        self._time = data['time']
        self._hwver = data['hwver']
        self._appver = data['appver']
        self._prj = data['project']
        self._ecu = data['ecu']
        self._cancfg = data['canconfig']
        for sc in data['msgconfig']:
            self._msgcfgs.append(MessageConfig(sc['ID'], sc['node'], sc['prd'],sc['trans'] \
                , sc['sglfunc'], sc['DLC'], sc['ide'], sc['enable'], sc['checked']))
        # self._msgcfgs = data['msgconfig']
        num = 0
        for mp in data['map']:
            self._maps.append(SignalMap(num, [mp[0], mp[1]], mp[2], mp[3], mp[4], mp[5]))
            num += 1
        # self._maps = data['map']


class MessageConfig(object):
    '''
    '''
    def __init__(self, msgid = '', nd = 0, prd = 100, tran = True, sf = '', dlc = 8, ide = True, en = True, chked = True):
        self._ID = msgid
        self._node = nd
        self._prd = prd
        self._tran = tran
        self._sglfunc = sf
        self._DLC = dlc
        self._IDE = ide
        self._enable = en
        self._checked = chked

class SignalMap(object):
    '''
    '''
    def __init__(self, num, var, sgl = '', st = '', tt = '', uniq = False):
        self._num = num
        self._var = var[0]
        self._type = var[1]
        self._signal = sgl
        self._sgltype = st
        self._transtype = tt
        self._uniq = uniq

def test():
    # ac = AppConfig()
    # ac.ImportFromFile(r'E:\pyproj\gener\test\app.ac')
    # print ac._vars

    # hc = HwConfig()
    # hc.ImportFromFile(r'E:\pyproj\gener\test\kk.hc')
    # print hc._can
    # print hc._DI
    # print hc._DO
    # print hc._PWM
    # print hc._AI

    mc = MapConfig()
    mc.ImportFromFile(r'E:\pyproj\gener\test\kk.sv')
    print mc._ecu
    print mc._cancfg
    for mcmc in mc._msgcfgs:
        print mcmc._ID
        print mcmc._node
        print mcmc._prd
        print mcmc._tran
        print mcmc._sglfunc
        print mcmc._DLC
        print mcmc._IDE
        print mcmc._enable
        print mcmc._checked
    for mp in mc._maps:
        print mp._num
        print mp._var
        print mp._type
        print mp._signal
        print mp._sgltype
        print mp._transtype
        print mp._uniq

if __name__ == '__main__':
    test()