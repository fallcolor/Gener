'''
user control
'''
from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

class FileDealControl(object):
    def __init__(self, rootCom, cbfunc = None, inText = "FileDeal", save = False):
        self._save = save
        self._fileOption = {}
        self._root = rootCom
        self._text = inText
        self._lf = LabelFrame(rootCom, text = '')
        self._button = Button(self._lf, text =  inText, command = self.OpenOrSaveFile)
        self._label = Label(self._lf, text = 'file path');
        self._filePath = None
        self._callbackFunc = cbfunc

    def ConfigOpen(self, filetype, suffix, title):
        self._open = True
        self._fileOption['defaultextension'] = suffix
        self._fileOption['filetypes'] = [(filetype, suffix), ('all files', '.*')]
        # self._fileOption['initialdir'] = 'e:\\'
        # self._fileOption['initialfile'] = 'myfile.acfg'
        self._fileOption['parent'] = self._root
        # self._fileOption['multiple'] = 1
        self._fileOption['title'] = title

    def OpenOrSaveFile(self):
        if self._save:
            if self._fileOption.has_key('title'):
                f = tkFileDialog.asksaveasfilename(**self._fileOption)
                print f
                if f:
                    if self._callbackFunc == None:
                        print 'no binding callback function'
                    else:
                        self._callbackFunc(f)
                else:
                    print 'save file failed', f
            else:
                print 'Please add file options.'
        else:
            if self._fileOption.has_key('title'):
                f = tkFileDialog.askopenfile(mode = 'r', **self._fileOption)
                if f:
                    self._label['text'] = f.name
                    if self._callbackFunc == None:
                        print 'no binding callback function'
                    else:
                        self._callbackFunc(f.name)
            else:
                print 'Please add file options.'

    def GetPath(self):
        return _label['text']

    def pack(self):
        self._lf.pack(fill = X)
        self._button.pack(side = LEFT);
        self._label.pack(side = LEFT);

class SignalMapControl(Frame):
    '''
    a control for signal mapping
    '''
    def __init__(self, rootCom, varNum, varType, varName, cb1value = '', cb2value = '', cb3value = '', unk = False, **kArg):
        Frame.__init__(self, rootCom, **kArg)
        # self._lf = LabelFrame(rootCom, text = '')
        self._num = Label(self, width = 5, text = varNum)
        self._type = Label(self, width = 8, text = varType, anchor = 'w')
        self._var = Label(self, width = 17, text = varName, anchor = 'w')
        self._combo1 = ttk.Combobox(self, width = 13)
        self._combo1.state(['readonly'])
        self._combo1.bind('<<ComboboxSelected>>', self.cb1Select)
        self._combo1.set(cb1value)
        self._combo2 = ttk.Combobox(self, width = 28)        
        self._combo2.state(['readonly'])
        self._combo2.bind('<<ComboboxSelected>>', self.cb2Select)        
        self._combo2.set(cb2value)
        self._combo3 = ttk.Combobox(self, width = 25)
        self._combo3.state(['readonly'])        
        self._combo3.set(cb3value)
        self._unique = unk
        self._signals = {}

        self._num.pack(side = LEFT)
        self._type.pack(side = LEFT)
        self._var.pack(side = LEFT)
        self._combo1.pack(side = LEFT)
        self._combo2.pack(side = LEFT)
        self._combo3.pack(side = LEFT)

    def cb1Select(self, e = None):
        if self._combo1.get() == "CAN signal":  
            self.AddCb2Value(self._signals['CAN signal'].keys())
        elif self._combo1.get() == "Hareware IO":  
            self.AddCb2Value(self._signals['Hareware IO'].keys())

    def cb2Select(self, e = None):
        if self._combo1.get() == "Hareware IO":  
            self.AddCb3Value(self._signals['Hareware IO'][self._combo2.get()])            
            self._combo3.set('')
        elif self._combo1.get() == "CAN signal":  
            self.AddCb3Value(self._signals['CAN signal'][self._combo2.get()])            
            self._combo3.set('')

    def AddCb1Value(self, vl):
        self._combo1['value'] = vl

    def AddCb2Value(self, vl):
        vl.sort()
        self._combo2['value'] = vl

    def AddCb3Value(self, vl):
        '''
        sgl like -- TM_InvTemp (0/16) --, key is 0
                 -- Bus_Volt (24/16) --, key is 24
        '''
        vl.sort(key = lambda sgl: int(sgl.split(' ')[1][1:].split('/')[0]))
        self._combo3['value'] = vl

    def EditMap(self, varNum, varType, varName, cb1value = '', cb2value = '', cb3value = '', unk = False):
        self._num['text'] = varNum
        self._type['text'] = varType
        self._var['text'] = varName
        self._combo1.set(cb1value)
        self._combo2.set(cb2value)
        self._combo3.set(cb3value)
        self._unique = unk

    def GetMap(self):
        re = []
        re.append(self._var['text'])
        re.append(self._type['text'])
        cb3str = self._combo3.get()
        re.append(cb3str)       
        cb2str = self._combo2.get()
        re.append(cb2str)
        cb1str = self._combo1.get()
        re.append(cb1str)
        re.append(self._unique)
        return re

    # def forget(self):
    #     self._lf.forget()
    #     self._num.forget()
    #     self._type.forget()
    #     self._var.forget()
    #     self._combo1.forget()
    #     self._combo2.forget()
    #     self._combo3.forget()
    #     # self.forget()

    # def pack(self):
    #     self._lf.pack(fill = X)
    #     self._num.pack(side = LEFT)
    #     self._type.pack(side = LEFT)
    #     self._var.pack(side = LEFT)
    #     self._combo1.pack(side = LEFT)
    #     self._combo2.pack(side = LEFT)
    #     self._combo3.pack(side = LEFT)

