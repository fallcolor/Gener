#! python2

from canmatrix import *
from svmatrix import *
import re
import os

dbcFile = r'e:/ks.dbc'
# dbcFile = r'/Users/caopengkun/python/Gener/ks.dbc'
dbcImportEncoding='iso-8859-1'

svFile = r'e:/ks.sv'
# svFile = r'/Users/caopengkun/python/Gener/ks.sv'

def importDBC(filename):

    i = 0
    db = CanMatrix()

    f = open(filename, 'rb')
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
                db._fl.addFrame(Frame(temp.group(1), temp.group(2), temp.group(3), temp.group(4)))
            else:
                regexp = re.compile("^BO\_ (\w+) (\w+) *: (\w+)")
                temp = regexp.match(decoded)
                db._fl.addFrame(Frame(temp.group(1), temp.group(2), temp.group(3), None))
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
                tempSig = Signal(temp.group(1), temp.group(2), temp.group(3), temp.group(4), temp.group(5), temp.group(6), temp.group(7),temp.group(8),temp.group(9),temp_raw.group(10).decode(dbcImportEncoding),reciever)     
                if tempSig._byteorder == 0:
                    # startbit of motorola coded signals are MSB in dbc
                    tempSig.setMsbStartbit(int(temp.group(2)))                
                db._fl.addSignalToLastFrame(tempSig)
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

                db._fl.addSignalToLastFrame(Signal(temp.group(1), temp.group(3), temp.group(4), temp.group(5), temp.group(6), temp.group(7),temp.group(8),temp.group(9),temp.group(10),temp_raw.group(11).decode(dbcImportEncoding),reciever, multiplex))
            # print temp.group(1),temp.group(2),temp.group(3)

    for bo in db._fl._list:
        if bo._Id > 0x80000000:
            bo._Id -= 0x80000000
            bo._extended = 1
    return db

def importSV(filename):
    db = SvMatrix()
    f = open(filename, 'rb')
    for line in f:
        l = line.strip()
        if l.__len__() == 0:
            continue
        temp = l.split(',')
        if temp.__len__() == 3:
            db.addMap(temp[0].strip(), temp[1].strip(), temp[2].strip())
        else:
            db.addMap(temp[0].strip(), temp[1].strip(), None)

    return db


def printDbc(db):
    for bo in db._fl._list:
        print bo._Id, bo._name, bo._Transmitter
        for sgl in bo._signals:
            print sgl._name, sgl._startbit

def printSv(db):
    for sv in db._list:
        print sv._signal, sv._value, sv._type


def test():
    #printDbc(importDBC(dbcFile))
    printSv(importSV(svFile))
    # print svFile

if __name__ == '__main__':
    test()
