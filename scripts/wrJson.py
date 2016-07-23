import json

from canmatrix import *
from ImportData import *

re = {"CANmessage" : {}, "HardwareIO" : {}}
jsonFile = r'e:/jn.json'
# db = importDBC(dbcFile)

def writeJson(dbcFile, jsonFile):
    db = importDBC(dbcFile)
    
    for fr in db._fl._list:
        istrans = False
        sglList = []
        
        if "VCU" in fr._Transmitter:
            istrans = True
        for sgl in fr._signals:
            sglList.append(sgl._name)
        # re["CANmessage"]["%s" % fr._Id] = {"name": "%s"%fr._name, "transmit": "%s"%istrans, "signal": sglList}
        re["CANmessage"][fr._Id] = {"name": fr._name, "transmit": istrans, "signal": sglList}

    try:
        fi = open(jsonFile, 'w')
        fi.write(json.dumps(re, indent = 2))
        fi.close()
        print 'success for generated json file!'
    except Exception, e:
        print Exception,":",e

def test():
    writeJson(dbcFile, jsonFile)
    # print json.dumps(re, indent = 2)

if __name__ == '__main__':
    test()
