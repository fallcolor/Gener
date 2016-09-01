
''' A class for a source file.
    sourcefile:
      |- file head
      |- include
      |- type define
      |- macor define
      |- global variable (static or extern)
      |- function declare (static or extern)
      |- variable declare
      |- function
'''
import time

commentSgl = '//'

class CommentStr(object):
    def __init__(self, commStr = None):
        self._str = commStr
    def GetStr(self):
        return '// ' + self._str

class FileHead(object):
    def __init__(self, filename = '', author = 'pk', descrip = ''):
        self._filename = filename
        self._author = author
        self._time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self._descrip = descrip
    def AddProperty(self, filename = '', author = 'pk', descrip = ''):
        self._filename = filename
        self._author = author
        self._descrip = descrip
    def GetList(self):
        tmplist = []
        tmplist.append(CommentStr('file name   : ' + self._filename).GetStr())
        tmplist.append(CommentStr('author      : ' + self._author).GetStr())
        tmplist.append(CommentStr('time        : ' + self._time).GetStr())
        tmplist.append(CommentStr('description : ' + self._descrip).GetStr())
        return tmplist

class FileInclud(object):
    def __init__(self, filelist = []):
        self._filelist = filelist
        self._comment = CommentStr('files include')
    def AddProperty(self, filelist):
        self._filelist = filelist
    def GetList(self):
        tmplist = []
        tmplist.append(self._comment.GetStr())
        if self._filelist:
            for fl in self._filelist:
                tmplist.append('#include ' + '"' + fl + '"')
        return tmplist

class FuncEle(object):
    def __init__(self, elecomment = ['element comment'], elebody = []):
        self._elecomm = elecomment
        self._elebody = elebody
    def AddComment(self, comm):
        self._elecomm = comm 
    def AddBody(self,bd):
        self._elebody = bd
    def GetList(self, inden = 4):
        tmplist = []
        for li in self._elecomm:
            tmplist.append(' ' * inden + '// ' + li)
        if self._elebody:
            for li in self._elebody:
                tmplist.append(' ' * inden + li)
        tmplist[-1] += '\n'
        return tmplist

class FuncBody(object):
    def __init__(self, para = 'void', retype = 'void', reval = '', called = False, declare = False):
        self._para = para
        self._eles = []
        self._retype = retype
        self._reVal = reval
        self._called = called
        self._declare = declare
        self._comment = ''
        self._name = ''

    def AddFuncName(self, name):
        self._name = name
    def AddFuncComment(self, commstr):
        self._comment = CommentStr(commstr).GetStr()
    def AddFuncPara(self, Arg):        
        self._para = Arg
    def AddFuncEle(self, ele):
        self._eles.append(ele)
    def CopyFromAnother(self, func):
        self._para = func._para
        self._eles = func._eles
        self._retype = func._retype
        self._reVal = func._reVal
        self._called = func._called
        self._declare = func._declare
        self._comment = func._comment
        self._name = func._name
        self._eles = func._eles
    def GetList(self, inden = 4):
        if self._declare:
            return self.GetDeclareList()

        if self._called:
            return self.GetCalledList()
        else:
            return self.GetNotCalledList()
    def GetNotCalledList(self, inden = 4):
        tmplist = []
        # function comment
        tmplist.append(self._comment)
        # function name
        tmplist.append(self._retype + ' ' + self._name + '(' + self._para + ')')
        tmplist.append('{')
        # function elements
        for li in self._eles:
            tmplist.extend(li.GetList(inden))
        if len(self._eles) > 0:
            tmplist[-1] = tmplist[-1][:-1]  # delete the last '\n'
        # function end
        tmplist.append('}')
        return tmplist
    def GetCalledList(self, inden = 4):
        tmplist = []
        tmplist.append(' ' * inden + self._comment)
        tmpstr = ''
        if self._reVal != '':
            tmpstr += self._reVal + ' '
        tmpstr += self._name + '(' + self._para + ');\n'
        tmplist.append(' ' * inden + tmpstr)
        return tmplist
    def GetDeclareList(self):
        tmplist = []
        tmplist.append(self._comment)
        tmpstr = 'extern '
        if self._retype != '':
            tmpstr += self._retype + ' '
        tmpstr += self._name + '(' + self._para + ');'
        tmplist.append(tmpstr)
        return tmplist

class SourceFile(object):
    def __init__(self, declare = False):
        self._indentationNum = 4    
        self._filehead = FileHead()
        self._fileinclude = FileInclud()
        self._funclist = []
        self._declare = declare
        self._filename = ''
    def AddFilehead(self, filename = '', author = 'pk', descrip = ''):
        self._filename = filename
        self._filehead.AddProperty(filename, author, descrip)
    def AddFileInclude(self, filelist):
        self._fileinclude.AddProperty(filelist)
    def AddFunc(self, func):
        self._funclist.append(func)
    def GetStr(self):
        tmplist = self._filename.upper().split('.')
        fn = '_'.join(tmplist) + '_'
        tmpstr = ''
        # file head
        tmpstr += '\n'.join(self._filehead.GetList()) + '\n\n'
        # anti redefine
        if self._declare:
            tmpstr += '#ifndef %s\n#define %s\n\n' % (fn, fn)
        # file include
        if len(self._fileinclude.GetList()) > 1:
            # list[0] is comment
            tmpstr += '\n'.join(self._fileinclude.GetList()) + '\n\n'
        # functions
        for func in self._funclist:
            tmpstr += '\n'.join(func.GetList(self._indentationNum)) + '\n\n'
        # anti redefine
        if self._declare:
            tmpstr += '#endif  // #ifndef %s\n' % fn
        # file end
        tmpstr += '// file end: ' + self._filehead._filename
        return tmpstr

def test():
    import CanCode as cc
    sf = SourceFile()
    sf.AddFilehead('main.c','pk','ok')
    sf.AddFileInclude(['stdio.h', 'math.h'])

    fd = FuncBody(declare = True, retype = 'int')
    fd.AddFuncComment('fd')
    fd.AddFuncName('func_declare')
    fd.AddFuncPara('sdfsf, ifef, ds9ff')
    sf.AddFunc(fd)

    f0 = FuncBody(called = True)
    f0.AddFuncComment('f0')
    f0.AddFuncName('initsdfsdf')
    f0.AddFuncPara('sdfsf, ifef, ds9ff')

    f1 = FuncBody()
    f1.AddFuncComment('f1')
    f1.AddFuncName('unpack0x1313FF01')
    f1.AddFuncPara('char* data, int num')
    f1.AddFuncEle(FuncEle(['temp variable'], ['uint32_T utmp;','int32_T itmp;']))
    f1.AddFuncEle(FuncEle(['signalname', 'startbit','leng'], ['busvolt = data[0];']))
    f1.AddFuncEle(f0)
    sf.AddFunc(f1)

    f2 = FuncBody()
    f2.AddFuncComment('f2')
    f2.AddFuncName('unpack0x1313FF01')
    f2.AddFuncPara('char* data, int num')
    f2.AddFuncEle(FuncEle(['temp variable'], ['uint32_T utmp;','int32_T itmp;']))
    f2.AddFuncEle(FuncEle(cc.GetSignalComm('bat', 'BAT..', 20, 16, 0.1, -40), cc.UnpackSignal('bat', 'int', 'data', 20, 16, 0.1, -40)))
    sf.AddFunc(f2)
    print len(sf._funclist)
    print sf.GetStr()

if __name__ == '__main__':
    test()