'''
user control
'''
from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

class FileDealControl(object):
    def __init__(self, rootCom, cbfunc = None, inText = "FileDeal"):
        self._open = True
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
        if self._fileOption.has_key('title'):
            f = tkFileDialog.askopenfile(mode = 'r', **self._fileOption)

            if f:
                self._label['text'] = f.name
                if self._callbackFunc == None:
                    print 'no binding callback function'
                else:
                    self._callbackFunc(f.name)
                    print 'file diag call back'
            else:
                print 'Open dbc file failed'
        else:
            print 'Please add file options.'

    def GetPath(self):
        return _label['text']

    def pack(self):
        self._lf.pack(fill = X)
        self._button.pack(side = LEFT);
        self._label.pack(side = LEFT);

class SignalMapControl(object):
    '''
    a control for signal mapping
    '''
    def __init__(self, rootCom, varNum, varType, varName, cb2value = '', cb3value = ''):
        self._lf = LabelFrame(rootCom, text = '')
        self._num = Label(self._lf, width = 5, text = varNum)
        self._type = Label(self._lf, width = 8, text = varType, anchor = 'sw')
        self._var = Label(self._lf, width = 17, text = varName, anchor = 'sw')
        self._combo1 = ttk.Combobox(self._lf, width = 15)
        self._combo1.state(['readonly'])
        self._combo1.bind('<<ComboboxSelected>>', self.cb1Select)
        self._combo2 = ttk.Combobox(self._lf, width = 30)        
        self._combo2.state(['readonly'])
        self._combo2.bind('<<ComboboxSelected>>', self.cb2Select)
        self.AddCb2Value(cb2value)
        self._combo3 = ttk.Combobox(self._lf, width = 25)
        self._combo3.state(['readonly'])
        self.AddCb3Value(cb3value)

    def cb1Select(self, e = None):
        if self._combo1.get() == "CAN signal":  
            self.AddCb2Value(signals['CAN signal'].keys())
        elif self._combo1.get() == "Hareware IO":  
            self.AddCb2Value(signals['Hareware IO'].keys())

    def cb2Select(self, e = None):
        if self._combo1.get() == "Hareware IO":  
            self.AddCb3Value(signals['Hareware IO'][self._combo2.get()])            
            self._combo3.set('')
        elif self._combo1.get() == "CAN signal":  
            self.AddCb3Value(signals['CAN signal'][self._combo2.get()])            
            self._combo3.set('')

    def AddCb2Value(self, vl):
        self._combo2['value'] = vl

    def AddCb3Value(self, vl):
        self._combo3['value'] = vl

    def EditMap(self, varNum, varType, varName, cb2value = '', cb3value = ''):
        self._num['text'] = varNum
        self._type['text'] = varType
        self._var['text'] = varName
        self.AddCb2Value(cb2value)
        self.AddCb3Value(cb3value)

    def GetMap(self):
        cb1str = self._combo1.get()
        cb3str = self._combo3.get()
        if self._combo1.get() == "CAN signal":
            if cb1str and cb3str:
                return self._num['text'], self._var['text'], cb1str, cb3str.split('(')[0], self._type['text']
            else:
                return self._num['text'], self._var['text'], None, None, None
        else:
            if cb1str and cb3str:
                return self._num['text'], self._var['text'], cb1str, cb3str, self._type['text']
            else:
                return self._num['text'], self._var['text'], None, None, None

    def forget(self):
        self._lf.forget()
        self._num.forget()
        self._type.forget()
        self._var.forget()
        self._combo1.forget()
        self._combo2.forget()
        self._combo3.forget()
        # self.forget()

    def pack(self):
        self._lf.pack(fill = X)
        self._num.pack(side = LEFT)
        self._type.pack(side = LEFT)
        self._var.pack(side = LEFT)
        self._combo1.pack(side = LEFT)
        self._combo2.pack(side = LEFT)
        self._combo3.pack(side = LEFT)

