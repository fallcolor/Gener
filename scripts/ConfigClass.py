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
    def IsNotEmpty(self):
        hclen = 0;
        hclen += len(self._DI)
        hclen += len(self._DO)
        hclen += len(self._PWM)
        hclen += len(self._AI)
        if hclen > 0:
            return True
        return False

class CanConfig(cm.CanMatrix):
    def ImportFromFile(self, infile):
        dbcImportEncoding = 'iso-8859-1'
        # dbcImportEncoding = 'utf-8'
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
            bo._checked = False
            if bo._Id > 0x80000000:
                bo._Id -= 0x80000000
                bo._extended = 1
            tmpstr = hex(bo._Id)
            bo._Id = tmpstr[0:2] + tmpstr[2:-1].upper()
        self._fl._list.sort(key = lambda Frame: Frame._name)

    def IsNotEmpty(self):
        if len(self._fl._list) > 0:
            return True
        return False

    def GetSignals(self):
        re = {}
        for fr in self._fl._list:
            if fr._checked:
                frid = fr._name + ' (' + '%s' % fr._Id + ')'
                listSignal = []
                for sgl in fr._signals:
                    strtmp = sgl._name + " (" + str(sgl._startbit) + '/' + str(sgl._signalsize) + ")"
                    listSignal.append(strtmp)
                re[frid] = listSignal
        return re

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
        self._dbc = CanConfig()
        self._hc = HwConfig()
        self._svfname = ''

    def AddVarsFrmoFile(self, infile):
        '''
        tbc: ChangeVariables
        '''
        ac = AppConfig()
        ac.ImportFromFile(infile)
        self.AddVariables(ac)

    # import data from app config
    def AddVariables(self, ac):
        self._appver = ac._version
        self._prj = ac._prj

        self.ChangeVariables(ac)

        self._displayfunc(self)

    def ChangeVariables(self, ac):
        '''
        refresh the variable of signal maps
        '''
        mpVar = [[mp._var, mp._type] for mp in self._maps]
        acVar = [acvar for acvar in ac._vars]

        # delete the element in self._maps but not in app config file
        tmpmap = []
        i = 0
        while i < len(mpVar):
            mpcnt = mpVar.count(mpVar[i])
            acvcnt = acVar.count(mpVar[i])
            if mpcnt < acvcnt:
                for j in range(mpcnt):
                    tmpmap.append(self._maps[i + j])
                for k in range(acvcnt - mpcnt):
                    tmpmap.append(SignalMap(0, mpVar[i]))
            elif mpcnt == acvcnt:
                for j in range(mpcnt):
                    tmpmap.append(self._maps[i + j])
            else:
                for j in range(acvcnt):
                    tmpmap.append(SignalMap(0, mpVar[i]))
            i += mpcnt

        # add new element in app config
        i = 0
        while i < len(acVar):
            acvcnt = acVar.count(acVar[i])
            mpcnt = mpVar.count(acVar[i])
            if mpcnt == 0:
                for j in range(acvcnt):
                    tmpmap.append(SignalMap(0, acVar[i + j]))
            i += acvcnt
        tmpmap.sort(key = lambda sglmap: sglmap._var)
        self._maps = tmpmap

    # import data from hardware
    def ChangeHwConfig(self, hc):

        return True

    # import data from dbc
    def AddDbcFromFile(self, infile):
        self._dbc = CanConfig()
        self._dbc.ImportFromFile(infile)
        self.AddDbc(self._dbc)

    def AddDbc(self, dbc):
        # print 'call adddbc()'
        # ECU selection
        self.ChangeEcu(dbc)

        # message frame configuration
        self.ChangeMsgConfig(dbc)

        # signal map configuration

        self._displayfunc(self)

    def ChangeEcu(self, dbc):
        '''
        refresh the ecu, delete not in dbc, and add new element
        '''
        # delete the element in self._ecu but not in dbc
        tmpdict = {}
        for ecuname in self._ecu:
            for ecu in dbc._BUs._list:
                if ecuname == ecu._name:
                    tmpdict[ecuname] = self._ecu[ecuname]
                    break
        self._ecu = tmpdict

        # add new element in dbc
        for ecu in dbc._BUs._list:
            self._ecu.setdefault(ecu._name, False)

    def ChangeMsgConfig(self, dbc):
        '''
        refresh the message config, delete not in dbc, and add new element
        '''
        tmpcfgs = []
        # delete the frame in self._msgcfgs but not in dbc
        for mcfg in self._msgcfgs:
            for fr in dbc._fl._list:
                if mcfg._Id == fr._Id:
                    tmpcfgs.append(mcfg)
                    break
        self._msgcfgs = tmpcfgs
        # add new frame
        for fr in dbc._fl._list:
            containId = [mcfg._Id for mcfg in self._msgcfgs]
            if fr._Id not in containId:
                self.AddMsgConfig(fr._Id, fr._name)
        self._msgcfgs.sort(key = lambda mcfg: mcfg._name)

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

    def EditMap(self, num, sgl, st, tt, uniq):
        '''
        map of signal and variable
        '''
        for mp in self._maps:
            if mp._num == num:
                self._signal = sgl
                self._sgltype = st
                self._transtype = tt
                self._uniq = uniq
                return True
        return False

    def GetMaps(self, signal):
        relist = []
        for sv in self._maps:
            tmpsgl = sv._signal.split(' ')[0]
            if signal == tmpsgl:
                relist.append([sv._var, sv._type, sv._signal])
        return relist

    def ImportFromFile(self, infile):
        f = open(infile, 'rb')
        data = json.loads(f.read())
        self._time = data['time']
        self._hwver = data['hwver']
        self._appver = data['appver']
        self._prj = data['project']
        self._ecu = data['ecu']
        if self._dbc.IsNotEmpty():
            self.ChangeEcu(self._dbc)
        self._cancfg = data['canconfig']
        self._msgcfgs = []  # clear last data
        self._maps = []
        for sc in data['msgconfig']:
            self._msgcfgs.append(MessageConfig(sc['ID'], sc['name'], sc['node'], sc['prd'] \
                , sc['DLC'], sc['enable'], sc['checked']))
        num = 0
        for mp in data['map']:
            num += 1
            self._maps.append(SignalMap(num, [mp[0], mp[1]], mp[2], mp[3], mp[4], mp[5]))
        # self._fl._list.sort(key = lambda Frame: Frame._name)
        self._maps.sort(key = lambda sglmap: sglmap._var)
        self._displayfunc(self)

    def GetSvFilePath(self, outfile):
        self._svfname = outfile

    def ExportSvToFile(self):
        data = {}
        data['time'] = self._time
        data['hwver'] = self._hwver
        data['appver'] = self._appver
        data['project'] = self._prj
        data['ecu'] = self._ecu
        data['canconfig'] = self._cancfg
        data['msgconfig'] = []
        for mc in self._msgcfgs:            
            data['msgconfig'].append(mc.GetValue())
        data['map'] = []
        for mp in self._maps:
            data['map'].append(mp.GetValue())
        try:
            f = open(self._svfname, 'w')
            f.write(json.dumps(data, indent = 4))
            f.close()
            print 'success for generated json file!'
        except Exception, e:
            print Exception,":",e

    def ChangeFromFrame(self, ecus, ccs, mcs, mps):
        self._ecu = ecus
        self._cancfg = ccs
        self._msgcfgs = []

        for sc in mcs:
            msgcfg = MessageConfig(sc['ID'], sc['name'], sc['node'], sc['prd']\
                , sc['DLC'], bool(sc['enable']), bool(sc['checked']))
            self._msgcfgs.append(msgcfg)
            # modify the  _checked attribute of dbc frame
            cnt = 0
            for fr in self._dbc._fl._list:
                if msgcfg._Id == fr._Id:
                    self._dbc._fl._list[cnt]._checked = msgcfg._checked
                cnt += 1

        self._maps = []
        num = 0
        for mp in mps:
            num += 1
            self._maps.append(SignalMap(num, [mp[0], mp[1]], mp[2], mp[3], mp[4], mp[5]))

    def GetTransEcu(self):
        re = []
        for ecu in self._ecu:
            if self._ecu[ecu]:
                re.append(ecu)
        return re

    def CheckSelf(self):
        '''
        whether data right
        '''
        # dbc
        if self._dbc.IsNotEmpty() is not True:
            restr = 'No dbc!'
            return False, 'No dbc!'

        # file name
        if self._svfname == '':
            restr = 'No file name!'
            return False, 'No file name!'
        
        # all variable-signal map done
        iserr, restr = self.IsMapConfigNotDone()
        if iserr:
            return False, restr

        # signal select contained by self._dbc and self._hc
        iserr, restr = self.IsMapSglContained()
        if iserr:
            return False, restr

        return True, ''

    def IsMapConfigNotDone(self):
        iserror = False
        restr = ''
        for mp in self._maps:
            if mp.IsMapDone() == False:
                iserror = True
                restr += str(mp._num) + '  ' + mp._var + '\n' 
        if iserror:
            restr = 'The following vars map not done!\n' + restr
            return True, restr
        else:
            return False, restr

    def IsMapSglContained(self):
        iserror = False
        refreshreq = False
        restr = 'The following signal of map not in dbc or the message frame not chedked\n'
        signals = {}
        signals['CAN signal'] = self._dbc.GetSignals()
        # signals['Hareware IO']

        for i in range(len(self._maps)):
            bcontain, bframe = self._maps[i].IsMapWell(signals)

            if bcontain == False:
                iserror = True
                restr += str(self._maps[i]._num) + '  ' + self._maps[i]._var +'\n'
            else:
                if bframe == False:
                    refreshreq = True
        if refreshreq:
            self._displayfunc(self)

        if iserror:
            return True, restr
        else:
            return False, ''


    def AddDisplayFunc(self, func):
        self._displayfunc = func

