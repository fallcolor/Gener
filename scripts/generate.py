#! python2

from math import pow
from ImportData import *

def WriteSglComment(startbit, length, factor, offset):
    strHe  = '    /* signal to var\n'
    strSt  = '       start bit : %s\n' % startbit
    strLen = '       length    : %s\n' % length
    strFac = '       factor    : %s\n' % factor
    strOff = '       offset    : %s\n' % offset
    return strHe + strSt + strLen + strFac + strOff + '     */'

def WriteUnpackSgl(sglName, sglType, dataStr, startbit, length, factor, offset):
    if startbit + length > 64:
        return 'Error: length of signal out of range'

    reStr = CalcSglValue(dataStr, startbit, length) + '\n'
    reStr += '    %s = (%s)tempValue * %s + %s;'%(sglName, sglType, factor, offset)

    return reStr

def CalcSglValue(dataStr, startbit, length):
    # sByte = startbit / 8
    # sBit  = startbit % 8

    CalcEff = (1, 3, 7, 15, 31, 63, 127, 255)

    # print '    tempValue =',
    # if sBit + length <= 8:
    #     print '((%s[%d] & %d) >> %d);'%(dataStr, sByte, CalcEff[sBit + length - 1], sBit)
    # else:
    #     print '    tempValue = tempValue + %d * ',
    #     CalcSglValue(dataStr, startbit - sBit + 8, sBit + length - 8)

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

#def unPackMsg()

def unPackSgl(sglName, sglType, dataStr, startbit, length, factor, offset):
    # test for signal unpack
    print WriteSglComment(startbit, length, factor, offset)
    print WriteUnpackSgl(sglName, sglType, dataStr, startbit, length, factor, offset)
    print ""

def test():
    unPackSgl('busVolt', 'float', 'data', 0, 16, 0.1, -100)
    unPackSgl('busCurr', 'int', 'data', 24, 24, 0.1, -3200)

if __name__ == '__main__':
    test()
