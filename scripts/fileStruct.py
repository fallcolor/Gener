
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
indentationNum = 4

class CommentStr(object):
    ''' class for comment
        _strlist: one-row comment without '// ' is an element of the string list

        GetStr: gain the list of comment with '// '
    '''
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
    def GetStr(self):
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
    def GetStr(self):
        tmplist = []
        tmplist.append(self._comment.GetStr())
        if self._filelist:
            for fl in self._filelist:
                tmplist.append('#include ' + '"' + fl + '"')
        return tmplist

class FuncBody(object):
    def __init__(self):
        

class SourceFile(object):
    def __init__(self):
        self._filehead = FileHead()
        self._fileinclude = FileInclud()
    def AddFilehead(self, filename = '', author = 'pk', descrip = ''):
        self._filehead.AddProperty(filename, author, descrip)
    def AddFileInclude(self, filelist):
        self._fileinclude.AddProperty(filelist)
    def GetStr(self):
        tmpstr = ''
        for li in self._filehead.GetStr():
            tmpstr += li + '\n'
        tmpstr += '\n'
        for li in self._fileinclude.GetStr():
            tmpstr += li + '\n'
        return tmpstr

def test():
    # fh = FileHead('sdfsdf.c', 'pk', 'sdfsdfsdfsdfsdf')
    # for li in fh.GetStr():
    #     print li

    # fi1 = FileInclud()
    # for li in fi1.GetStr():
    #     print li
    # fi2 = FileInclud(['asdf.h', 'sfwef.h'])
    # for li in fi2.GetStr():
    #     print li

    sf = SourceFile()
    sf.AddFilehead('main.c','pk','ok')
    sf.AddFileInclude(['stdio.h', 'math.h'])
    print sf.GetStr()

if __name__ == '__main__':
    test()