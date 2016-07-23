# -*- coding: UTF-8 -*-

from Tkinter import *
import tkFileDialog

import json

# app variables
appVar = []

varLabel = []



root = Tk()
acfgPathLabel = Label(root, text ='acfg file path: ')
dbcPathLabel = Label(root, text ='dbc file path: ')
hcfgPathLabel = Label(root, text ='hcfg file path: ')

def fileOption(filetype, suffix, title):
    '''option for file dialog
    '''
    OpenOption = {}
    OpenOption['defaultextension'] = suffix
    OpenOption['filetypes'] = [(filetype, suffix), ('all files', '.*')]
    # OpenOption['initialdir'] = 'e:\\'
    # OpenOption['initialfile'] = 'myfile.acfg'
    OpenOption['parent'] = root
    # OpenOption['multiple'] = 1
    OpenOption['title'] = title
    return OpenOption

def OpenAcfg():
    # open app config file
    OpenOption = fileOption('app config', '.acfg', 'Open app configuration')

    f = tkFileDialog.askopenfile(mode = 'r', **OpenOption)
    
    if f:
        acfgPathLabel['text'] += f.name
        data = json.loads(f.read())
        for vari in data['var']:
            appVar.append(vari)
        print appVar
    else:
        messagebox.showinfo(title = 'error', message = 'Open app config file failed')

def OpenDbc():
    # open dbc file
    OpenOption = fileOption('CAN database', '.dbc', 'Open CAN database')

    f = tkFileDialog.askopenfile(mode = 'r', **OpenOption)
    
    if f:
        dbcPathLabel['text'] += f.name
        print f.read()
    else:
        messagebox.showinfo(title = 'error', message = 'Open dbc file failed')
    

def OpenHcfg():
    print "OpenHcfg"  

Button(root, text = 'Open .acfg', command = OpenAcfg).pack() 
acfgPathLabel.pack()
Button(root, text = 'Open .dbc', command = OpenDbc).pack()
dbcPathLabel.pack()
Button(root, text = 'Open .hcfg', command = OpenHcfg).pack()
hcfgPathLabel.pack()

root.mainloop()

if __name__ == '__main__':
    start_gui()