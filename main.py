# -*- coding: UTF-8 -*-

import sys
import time


from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk
import json
import scripts.ImportData as imdata
import scripts.generatecode as gc 

# tkMessageBox.showinfo("Python command","人生苦短、我用Python")

reload(sys)
sys.setdefaultencoding('utf8')

svfile = ''

signals = {}

def StartGui():
    global val, root
    root = Tk()
    root.title('configration tool')
    root.geometry('800x600+100+20')

    vrms = VarSglMaps()

    inacfg = FileDeal(root, cbfunc = vrms.ImportData, inText = 'input acfg')
    inacfg.ConfigOpen('configuration for application', '.acfg', 'Open acfg')
    inacfg.pack()

    inhcfg = FileDeal(root, cbfunc = vrms.ImportData, inText = 'input hcfg')
    inhcfg.ConfigOpen('configuration for hardware', '.hcfg', 'Open hcfg')
    inhcfg.pack() 

    indbc = FileDeal(root, cbfunc = vrms.ImportData, inText = 'input dbc')
    indbc.ConfigOpen('data for can', '.dbc', 'Open dbc')
    indbc.pack()

    geneBtn = Button(root, text = "generate code", command = vrms.GenerateCode)
    geneBtn.pack()

    # sssss = SignalMap(root)
    # sssss.pack()

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

class SignalMap(object):
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

# class VarSglMap:
#     def __init__(self, varName):
#         self._var = varName
#         self._signal = None

#     def AddSignal(self, sglName):
#         self._signal = sglName

class VarSglMaps(object):
    def __init__(self):
        self._mapList = []
        self._dbc = None
        self._cb1Item = []
        self._svm = None
        self._code = ''

    def AddMap(self, vsm):
        self._mapList.append(vsm)

    def ImportVar(self, infile):
        f = open(infile, 'rb')
        data = json.loads(f.read())
        varNum = 0
        for vs in data:
            varNum += 1
            sm = SignalMap(root, varNum, data[vs], vs)
            self._mapList.append(sm)
            sm.pack()

    def ImportData(self, infile):
        if infile[-3:] == 'dbc':
            self.ImportDbc(infile)
            self._dbcUpdataFlag = True
        elif infile[-4:] == 'acfg':
            self.ImportVar(infile)
            global svfile
            svfile = infile[:-5] + '.sv'
            # print svfile
        elif infile[-4:] == 'hcfg':
            self.ImportHcfg(infile)
        else:
            print 'unknown file type'

        if self._mapList:
            for sm in self._mapList:
                sm._combo1['value'] = signals.keys()

    def ImportHcfg(self, infile):
        f = open(infile, 'rb')
        data = json.loads(f.read())
        signals['Hareware IO'] = data

    def ImportDbc(self, infile):
        self._dbc = imdata.importDBC(infile)
        signals['CAN signal'] = self._dbc.getSignals()

    def ImportSv(self, infile):
        self._svm = imdata.importSV(infile)

    def GetMapList(self):
        relist = []
        if self._mapList:
            for sm in self._mapList:
                data = sm.GetMap()
                if data:
                    relist.append(data)
            # print relist
            return relist
        else:
            return None 

    def GenerateCode(self):
        relist = self.GetMapList()
        if relist:
            errstr = ''
            for svm in relist:
                if svm[2] == None:
                    errstr += '\n' + str(svm[0]) + '. ' + svm[1]
            if errstr != '':
                tkMessageBox.showinfo('error', '以下参数未完成配置：%s' % errstr)
            else:
                global svfile
                tmpfile = svfile[:-3] + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + svfile[-3:]
                # svfile = svfile[:-3] + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + svfile[-3:]
                # print svfile
                self.WriteSvFile(relist, tmpfile)
                self.ImportSv(tmpfile)
                self._code = gc.GenerateCode(self._dbc, self._svm)
                print self._code
        else:
            tkMessageBox.showinfo("error","请选择App Config文件")

    def WriteSvFile(self, svlist, wfile):
        try:
            f = open(wfile, 'w')
            if svlist:
                wstr = ''
                for item in svlist:
                    wstr += item[3] + ', ' + item[1] + ', ' + item[4] + '\n'
                f.write(wstr)
                f.close()
                print 'success write sv file' 
        except Exception, e:
            print Exception,":",e           

if __name__ == '__main__':
    StartGui()