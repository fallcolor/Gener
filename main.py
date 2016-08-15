import sys
import time


from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

import scripts.ConfigClass as cc

reload(sys)
sys.setdefaultencoding('utf8')



def StartGui():
    global val, root, nb, msgFrame, sglFrame, mc
    root = Tk()
    root.title('configration tool')
    root.geometry('800x600+100+20')

    mc = cc.MapConfig()

    nb = ttk.Notebook(root)
    msgFrame = LabelFrame(nb, height = 20, width = 30)
    sglFrame = SignalFrameControl(nb, height = 20, width = 30)
    nb.add(msgFrame, text = 'Basic config')
    nb.add(sglFrame, text = 'Signal Map')

    mc.AddDisplayFunc(sglFrame.Refresh)

    inacfg = FileDeal(root, cbfunc = mc.AddVarsFrmoFile, inText = 'input acfg')
    inacfg.ConfigOpen('configuration for application', '.ac', 'Open acfg')
    inacfg.pack()

    inhcfg = FileDeal(root, inText = 'input hcfg')
    inhcfg.ConfigOpen('configuration for hardware', '.hc', 'Open hcfg')
    inhcfg.pack()

    indbc = FileDeal(root, inText = 'input dbc')
    indbc.ConfigOpen('data for can', '.dbc', 'Open dbc')
    indbc.pack()

    geneBtn = Button(root, text = "generate code")
    geneBtn.pack()

    nb.pack(fill = BOTH, expand = 1)
    
    root.mainloop()

class FileDeal(object):
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
    def __init__(self, rootCom, varNum, varType, varName):
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
        self._combo3 = ttk.Combobox(self._lf, width = 25)
        self._combo3.state(['readonly'])

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

    def pack(self):
        self._lf.pack(fill = X)
        self._num.pack(side = LEFT)
        self._type.pack(side = LEFT)
        self._var.pack(side = LEFT)
        self._combo1.pack(side = LEFT)
        self._combo2.pack(side = LEFT)
        self._combo3.pack(side = LEFT)

class SignalFrameControl(LabelFrame):
    # def __init__(self):
    #     self._mapList = []
    def Refresh(self):
        self._mapList = []
        # print 'Call SignalFrameControl.Refresh()'
        for vs in mc._maps:
            sm = SignalMapControl(self, vs._num, vs._type, vs._var)
            self._mapList.append(sm)
            sm.pack()


if __name__ == '__main__':
    StartGui()