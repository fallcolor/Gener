'''
CanCode.py
2016.08.09

pack and unpack can signal

'''

import math

def UnpackSignal(outlist, sglName, sglType, dataStr, startbit, length, factor, offset):
    ''' return a list of unpack can signal code, each line is an element of the list
    '''
    if startbit + length > 64:
        return ['// Error: length of signal out of range']

    CalcUnpackSgl(outlist, dataStr, startbit, length)
    outlist.append('%s = (%s)tempValue * %s + %s;'%(sglName, sglType, factor, offset))

def CalcUnpackSgl(outlist, dataStr, startbit, length):
    # bit field operation flag
    CalcEff = (1, 3, 7, 15, 31, 63, 127, 255)

    if (startbit % 8) + length > 8:
        HiBit  = startbit + length
        HiByte = HiBit / 8
        if HiBit % 8 == 0:
            CalcUnpackSgl(outlist, dataStr, startbit, length - 8)
            outlist.append('tempValue += %s[%d] * %d;' % (dataStr, HiByte - 1, pow(2, length - 8)))
        else:
            CalcUnpackSgl(outlist, dataStr, startbit, length - (HiBit % 8))
            outlist.append('tempValue += (%s[%d] & %d) * %d;' \
                % (dataStr, HiByte, CalcEff[HiBit % 8 - 1], pow(2, length - (HiBit % 8))))
    else: 
        sByte = startbit / 8
        sBit  = startbit % 8
        print sBit
        if sBit == 0:
            outlist.append('tempValue = %s[%d];' % (dataStr, sByte))
        else:
            outlist.append('tempValue = (%s[%d] & %d) >> %d;' \
                % (dataStr, sByte, CalcEff[sBit + length - 1], sBit))


def test():
    ol = []
    UnpackSignal(ol, 'bat', 'int', 'data', 0, 6, 0.1, -40)
    print ol
    ol = []
    UnpackSignal(ol, 'bat', 'int', 'data', 0, 16, 0.1, -40)
    print ol

if __name__ == '__main__':
    test()