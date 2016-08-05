# ECU代码生成
## 对于几个输入文件顺序的做法

## 生成的代码
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
class FileHead(object):
    def __init__(self, filename = '', author = 'pk', descrip = ''):
        self._filename = filename
        self._author = author
        self._time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self._descrip = descrip

class FileInclud(object):
    def __init__(self, filelist = []):
        self._filelist = filelist

class FunctionBody(object):
    def __init__(self, name):
        self._name = name
        self._eles = []
```