class MessageConfigControl(object):
    def __init__(self, rootCom, num, msgid, name):
        self._chkVar = IntVar()
        self._chkEnable = IntVar()
        self._prdVar = StringVar()
        self._DLCVar = StringVar()
        self._lf = LabelFrame(rootCom, text = '')
        self._chk = Checkbutton(self._lf, variable = self._chkVar)
        self._num = Label(self._lf, text = num)
        self._Id = Label(self._lf, text = msgid)
        self._msgname = Label(self._lf, text = name)
        self._node = ttk.Combobox(self._lf, width = 15)
        self._prd = Entry(self._lf, textvariable = self._prdVar)
        self._prd.insert(0, '100')
        self._DLC = Entry(self._lf, textvariable = self._DLCVar)
        self._DLC.insert(0, '8')
        self._enable = Checkbutton(self._lf, variable = self._chkEnable, text = 'Enable')

    def GetValue(self):
        return self._Id['text'], self._prd.get(), self._DLC.get(), self._chkEnable.get(), self._chkVar.get()

    def ChangeValue(self, num, msgid, name, node, prd, dlc, en, chk):
        self._num['text'] = num
        self._Id['text'] = msgid
        self._msgname['text'] = name
        self._node.set(node)
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

    def forget(self):
        self._lf.forget()
        self._chk.forget()
        self._num.forget()
        self._Id.forget()
        self._msgname.forget()
        self._node.forget()
        self._prd.forget()
        self._DLC.forget()
        self._enable.forget()

    def pack(self):
        self._lf.pack(fill = X)
        self._chk.pack(side = LEFT)
        self._num.pack(side = LEFT)
        self._Id.pack(side = LEFT)
        self._msgname.pack(side = LEFT)
        self._node.pack(side = LEFT)
        self._prd.pack(side = LEFT)
        self._DLC.pack(side = LEFT)
        self._enable.pack(side = LEFT)


class MessageFrameControl(LabelFrame):
    def __init__(self, ro, **kwArg):
        LabelFrame.__init__(self, ro, **kwArg)
        self._chkFrm = None
        self._ecuList = []
        self._chkVar = []
        self._mcList = []

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
        # mcc = MessageConfigControl(self, 10, 'sdf', 'sdfsdfsdf')
        # self._mcList.append(mcc)
        # self._mcList[0].pack()
        # self._mcList[0].ChangeValue(1, 'sdfsd', 'nameeee', 2, 100, 7, 0, 1)
        cnt = 0
        for msgcfg in self._mcList:
            msgcfg.forget()
        for msgcfg in mc._msgcfgs:
            if cnt == len(self._mcList):
                self._mcList.append(MessageConfigControl(self, cnt + 1, msgcfg._Id, msgcfg._name))
            else:
                self._mcList[cnt].ChangeValue(cnt + 1, msgcfg._Id, msgcfg._name, msgcfg._node, msgcfg._prd, msgcfg._DLC, msgcfg._enable, msgcfg._checked)
            self._mcList[cnt].pack()
            cnt += 1

class SignalFrameControl(LabelFrame):
    def __init__(self, ro, **kwArg):
        LabelFrame.__init__(self, ro, **kwArg)
        self._mapList = []
    def Refresh(self, mc):
        # print 'Call SignalFrameControl.Refresh()'
        cnt = 0
        for vs in self._mapList:
            vs.forget()

        for vs in mc._maps:
            if cnt == len(self._mapList):
                sm = SignalMapControl(self, vs._num, vs._type, vs._var, vs._transtype, vs._sgltype)
                self._mapList.append(sm)
            else:
                self._mapList[cnt].EditMap(vs._num, vs._type, vs._var, vs._transtype, vs._sgltype)
            self._mapList[cnt].pack()
            cnt += 1

def test():
    root = Tk()
    root.title('configration tool')
    root.geometry('800x600+100+20')
    lb = LabelFrame(root)
    lb.pack()
    mcc = MessageConfigControl(lb, 10, 'sdf', 'sdfsdfsdf')
    mcc.pack()
    mcc.ChangeValue(1, 'sdfsd', 'nameeee', 2, 100, 7, 0, 1)
    print mcc
    print mcc._chk

    root.mainloop()


if __name__ == '__main__':
    test()