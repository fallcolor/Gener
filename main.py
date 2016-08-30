import sys
import time

# griphic interface
from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

# user module
import scripts.ConfigClass as cc
import scripts.UserControl as uc
import scripts.GenerateCanCode as gcc

reload(sys)
sys.setdefaultencoding('utf8')

def StartGui():
    global val, root, nb, msgFrame, sglFrame, mc, dbc, hc, outsv
    root = Tk()
    root.title('configration tool')
    root.geometry('800x600+100+20')

    mc = cc.MapConfig()
    # dbc = cc.CanConfig()
    # hc = cc.HwConfig()

    nb = ttk.Notebook(root)
    nb.bind('<<NotebookTabChanged>>', NoteBookSelected)
    msgFrame = uc.MessageFrameControl(nb, height = 20, width = 30)
    sglFrame = uc.SignalFrameControl(nb, height = 20, width = 30)
    nb.add(msgFrame, text = 'Basic config')
    nb.add(sglFrame, text = 'Signal Map')
    mc.AddDisplayFunc(DisplayFunc)

    # message frmae


    # signal frame
    # mc.AddDisplayFunc(sglFrame.Refresh)

    inacfg = uc.FileDealControl(root, cbfunc = mc.AddVarsFrmoFile, inText = 'input ac file')
    inacfg.ConfigOpen('configuration for application', '.ac', 'Open acfg')
    inacfg.pack()

    inhcfg = uc.FileDealControl(root, inText = 'input hc file')
    inhcfg.ConfigOpen('configuration for hardware', '.hc', 'Open hcfg')
    inhcfg.pack()

    indbc = uc.FileDealControl(root, cbfunc = mc.AddDbcFromFile, inText = 'input dbc file')
    indbc.ConfigOpen('data for can', '.dbc', 'Open dbc')
    indbc.pack()

    insv = uc.FileDealControl(root, cbfunc = mc.ImportFromFile, inText = 'input sv file')
    insv.ConfigOpen('data for sv', '.sv', 'Open sv')
    insv.pack()

    outsv = uc.FileDealControl(root, cbfunc = mc.ExportToFile, inText = 'Output sv file', save = True)
    outsv.ConfigOpen('data for sv', '.sv', 'Save sv')
    outsv.pack()

    fr = Frame(root)
    fr.pack(fill = X)
    saveBtn = Button(fr, text = "save config", command = SaveData)
    saveBtn.pack(side = LEFT)
    geneBtn = Button(fr, text = "generate code", command = GenerateCode)
    geneBtn.pack(side = LEFT)

    nb.pack(fill = BOTH, expand = 1, side = BOTTOM)
    
    root.mainloop()

def NoteBookSelected(e = None):
    # save current data
    SaveData()
    # refresh display
    DisplayFunc(mc)

def DisplayFunc(mc):
    # refresh display
    sglFrame.Refresh(mc)
    msgFrame.Refresh(mc)

def SaveData():
    ecuchks, msgcfgs = msgFrame.GetValue()
    sglmaps = sglFrame.GetValue()
    # print 'main cfg: ', msgcfgs
    mc.ChangeFromFrame(ecuchks, mc._cancfg, msgcfgs, sglmaps)
    # print 'main mc: ', [[fr._Id, fr._checked] for fr in mc._dbc._fl._list]

def ipdbc(infile):
    mc.AddDbcFromFile(infile)
    dbc.ImportFromFile(infile)

def GenerateCode():
    SaveData()
    tmpstr = ''
    print len(mc._dbc._fl._list)
    mcstate, errmsg = mc.CheckSelf()
    if mcstate:
        tmpstr = gcc.GenerateCanCode(mc._dbc, mc, mc.GetTransEcu())
        print tmpstr
    else:
        tkMessageBox.showinfo("Error", errmsg)


if __name__ == '__main__':
    StartGui()