
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
        tmplist.append(CommentStr('file name   :' + self._filename).GetStr())
        tmplist.append(CommentStr('author      :' + self._author).GetStr())
        tmplist.append(CommentStr('time        :' + self._time).GetStr())
        tmplist.append(CommentStr('description :' + self._descrip).GetStr())
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
    def __init__(self):
        self._para = 'void'
        self._eles = []
    def AddFuncName(self, name):
        self._name = name
    def AddFuncComment(self, commstr):
        self._comment = CommentStr(commstr).GetStr()
    def AddFuncPara(self, Arg):        
        self._para = Arg
    def AddFuncEle(self, ele):
        self._eles.append(ele)
    def GetList(self, inden = 4):
        tmplist = []
        # function comment
        tmplist.append(self._comment)
        # function name
        tmplist.append('void ' + self._name + '(' + self._para + ')')
        tmplist.append('{')
        # function elements
        for li in self._eles:
            tmplist.extend(li.GetList(inden))
        tmplist[-1] = tmplist[-1][:-1]  # delete the last '\n'
        # function end
        tmplist.append('}')
        return tmplist

class SourceFile(object):
    def __init__(self):
        self._indentationNum = 4    
        self._filehead = FileHead()
        self._fileinclude = FileInclud()
        self._funclist = []
    def AddFilehead(self, filename = '', author = 'pk', descrip = ''):
        self._filehead.AddProperty(filename, author, descrip)
    def AddFileInclude(self, filelist):
        self._fileinclude.AddProperty(filelist)
    def AddFunc(self, func):
        self._funclist.append(func)
    def GetStr(self):
        tmpstr = ''
        # file head
        tmpstr += '\n'.join(self._filehead.GetList()) + '\n\n'
        # file include
        tmpstr += '\n'.join(self._fileinclude.GetList()) + '\n\n'
        # functions
        for func in self._funclist:
<<<<<<< HEAD
            tmpstr += '\n'.join(func.GetStr(self._indentationNum)) + '\n\n'
=======
            tmpstr += '\n'.join(func.GetList(self._indentationNum)) + '\n\n'

>>>>>>> f9a19edf2751141b2379e7e153549a1e42aefab5
        # file end
        tmpstr += '// file end: ' + self._filehead._filename
        return tmpstr

def test():
    sf = SourceFile()
    sf.AddFilehead('main.c','pk','ok')
    sf.AddFileInclude(['stdio.h', 'math.h'])

    f1 = FuncBody()
    f1.AddFuncComment('f1')
    f1.AddFuncName('unpack0x1313FF01')
    f1.AddFuncPara('char* data, int num')
    f1.AddFuncEle(FuncEle(['temp variable'], ['uint32_T utmp;','int32_T itmp;']))
    f1.AddFuncEle(FuncEle(['signalname', 'startbit','leng'], ['busvolt = data[0];']))
    sf.AddFunc(f1)

    f2 = FuncBody()
    f2.AddFuncComment('f2')
    f2.AddFuncName('unpack0x1313FF01')
    f2.AddFuncPara('char* data, int num')
    f2.AddFuncEle(FuncEle(['temp variable'], ['uint32_T utmp;','int32_T itmp;']))
    f2.AddFuncEle(FuncEle(['signalname', 'startbit','leng'], ['busvolt = data[0];']))
    sf.AddFunc(f2)

    print sf.GetStr()

if __name__ == '__main__':
    test()