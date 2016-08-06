# CAN模块的自动代码生成（Python实现）（1）介绍

## 概述

2016.07.23

当前新能源汽车形势大好，商用车更是不得了，很多N年没出货的主机厂都复活了，恨不得明年的市场都圈过来。作为ECU供应商，面对各种恨不得刚签完合同就拿到货的要求，如在保证质量的前提下，尽快完成项目，服务好这么多衣食父母，就成了一个主要问题。

一个软件开发团队，特别是没钱的团队，代码全靠手写。想想当前人家牛X的公司，各种高大上的工具完全没有；就算顶着压力买来了，也不一定用得好，还不如自己造能用的小车，总比走路快点。

找来找去，对于一个稳定的ECU，控制策略基本定型，最大的不同就是控制器对外接口了。写这些代码都是体力劳动，基本没啥技术含量，而且还需要一颗细致的心。我总是想，再看几年这些控制器管脚配置和CAN协议信号，眼花年龄肯定提前。就算不为提高效率，也要为自己的眼睛好好考虑考虑。

## 需求

跟着当看着很好，但是没钱买的工具学：做配置，写代码的工作交给工具。看起来要做的就是写一个软件，它的功能就是根据配置生成C代码了。

首先就是要看看工具的需求了。当前的情况如下：

* 有专门的基础软件完成控制器硬件的配置、任务调度和基本服务什么的。这些功能都有相应的接口，使用时只要调用就行了。比如CAN通讯模块：

```c
// 波特率设置 node 0， 250K
CAN_SetBaudrate(NODE0, BAUDRATE_250K);
// ID 0x18FFF1A0, node 0, 100ms, 接收报文
CAN_InitMessageFrame(0x18FFF1A0, NODE0, PRD_100ms, RECIEVED)
```

* CAN信号的打包与解包还是要根据协议手动完成

```c
CAN_Unpack_0x18FFF1A0()
{
  uint32_T tmp = 0;
  
  // Bat.BusCurr  startbit: 0, length: 16, factor: 0.1A/bit, offset: -3200A
  tmp = data[0];
  tmp += data[1] >> 8;
  Bat.BusCurr = (float)tmp * 0.1 - 3200;
}
```

* 控制策略已与硬件隔离，不受控制器硬件或是管脚与CAN协议变化的制约。
* 控制器管脚通过一个映射函数，与控制策略需要的信号联系起来

```c
// key start信号接控制器32脚
Body.KeyStart = PIN32_DIH;
```

看来工具的任务，就是完成上面的三段代码，到时候只要点点鼠标就行了。

工具的输出是C语言的代码，那输入呢，可以分三部分：

> 1. CAN协议，可以用DBC
> 2. 控制器接口定义
> 3. 控制策略需要的信号

## 实现方案

基本需求确定了，就要开始干活了。

先找找我要的东西有没有现成的，没找到（要是找到了，就不写这个东西了）

再看看有没有什么模块是已有的。

> 嗯，找到个跟DBC有关的项目：[CanMatrix](https://github.com/ebroecker/canmatrix)，感谢作者Eduard

别的再找不到了，那就只能自己搞了。

野路子编程，只要能实现功能就行，一个模块一个模块搭起来。

PS: 已半夜，明天起来继续写


# CAN模块的自动代码生成（Python实现）（2）代码文件
2016.08.06

生成的代码大概是下面的样子

```C
/* 文件名： unpack.c
   作者：   fc
   时间：   2016-08-04
   说明：   .......
 */

#include "include.h"

unpack_0x0C00000B(data)
{
    int tmp;

    busCurr = (float)(data[0] + data[1] * 256) * 0.1 - 3200;
    busVolt = (float)(data[2] + data[3] * 256) * 0.1;

    mainRlyRb = data[7] & 0x01;
}
```
代码源文件有以下几部分组成：
* 文件头：包含文件名、作者、时间、文件说明等
* 文件引用
* 函数

建立以下几个类

```Python
FileHead()
FileInclud()
FuncEle()
FuncBody()
SourceFile()
```
将函数中的代码由多个元素`ele`组成，每个元素都由注释和指令组成。为了添加注释方便，建立了一个生成注释的类。

其中`SourceFile`类，有一个`GetStr`方法可以返回此代码文件的字符串，其它的每一个类都有一个`GetList `方法，返回一个列表，列表中的每个元素表示一行代码。在最后才生成字符串是为了统一计算代码缩进。当然，CAN模块的代码缩进只有一级，所以比较简单。

```python
# fileclass.py
import time

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
            # return tmplist
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
        tmplist[-1] = tmplist[-1][:-1]  # delete '\n' of the last element
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
            tmpstr += '\n'.join(func.GetList(self._indentationNum)) + '\n\n'
        # file end
        tmpstr += '// file end: ' + self._filehead._filename
        return tmpstr
```

写段代码测试一下：

```python
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
```

输出：

```shell
$ python fileclass.py
// file name   :main.c
// author      :pk
// time        :2016-08-06 11:00:07
// description :ok

// files include
#include "stdio.h"
#include "math.h"

// f1
void unpack0x1313FF01(char* data, int num)
{
    // temp variable
    uint32_T utmp;
    int32_T itmp;

    // signalname
    // startbit
    // leng
    busvolt = data[0];
}

// f2
void unpack0x1313FF01(char* data, int num)
{
    // temp variable
    uint32_T utmp;
    int32_T itmp;

    // signalname
    // startbit
    // leng
    busvolt = data[0];
}

// file end: main.c
```
