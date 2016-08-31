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
    cname = mc._svfname[:-2] + 'c'
    cname = cname.split('/')[-1]
    hname = mc._svfname[:-2] + 'h'
    hname = hname.split('/')[-1]
    cfile.AddFilehead(cname, 'pk', 'source file for CAN message init and signal task')
    hfile.AddFilehead(hname, 'pk', 'head file for CAN message init and signal task')

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
        transstr = ', '.join(fr._Transmitter)

        tmpstr = 'can message: ID = %s, Trans ECU(s) is(are): %s'
        func.AddFuncComment(tmpstr % (fr._Id, transstr))
        if transflag == 1:
            func.AddFuncName('pack_%s' % fr._Id)
        else:
            func.AddFuncName('unpack_%s' % fr._Id)
        func.AddFuncPara('char* data')
        func.AddFuncEle(fc.FuncEle(['temp variable'], ['uint32_T tmpValue;']))
        # add signal
        for sgl in fr._signals:
            sglmaps = mc.GetMaps(sgl._name)
            for sm in sglmaps:
                comlist = cc.GetSignalComm(sm[0], sm[2].split(' ')[0], sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)
                if transflag == 1:
                    bodylist = cc.PackSignal(sm[0], sm[1], 'data', sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)
                else:
                    bodylist = cc.UnpackSignal(sm[0], sm[1], 'data', sgl._startbit, sgl._signalsize, sgl._factor, sgl._offset)                   
                func.AddFuncEle(fc.FuncEle(comlist, bodylist))
        
        if len(func._eles) > 1:
            cfile.AddFunc(func)
    return cfile.GetStr(), hfile.GetStr()

def test():
    import ConfigClass as cc
    mc = cc.MapConfig()
    mc.AddDbcFromFile(r'E:\pyproj\gener\test\ks.dbc')
    mc.ImportFromFile(r'E:\pyproj\gener\test\kk.sv')
    print mc._ecu
    print GenerateCanCode(mc)


if __name__ == '__main__':
    test()
