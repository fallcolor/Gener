'''
GenerateCanCode.py
2016.08.24

Generate CAN code, including both .c and .h

'''

import CanCode as cc
import FileClass as fc


def GenerateCanCode(mc):
    cfile = fc.SourceFile()
    hfile = fc.SourceFile()
    for fr in mc._dbc._fl._list:
        transflag = 0
        func = fc.FuncBody()
        # there's no map of signal and variable 
        if len(mc._maps) == 0:
            break

        # whether it is a transmit frame
        eculist = mc.GetTransEcu()
        for ecu in eculist:
            if ecu in fr._Transmitter:
                transflag = 1
                break
        transstr = ''
        for tran in fr._Transmitter:
            transstr += ', ' + tran
        # if transflag == 1:  # transmit frame            
        tmpstr = 'can message: ID = 0x%s, Trans ECU(s) is(are): %s'
        func.AddFuncComment(tmpstr % (fr._Id, transstr))
        if transflag == 1:
            func.AddFuncName('pack_0x%s' % fr._Id)
        else:
            func.AddFuncName('unpack_0x%s' % fr._Id)
        func.AddFuncPara('char* data')
        func.AddFuncEle(fc.FuncEle(['temp variable'], ['uint32_T tmpValue;']))
        # add signal
        for sgl in fr._signals:
            sglmaps = mc.GetMaps(sgl._name)
            for sm in sglmaps:
                comlist = cc.GetSignalComm(sm[0], sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)
                if transflag == 1:
                    bodylist = cc.PackSignal(sm[0], sm[1], 'data', sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)
                else:
                    bodylist = cc.UnpackSignal(sm[0], sm[1], 'data', sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)                   
                func.AddFuncEle(fc.FuncEle(comlist, bodylist))

        if len(func._eles) > 1:
            cfile.AddFunc(func)
    return cfile.GetStr()

def test():
    import ConfigClass as cc
    mc = cc.MapConfig()
    mc.ImportFromFile(r'E:\pyproj\gener\test\kk.sv')
    mc.AddDbcFromFile(r'E:\pyproj\gener\test\ks.dbc')
    print mc._ecu
    print GenerateCanCode(mc)


if __name__ == '__main__':
    test()
