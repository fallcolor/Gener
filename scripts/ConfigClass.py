'''
    config file class:
    class AppConfig()
    class HwConfig()
    class MapConfig()

'''
import json
import canmatrix as cm
import re

'''
>>> mylist = [1,2,2,2,2,3,3,3,4,4,4,4]
>>> myset = set(mylist)
>>> for item in myset:
         print("the %d has found %d" %(item,mylist.count(item)))
 
the 1 has found 1
the 2 has found 4
the 3 has found 3
the 4 has found 4
'''

class AppConfig(object):
    '''
    contain app configuration, with following attributes:
        _version
        _prj: project name
        _var: a list of variable, like [["Bat.BusVolt": "float"],["Bat.BusVolt": "float"]]
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

class CanConfig(cm.CanMatrix):
    def ImportFromFile(self, infile):
        dbcImportEncoding='iso-8859-1'
        i = 0

        f = open(infile, 'rb')
        for line in f:
            i = i+1
            l = line.strip()
            if l.__len__() == 0:
                continue

            decoded = l.decode(dbcImportEncoding)
            if decoded.startswith("BO_ "):
                # print re.match("^BO\_ (\w+) (\w+) *: (\w+) (\w+)", decoded).group(1)
                # print tmp.group(1)

                regexp = re.compile("^BO\_ (\w+) (\w+) *: (\w+) (\w+)")
                temp = regexp.match(decoded)
                #db._fl.addFrame(Frame(temp.group(1), temp.group(2), temp.group(3), temp.group(4)))
                if temp:
                    self._fl.addFrame(cm.Frame(temp.group(1), temp.group(2), temp.group(3), temp.group(4)))
                else:
                    regexp = re.compile("^BO\_ (\w+) (\w+) *: (\w+)")
                    temp = regexp.match(decoded)
                    self._fl.addFrame(cm.Frame(temp.group(1), temp.group(2), temp.group(3), None))
                # print temp.group(1), temp.group(2),temp.group(3)
            elif decoded.startswith("SG_ "):
                pattern = "^SG\_ (\w+) : (\d+)\|(\d+)@(\d+)([\+|\-]) \(([0-9.+\-eE]+),([0-9.+\-eE]+)\) \[([0-9.+\-eE]+)\|([0-9.+\-eE]+)\] \"(.*)\""
                regexp = re.compile(pattern)
                temp = regexp.match(decoded)
                regexp_raw = re.compile(pattern.encode(dbcImportEncoding))
                temp_raw = regexp_raw.match(l)
                if temp:
                    #reciever = list(map(str.strip, temp.group(11).split(',')))
                    reciever = None
                    tempSig = cm.Signal(temp.group(1), temp.group(2), temp.group(3), temp.group(4), temp.group(5), temp.group(6), temp.group(7),temp.group(8),temp.group(9),temp_raw.group(10).decode(dbcImportEncoding),reciever)     
                    if tempSig._byteorder == 0:
                        # startbit of motorola coded signals are MSB in dbc
                        tempSig.setMsbStartbit(int(temp.group(2)))                
                    self._fl.addSignalToLastFrame(tempSig)
                else:
                    pattern = "^SG\_ (\w+) (\w+) *: (\d+)\|(\d+)@(\d+)([\+|\-]) \(([0-9.+\-eE]+),([0-9.+\-eE]+)\) \[([0-9.+\-eE]+)\|([0-9.+\-eE]+)\] \"(.*)\" (.*)"
                    regexp = re.compile(pattern)
                    regexp_raw = re.compile(pattern.encode(dbcImportEncoding))
                    temp = regexp.match(decoded)
                    temp_raw = regexp_raw.match(l)
                    # reciever = list(map(str.strip, temp.group(12).split(',')))
                    reciever = None
                    multiplex = temp.group(2)
                    if multiplex == 'M':
                        multiplex = 'Multiplexor'
                    else:
                        multiplex = int(multiplex[1:])

                    self._fl.addSignalToLastFrame(cm.Signal(temp.group(1), temp.group(3), temp.group(4), temp.group(5), temp.group(6), temp.group(7),temp.group(8),temp.group(9),temp.group(10),temp_raw.group(11).decode(dbcImportEncoding),reciever, multiplex))
                # print temp.group(1),temp.group(2),temp.group(3)

            elif decoded.startswith("BU_:"):
                pattern = "^BU\_\:(.*)"
                regexp = re.compile(pattern)
                regexp_raw = re.compile(pattern.encode(dbcImportEncoding))
                temp = regexp.match(decoded)
                if temp:
                    myTempListe = temp.group(1).split(' ')
                    for ele in myTempListe:
                        if len(ele.strip()) > 1:
                            self._BUs.add(cm.BoardUnit(ele))

        for bo in self._fl._list:
            if bo._Id > 0x80000000:
                bo._Id -= 0x80000000
                bo._extended = 1
            tmpstr = hex(bo._Id)
            bo._Id = tmpstr[0:2] + tmpstr[2:-1].upper()
        self._fl._list.sort(key = lambda Frame: Frame._name)

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
        self._displayfunc = EmptyFunc

    # import data from app config
    def AddVariables(self, ac):
        self._appver = ac._version
        self._prj = ac._prj
        # self._maps = []
        cnt = 1
        for var in ac._vars:
            self._maps.append(SignalMap(cnt, var))
            cnt += 1
        self._displayfunc(self)

    def AddVarsFrmoFile(self, infile):
        '''
        tbc: ChangeVariables
        '''
        ac = AppConfig()
        ac.ImportFromFile(infile)
        self.AddVariables(ac)

    def ChangeVariables(self, ac):
        # [i for i in li]
        return True

    # import data from hardware
    def ChangeHwConfig(self, hc):

        return True

    # import data from dbc
    def AddDbcFromFile(self, infile):
        cc = CanConfig()
        cc.ImportFromFile(infile)
        self.AddDbc(cc)

    def AddDbc(self, cc):
        # ECU selection
        self._ecu = {}
        for ecu in cc._BUs._list:
            self._ecu[ecu._name] = False
        # message frame configuration
        self._msgcfgs = []
        for fr in cc._fl._list:
            self.AddMsgConfig(fr._Id, fr._name)

        self._displayfunc(self)

    def AddMsgConfig(self, mid, name):
        self._msgcfgs.append(MessageConfig(msgid = mid, na = name))

    def EditMsgConfig(self, msgid, name, nd, prd, tran, dlc, ide, en, chked):
        for mc in self._msgcfgs:
            if mc._Id == msgid:
                mc._name = name
                mc._node = nd
                mc._prd = prd
                mc._tran = tran
                mc._DLC = dlc
                mc._IDE = ide
                mc._enable = en
                mc._checked = chked
                return True
        return False

    # map of signal and variable
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
            self._msgcfgs.append(MessageConfig(sc['ID'], sc['name'], sc['node'], sc['prd'],sc['trans'] \
                , sc['sglfunc'], sc['DLC'], sc['ide'], sc['enable'], sc['checked']))
        # self._msgcfgs = data['msgconfig']
        num = 0
        for mp in data['map']:
            self._maps.append(SignalMap(num, [mp[0], mp[1]], mp[2], mp[3], mp[4], mp[5]))
            num += 1
        # self._maps = data['map']
        self._displayfunc(self)

    def AddDisplayFunc(self, func):
        self._displayfunc = func

class MessageConfig(object):
    '''
    '''
    def __init__(self, msgid = '', na = '',nd = 0,  prd = 100, tran = False, sf = '', dlc = 8, ide = True, en = True, chked = False):
        self._Id = msgid
        self._name = na
        self._node = nd
        self._prd = prd
        self._tran = tran
        self._sglfunc = sf
        self._DLC = dlc
        self._IDE = ide
        self._enable = en
        self._checked = chked
    def ChangeMsgCfg(mc):
        self._Id = mc._Id
        self._name = mc._name
        self._node = mc._node
        self._prd = mc._prd
        self._tran = mc._tran
        self._sglfunc = mc._sglfunc
        self._DLC = mc._DLC
        self._IDE = mc._IDE
        self._enable = mc._enable
        self._checked = mc._checked

class SignalMap(object):
    '''
    '''
    def __init__(self, num, var, sgl = '', st = '', tt = '', uniq = False):
        self._num = num
        self._var = var[0]
        self._type = var[1]
        self._signal = sgl
        self._sgltype = st      # msg name or DI\DO\PWM
        self._transtype = tt    # can or hw IO
        self._uniq = uniq

def EmptyFunc(ef):
    pass

def printmc(mc):
    print 'App vension is %s' % mc._appver
    print 'Hw vension is %s' % mc._hwver
    print 'Reference ECU are : ', mc._ecu
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

    # mc = MapConfig()
    # mc.ImportFromFile(r'E:\pyproj\gener\test\kk.sv')
    # mc.AddVariables(ac)
    # printmc(mc)

    cc = CanConfig()
    cc.ImportFromFile(r'E:\pyproj\gener\test\ks.dbc')
    for fr in cc._fl._list:
        print fr._name

if __name__ == '__main__':
    test()