class MessageConfigControl(Frame):
    def __init__(self, parent, *arg, **karg):
        Frame.__init__(self, parent, **karg)
        self._chklen = 3
        self._numlen = 3
        self._Idlen = 12
        self._namelen = 25
        self._nodelen = 6
        self._prdlen = 10
        self._dlclen = 6
        self._chkVar = IntVar()
        self._chkEnable = IntVar()
        self._nodeVar = StringVar()
        self._prdVar = StringVar()
        self._DLCVar = StringVar()
        self._chk = Checkbutton(self, variable = self._chkVar, width = self._chklen)
        self._chk['command'] = self.MessageChecked
        self._num = Label(self, text = arg[0], width = self._numlen)
        self._Id = Label(self, text = arg[1], width = self._Idlen, anchor = 'e')
        self._msgname = Label(self, text = arg[2], width = self._namelen, anchor = 'w')
        self._node = Entry(self, textvariable = self._nodeVar, width = self._prdlen, justify = CENTER)
        self._node.insert(0, '2')
        self._prd = Entry(self, textvariable = self._prdVar, width = self._prdlen, justify = CENTER)
        self._prd.insert(0, '100')
        self._DLC = Entry(self, textvariable = self._DLCVar, width = self._dlclen, justify = CENTER)
        self._DLC.insert(0, '8')
        self._enable = Checkbutton(self, variable = self._chkEnable)

        self._chk.pack(side = LEFT)
        self._num.pack(side = LEFT)
        self._Id.pack(side = LEFT)
        self._msgname.pack(side = LEFT, padx = 8)
        self._node.pack(side = LEFT, padx = 8)
        self._prd.pack(side = LEFT, padx = 8)
        self._DLC.pack(side = LEFT, padx = 8)
        self._enable.pack(side = LEFT, padx = 8)

    def MessageChecked(self):
        self._DLCVar.set(self._chkVar.get())
        if self._chkVar.get() == 0:
            self._node['bg'] = 'gray'
            self._prd['bg'] = 'gray'
            self._DLC['bg'] = 'gray'
        else:
            self._node['bg'] = 'white'
            self._prd['bg'] = 'white'
            self._DLC['bg'] = 'white'

    def GetValue(self):
        return self._Id['text'], self._msgname['text'], self._node.get(), self._prd.get(), self._DLC.get(), self._chkEnable.get(), self._chkVar.get()

    def ChangeValue(self, num, msgid, name, node, prd, dlc, en, chk):
        self._num['text'] = num
        self._Id['text'] = msgid
        self._msgname['text'] = name
        self._nodeVar.set(node)
        self._prdVar.set(prd)
        self._DLCVar.set(dlc)
        if en == 1:
            self._enable.select()
        else:
            self._enable.deselect()
        if chk == 1:
            self._chk.select()
        else:
            self._chk.deselect()
        self.MessageChecked()

