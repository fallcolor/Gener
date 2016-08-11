'''
CanCode.py
2016.08.09

pack and unpack can signal

interface function, they all return a list:
    GetSignalComm()
    PackSignal()
    UnpackSignal()

'''

from math import pow

def GetSignalComm(sglName, startbit, length, factor, offset):
    relist = []
    relist.append('value name : %s' % sglName)
    relist.append('start bit  : %s' % startbit)
    relist.append('length     : %s' % length)
    relist.append('factor     : %s' % factor)
    relist.append('offset     : %s' % offset)
    return relist

def PackSignal(sglName, sglType, dataStr, startbit, length, factor, offset):
    ''' return a list of pack can signal code, each line is an element of the list
    '''
    _length = length
    _startbit = startbit
    relist = ['tmpValue = (uint32_T)((%s - %s) / %s);' % (sglName, offset, factor)]
    if startbit + length > 64:
        return ['// Error: length of signal out of range']

    # string like  data[x1] = (sgl & 'x2') >> x3 << x4
    x1 = 0
    x2 = ''
    x3 = 0
    x4 = 0
    packedlen = 0
    while _length > 0:    
        tmpstr = ''
        if (_startbit % 8) + _length > 8:
            curLen = 8 - (_startbit % 8)
            x1 = _startbit / 8
            x2 = GetPackBitField(packedlen, (curLen + packedlen))
            x3 = packedlen
            x4 = _startbit % 8
            tmpstr += GetPackStr(dataStr, x1, x2, x3, x4)
            _startbit += curLen
            _length -= curLen
            packedlen += curLen
        else:
            x1 = _startbit / 8
            if length == 8 and (startbit % 8) == 0:
                x2 = ''
            else:
                x2 = GetPackBitField(packedlen, length)
            # print x2
            x3 = packedlen
            x4 = _startbit % 8   
            tmpstr += GetPackStr(dataStr, x1, x2, x3, x4)
            _length = 0
        relist.append(tmpstr)
    return relist

def GetPackStr(dataStr, x1, x2, x3, x4):
    # string like  data[x1] = (sgl & 'x2') >> x3 << x4
    restr = 'tmpValue'
    if x2 != '':
        restr += ' & %s' % x2
    if x3 != 0:
        restr = '(' + restr + ') >> %d' % x3
    if x4 != 0:
        restr = '(' + restr + ') << %d' % x4
    restr = 'data[%d] += ' % x1 + restr + ';'
    return restr

def GetPackBitField(packedlen, length):
    re = pow(2, length) - pow(2, packedlen)
    if re < 16:
        return '0x0' + '%X' % re
    return '0x' + '%X' % re

def UnpackSignal(sglName, sglType, dataStr, startbit, length, factor, offset):
    ''' return a list of unpack can signal code, each line is an element of the list
    '''
    _length = length
    _startbit = startbit
    relist = ['uint32_T tmpValue = 0;']
    if startbit + length > 64:
        return ['// Error: length of signal out of range']

    # string like  ((data[x1] & 'x2') >> x3) * x4
    x1 = 0
    x2 = '0xFF'
    x3 = 0
    x4 = 1  
    while _length > 0:    
        tmpstr = ''
        if (_startbit % 8) + _length > 8:
            curLen = 8 - (_startbit % 8)
            x1 = _startbit / 8
            x2 = GetUnpackBitField(_startbit % 8, curLen)
            x3 = _startbit % 8
            tmpstr += GetUnpackStr(dataStr, x1, x2, x3, x4)
            _startbit += curLen
            _length -= curLen
            x4 *= pow(2, curLen)
        else:
            x1 = _startbit / 8
            x2 = GetUnpackBitField(_startbit % 8, _length)
            x3 = _startbit % 8
            tmpstr += GetUnpackStr(dataStr, x1, x2, x3, x4)
            _length = 0
        tmpstr = 'tmpValue += ' + tmpstr + ';'
        relist.append(tmpstr)
    relist.append('%s = (%s)tempValue * %s + %s;' % (sglName, sglType, factor, offset))
    return relist

def GetUnpackStr(dataStr, x1, x2, x3, x4):
    # string like  ((data[x1] & 'x2') >> x3) * x4
    restr = ''
    restr = '%s[%d]' % (dataStr, x1)
    if x2 != '0xFF':
        restr = restr + ' & %s' % x2
        if x3 != 0:
            restr = '(' + restr +') >> %d' % x3
        if x4 != 1:
            restr = '(' + restr +') * %d' % x4
    else:
        if x3 != 0:
            restr = '(' + restr +') >> %d' % x3
        if x4 != 1:
            restr = restr +' * %d' % x4
    return restr

def GetUnpackBitField(startbit, length):
    ''' return a string like '0xFA'
    '''
    if startbit + length > 8:
        return '0xFF'

    _sb = startbit
    _len = 0
    re = 0;
    while _len < length:
        re += pow(2, _sb)
        _sb += 1
        _len += 1
    if re < 16:
        return '0x0' + '%X' % re
    return '0x' + '%X' % re


def test():
    print UnpackSignal('bat', 'int', 'data', 0, 8, 0.1, -40)
    print UnpackSignal('bat', 'int', 'data', 2, 1, 0.1, -40)
    print UnpackSignal('bat', 'int', 'data', 12, 3, 0.1, -40)
    print UnpackSignal('bat', 'int', 'data', 20, 16, 0.1, -40)
    # print PackSignal('bat', 'int', 'data', 20, 16, 0.1, -40)
    # print GetPackBitField(8, 16)
    # print PackSignal('bat', 'int', 'data', 0, 8, 0.1, -40)
    # print PackSignal('bat', 'int', 'data', 0, 22, 0.1, -40)
    # print PackSignal('bat', 'int', 'data', 8, 16, 0.1, -40)
    # print PackSignal('bat', 'int', 'data', 5, 2, 0.1, -40)
    # print PackSignal('bat', 'int', 'data', 4, 8, 0.1, -40)

if __name__ == '__main__':
    test()