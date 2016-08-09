#! python2

from math import pow
from ImportData import *

def GetSglCommStr(sglName, startbit, length, factor, offset):
    strHe  = '    /* value name : %s\n' % sglName
    strSt  = '       start bit  : %s\n' % startbit
    strLen = '       length     : %s\n' % length
    strFac = '       factor     : %s\n' % factor
    strOff = '       offset     : %s\n' % offset
    return strHe + strSt + strLen + strFac + strOff + '     */'

def GetUnpackSglStr(sglName, sglType, dataStr, startbit, length, factor, offset):
    if startbit + length > 64:
        return 'Error: length of signal out of range'

    reStr = CalcSglValue(dataStr, startbit, length) + '\n'
    reStr += '    %s = (%s)tempValue * %s + %s;'%(sglName, sglType, factor, offset)

    return reStr

def CalcSglValue(dataStr, startbit, length):

    CalcEff = (1, 3, 7, 15, 31, 63, 127, 255)
    
    if (startbit % 8) + length > 8:
        HiBit  = startbit + length
        HiByte = HiBit / 8
        if HiBit % 8 == 0:
            strHighByte = '    tempValue += %s[%d] * %d;' % (dataStr, HiByte - 1, pow(2, length - 8))
            return CalcSglValue(dataStr, startbit, length - 8) +'\n' + strHighByte
        else:
            strHighByte = '    tempValue += (%s[%d] & %d) * %d;' \
                % (dataStr, HiByte, CalcEff[HiBit % 8 - 1], pow(2, length - (HiBit % 8)))

            return CalcSglValue(dataStr, startbit, length - (HiBit % 8)) + '\n' + strHighByte
    else: 
        sByte = startbit / 8
        sBit  = startbit % 8
        if sBit == 0:
            return '    tempValue = %s[%d];' % (dataStr, sByte)
        else:
            return '    tempValue = (%s[%d] & %d) >> %d;' \
                % (dataStr, sByte, CalcEff[sBit + length - 1], sBit)

def GetUnpackCommStr(MsgId):
    strCom = '// unpack can message: ID = 0x%X' % MsgId
    return strCom

def GetUnpackMsgNameStr(MsgId):
    strHead = 'void Unpack_0x%X(void)' % MsgId
    return strHead

def GetUnpackMsgHeadStr(MsgId):
    strHead = GetUnpackMsgNameStr(MsgId) + '\n{\n    uint32_T tempValue = 0;'
    return strHead

def GetUnpackMsgFootStr(MsgId):
    strFoot = '}'
    return strFoot

def unPackSgl(sglName, sglType, dataStr, startbit, length, factor, offset):
    # test for signal unpack
    print GetSglCommStr(sglName, startbit, length, factor, offset)
    print GetUnpackSglStr(sglName, sglType, dataStr, startbit, length, factor, offset)
    print ""

def unPackMsg(MsgId):
    print GetUnpackCommStr(MsgId)
    print GetUnpackMsgHeadStr(MsgId)
    print GetUnpackMsgFootStr(MsgId)

def test():
    print GetUnpackCommStr(123)
    print GetUnpackMsgHeadStr(123)
    unPackSgl('busVolt', 'float', 'data', 0, 16, 0.1, -100)
    unPackSgl('busCurr', 'int', 'data', 24, 24, 0.1, -3200)
    print GetUnpackMsgFootStr(123)

if __name__ == '__main__':
    test()