class MessageFrameControl(LabelFrame):
    def __init__(self, ro, **kwArg):
        LabelFrame.__init__(self, ro, **kwArg)
        self._chkFrm = None
        self._mcFrm = None
        self._ecuList = []
        self._chkVar = []
        self._mcList = []

    def GetValue(self):
        chkValue = {}
        mcValue = []
        # ecu check valud
        cnt = 0
        for ecu in self._ecuList:
            chkValue[ecu['text']] = bool(self._chkVar[cnt].get())
            cnt += 1
        for mc in self._mcList:
            tmpstr = mc.GetValue()
            tmp = {}
            tmp['ID'] = tmpstr[0]
            tmp['name'] = tmpstr[1]
            tmp['node'] = tmpstr[2]
            tmp['prd'] = tmpstr[3]
            tmp['DLC'] = tmpstr[4]
            tmp['enable'] = tmpstr[5]
            tmp['checked'] = tmpstr[6]
            mcValue.append(tmp)
        return chkValue, mcValue


    def Refresh(self, mc):
        # check button
        cnt = 0
        if self._chkFrm is None:
            self._chkFrm = LabelFrame(self, text = 'Select Tx ECU')
            self._chkFrm.pack(fill = X)

        for ecu in self._ecuList:
            ecu.forget()

        for ecu in mc._ecu:
            if cnt == len(self._ecuList):   # cnt is index, is len - 1
                self._chkVar.append(IntVar())
                chkbtn = Checkbutton(self._chkFrm, text = ecu, variable = self._chkVar[cnt])
                # chkbtn = Checkbutton(self._chkFrm, text = ecu)           
                self._ecuList.append(chkbtn)
            else:
                # self._chkVar.append(IntVar())
                self._ecuList[cnt]['text'] = ecu
            self._ecuList[cnt].pack(side = LEFT)
            cnt += 1

        # message config
        if self._mcFrm is None:
            lf = Frame(self)
            l0 = Label(lf, text = 'check', width = 5).pack(side = LEFT, padx = 2)
            l1 = Label(lf, text = 'No.', width = 5, justify = CENTER).pack(side = LEFT)
            l2 = Label(lf, text = 'ID', width = 12).pack(side = LEFT)
            l3 = Label(lf, text = 'name', width = 23).pack(side = LEFT, padx = 6)
            l4 = Label(lf, text = 'node', width = 6).pack(side = LEFT, padx = 26)
            l5 = Label(lf, text = 'prd', width = 10).pack(side = LEFT, padx = 8)
            l6 = Label(lf, text = 'DLC', width = 6).pack(side = LEFT, padx = 8)
            l7 = Label(lf, text = 'enable', width = 6).pack(side = LEFT)
            lf.pack(fill = X)
            self._mcFrm = LabelFrame(self)
            self._mcFrm.pack(fill = BOTH, expand=True)
            self._sb = Scrollbar(self._mcFrm)
            self._sb.pack(side = RIGHT, fill = Y)
            self._cvs = Canvas(self._mcFrm)
            self._cvs.forget()
            self._cvs.pack(side = LEFT, fill = BOTH, expand=True)
            self._cvs['yscrollcommand'] = self._sb.set
            self._sb['command'] = self._cvs.yview
        cnt = 0
        self._cvs.delete('all')
        self._mcList = []

        for msgcfg in mc._msgcfgs:
            # if cnt == len(self._mcList):
            self._mcList.append(MessageConfigControl(self._cvs, cnt + 1, msgcfg._Id, msgcfg._name))
            self._mcList[cnt].ChangeValue(cnt + 1, msgcfg._Id, msgcfg._name, msgcfg._node, msgcfg._prd, msgcfg._DLC, msgcfg._enable, msgcfg._checked)
            self._cvs.create_window(0, cnt * 30, anchor = NW, window = self._mcList[cnt])
            # else:
            #     self._mcList[cnt].ChangeValue(cnt + 1, msgcfg._Id, msgcfg._name, msgcfg._node, msgcfg._prd, msgcfg._DLC, msgcfg._enable, msgcfg._checked)
            cnt += 1
        self._cvs['scrollregion'] = (0, 0, 800, cnt * 30)

class SignalFrameControl(Frame):
    def __init__(self, ro, **kwArg):
        Frame.__init__(self, ro, **kwArg)
        self._mapList = []
        self._smFrm = None
    def GetValue(self):
        re = []
        for sm in self._mapList:
            re.append(sm.GetMap())
        return re

    def Refresh(self, mc):
        
        if self._smFrm is None:
            self._smFrm = LabelFrame(self)
            self._smFrm.pack(fill = BOTH, expand=True)
            self._sb = Scrollbar(self._smFrm)
            self._sb.pack(side = RIGHT, fill = Y)
            self._cvs = Canvas(self._smFrm)
            self._cvs.forget()
            self._cvs.pack(side = LEFT, fill = BOTH, expand=True)
            self._cvs['yscrollcommand'] = self._sb.set
            self._sb['command'] = self._cvs.yview
        cnt = 0
        self._cvs.delete('all')
        self._mapList = []

        # fresh combobox value
        cb1value = []
        if len(mc._dbc._fl._list) > 0:
            cb1value.append('CAN signal')

        if mc._hc.IsNotEmpty():
            cb1value.append('Hardware IO')

        mapsignals = mc._dbc.GetSignals()
        # print mapsignals
        for vs in mc._maps:
            sm = SignalMapControl(self._cvs, cnt + 1, vs._type, vs._var, vs._transtype, vs._sgltype, vs._signal)
            
            # display signal map if maped and has dbc
            if mapsignals:
                # if mc._dbc.IsNotEmpty():
                sm._signals['CAN signal'] = mapsignals
                sm.AddCb1Value(sm._signals.keys())
                if sm._combo1.get():
                    sm.AddCb2Value(sm._signals[sm._combo1.get()].keys())
                # if sm._combo2.get():
                #     sm.AddCb3Value(sm._signals[sm._combo1.get()][sm._combo2.get()])
            self._mapList.append(sm)
            self._cvs.create_window(2, cnt * 30, anchor = NW, window = self._mapList[cnt])
            cnt += 1
        self._cvs['scrollregion'] = (0, 0, 800, cnt * 30)

def test():
    root = Tk()
    root.title('configration tool')
    root.geometry('800x600+100+20')

    cv = Canvas(root)
    sb = Scrollbar(root)
    cv['yscrollcommand'] = sb.set
    sb['command'] = cv.yview

    for i in range(10):
        mc = MessageConfigControl(cv, i, 'sdfsdf', 'sdfsdf')
        mc.pack()

    root.mainloop()


if __name__ == '__main__':
    test()

# root.bind(<MouseWheel>)