class MessageConfig(object):
    '''
    '''
    def __init__(self, msgid = '', na = '',nd = 2,  prd = 100, dlc = 8, en = False, chked = False):
        self._Id = msgid
        self._name = na
        self._node = nd
        self._prd = prd
        self._tran = False
        self._DLC = dlc
        self._enable = en
        self._checked = chked
    def ChangeMsgCfg(mc):
        self._Id = mc._Id
        self._name = mc._name
        self._node = mc._node
        self._prd = mc._prd
        self._tran = mc._tran
        self._DLC = mc._DLC
        self._IDE = mc._IDE
        self._enable = mc._enable
        self._checked = mc._checked
    def GetValue(self):
        re = {}
        re['ID'] = self._Id
        re['name'] = self._name
        re['node'] = self._node
        re['prd'] = self._prd
        re['trans'] = self._tran
        re['DLC'] = self._DLC
        re['enable'] = self._enable
        re['checked'] = self._checked
        return re

class SignalMap(object):
    '''
    signal map. configurate by user.
    '''
    def __init__(self, num, var, sgl = '', st = '', tt = '', uniq = False):
        self._num = num
        self._var = var[0]
        self._type = var[1]
        self._signal = sgl
        self._sgltype = st      # msg name or DI\DO\PWM
        self._transtype = tt    # can or hw IO
        self._uniq = uniq
    def GetValue(self):
        re = []
        re.append(self._var)
        re.append(self._type)
        re.append(self._signal)
        re.append(self._sgltype)
        re.append(self._transtype)
        re.append(self._uniq)
        return re
    def ClearMap(self):
        self._signal = ''
        self._sgltype = ''      # msg name or DI\DO\PWM
        self._transtype = ''    # can or hw IO
        self._uniq = False
    def IsMapDone(self):
        # whether maped
        if self._signal == '' or self._sgltype == '' or self._transtype == '':
            return False
        return True

    def IsMapWell(self, sgls):
        '''
        mapped signal contained by signals
        '''
        # dbc
        if self._transtype == 'CAN signal':
            for fr in sgls['CAN signal']:
                if self._signal in sgls['CAN signal'][fr]:
                    if self._sgltype == fr:
                        # signal contained, and the same frame name
                        return True, True
                    else:
                        # signal contained, but different frame name, change it
                        self._sgltype = fr
                        return True, False
        return False, False




def EmptyFunc(ef):
    pass

def printmc(mc):
    print 'App vension is %s' % mc._appver
    print 'Hw vension is %s' % mc._hwver
    print 'Reference ECU are : ', mc._ecu
    print 'can config:', mc._cancfg
    print 'message config:'
    for mcmc in mc._msgcfgs:
        print 'id    :', mcmc._Id
        print '  node:', mcmc._node
        print '  prd :', mcmc._prd
        print '  tran:', mcmc._tran
        print '  DLC :', mcmc._DLC
        print '  en  :', mcmc._enable
        print '  chk :', mcmc._checked
    print 'Signal maps:'
    for mp in mc._maps:
        print 'num   :', mp._num
        print '  var :', mp._var
        print '  type:', mp._type
        print '  sgl :', mp._signal
        print '  sglt:', mp._sgltype
        print '  trt :', mp._transtype
        print '  uniq:', mp._uniq

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