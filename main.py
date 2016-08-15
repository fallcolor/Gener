import sys
import time

# griphic interface
from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

# user module
import scripts.ConfigClass as cc

reload(sys)
sys.setdefaultencoding('utf8')

def StartGui():
    global val, root, nb, msgFrame, sglFrame
    root = Tk()
    root.title('configration tool')
    root.geometry('800x600+100+20')

    nb = ttk.Notebook(root)
    msgFrame = LabelFrame(nb, height = 20, width = 30)
    sglFrame = LabelFrame(nb, height = 20, width = 30)
    nb.add(msgFrame, text = 'Basic config')
    nb.add(sglFrame, text = 'Signa. Map')

    inacfg = FileDeal(root, inText = 'input ac file')
    inacfg.ConfigOpen('configuration for application', '.ac', 'Open acfg')
    inacfg.pack()

    inhcfg = FileDeal(root, inText = 'input hc file')
    inhcfg.ConfigOpen('configuration for hardware', '.hc', 'Open hcfg')
    inhcfg.pack()

    indbc = FileDeal(root, inText = 'input dbc file')
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

if __name__ == '__main__':
    StartGui()