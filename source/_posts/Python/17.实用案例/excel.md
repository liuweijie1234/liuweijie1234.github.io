---
title: Python3 操作Excel常用库
date: 2022-08-15 10:22:00
tags:
- Python
categories:
- Python
---


[Python3操作Excel常用库整理（xlrd/xlwt,openpyxl,xlwings和xlsxwriter）](https://zhuanlan.zhihu.com/p/500771899)
[Python学习笔记（二）xlwt库与xlsxwriter库的区别](https://zhuanlan.zhihu.com/p/144082064)

## 模块简介

**xlrd**：支持读取 .xls ，不支持读取 .xlsx 文件, 需要使用低版本xlrd才能读取.xlsx文件 (pip install xlrd==1.2.0)

**xlwt**：支持创建和写入 .xls 格式的文件，不支持创建和写入 .xlsx 文件；存储的数量非常少

**openpyxl**：支持读写 .xlsx 文件；不支持读写 .xls 文件；存储的数量非常大

优点：
- 功能较广泛，可以设置单元格格式等。
- 支持对工作表的操作，如插入、删除和重命名等。

缺点：
- 执行速度可能相对较慢，特别是处理大型数据文件时。
- 不支持直接将 Excel 文件转换为其他格式，如CSV。

**xlwings**：支持读写 .xls 和 .xlsx 文件；

优点：
- 支持与 Excel 的完全交互，包括读取、写入、操作和调用 VBA 宏等。
- 可以在Python中实现复杂的数据处理和分析任务。

缺点：
- 需要安装 Excel 应用程序，并且只能在Windows和Mac上使用。
- 对于简单的读写操作，可能相对于其他模块来说过于复杂。

**xlsxwriter** ：支持创建和写入 .xlsx 文件；不支持创建和写入 .xls 文件

优点：
- 可以创建复杂的 Excel 文件，支持较多的 Excel 功能和格式，支持图片/表格/图表/格式等。
- 提供了优化的写入速度，适用于大型数据文件的处理，可存储100万条记录。

缺点：
- 不支持读取和解析现有的 Excel 文件。
- 不支持对已有文件进行修改操作，只能创建新的文件。


![](/images/v2-838b133a0fc1316f5343917c80ac3943_r.png)

## xlrd

### 2、安装

```bash
pip install xlrd
```

### 3、使用


#### 3.1 打开 excel 文件
```python
import xlrd 

"""
step 1

xlrd.open_workbook 
作用：打开 excel 文件读取数据
本质：得到对象 class 'xlrd.book.Book'
路径：Lib/site-packages/xlrd/book.py
"""

book = xlrd.open_workbook("myfile.xls")  

>>> book.nsheets        # 获取 book 的 sheets 数目 (int)
1
>>> book.sheet_names()  # 返回 sheet 的 name (list)
['Sheet1']
```

#### 3.2 读取工作表
```python
"""
step 2

作用：获取 book 中的工作表 sheet
本质：通过 book 得到对象 class 'xlrd.sheet.Sheet'

后续行、列、块都是基于 sheet 对象操作
"""

sheet = book.sheets()[0]                 # 通过索引顺序获取 (class 'xlrd.sheet.Sheet')

sheet_indx = 0
sheet = book.sheet_by_index(sheet_indx)  # 通过索引顺序获取 (class 'xlrd.sheet.Sheet')

sheet_name = 'Sheet1'
sheet = book.sheet_by_name(sheet_name)   # 通过名称获取 (class 'xlrd.sheet.Sheet')

name = sheet.name                        # 获取该 sheet 的 name
nrows = sheet.nrows                      # 获取该 sheet 中的有效行数（int）
ncols = sheet.ncols                      # 获取该 sheet 中的有效列数（int）

```

#### 3.3 读取工作表的行数据

```python
"""
step 3 
行操作
"""
# start_colx 指开始的列索引，end_colx 指结束的列索引
sheet.row(rowx)                                      # 返回由该行中所有的单元格对象组成的列表
sheet.row_slice(rowx)                                # 与 row()类似
sheet.row_types(rowx, start_colx=0, end_colx=None)   # 返回由该行中所有单元格的数据类型组成的列表
sheet.row_values(rowx, start_colx=0, end_colx=None)  # 返回由该行中所有单元格的数据组成的列表
sheet.row_len(rowx)                                  # 返回该行的有效单元格长度

>>> sheet.row(0)
[text:'ESN', text:'PWD', text:'MAC', text:'SN']

>>> sheet.row_slice(0)
[text:'ESN', text:'PWD', text:'MAC', text:'SN']

>>> sheet.row_types(0)
array('B', [1, 1, 1, 1])

>>> sheet.row_values(0)
['ESN', 'PWD', 'MAC', 'SN']

>>> sheet.row_len(0)
4

```
#### 3.4 读取工作表的列数据
```python
"""
step 4
列操作
"""
# start_rowx指开始的行索引，end_rowx指结束的行索引
sheet.col(colx, start_rowx=0, end_rowx=None)         # 返回由该列中所有的单元格对象组成的列表，
sheet.col_slice(colx, start_rowx=0, end_rowx=None)   # 与 sheet.col()类似
sheet.col_types(colx, start_rowx=0, end_rowx=None)   # 返回由该列中所有单元格的数据类型组成的列表
sheet.col_values(colx, start_rowx=0, end_rowx=None)  # 返回由该列中所有单元格的数据组成的列表


>>> sheet.col(0,start_rowx=1,end_rowx=2)
[text:'xxx2224511428']
>>> sheet.col_types(0,start_rowx=1,end_rowx=4)
[1, 1, 1]
>>> sheet.col_values(0,start_rowx=1,end_rowx=4)
['xxx2224511428', 'xxx2224511427', 'xxx2224511426']

```
#### 3.5 读取工作表的单元格数据
```python
"""
step 5 
单元格操作
"""
sheet.cell(rowx,colx)        # 返回单元格对象  <class 'xlrd.sheet.Cell'>
sheet.cell_type(rowx,colx)   # 返回单元格中的数据类型
sheet.cell_value(rowx,colx)  # 返回单元格中的数据

>>> sheet.cell(0,0)
text:'ESN'
>>> sheet.cell_type(0,0)
1
>>> sheet.cell_value(0,0)
'ESN'

```

### 4、常用单元格中的数据类型

0 -> empty（空的）
1 -> string（text）
2 -> number
3 -> date
4 -> boolean
5 -> error
6 -> blank（空白表格）

### 5、参考链接

http://www.python-excel.org/
https://xlrd.readthedocs.io/en/latest/
https://www.cnblogs.com/insane-Mr-Li/p/9092619.html



## openpyxl

```python
from openpyxl import load_workbook

# 加载 Excel 文件
workbook = load_workbook('example.xlsx')

# 获取工作表
worksheet = workbook['Sheet1']

# 读取数据
cell_value = worksheet['A1'].value
print(cell_value)
```

### 在Django中使用openpyxl

```python
from openpyxl import Workbook
from django.http import HttpResponse

def export_to_excel(request):
    # 创建一个Workbook对象
    wb = Workbook()
    ws = wb.active

    # 查询数据并写入Excel
    queryset = MyModel.objects.all()
    for row_num, obj in enumerate(queryset, start=1):
        ws.cell(row=row_num, column=1, value=obj.field1)
        ws.cell(row=row_num, column=2, value=obj.field2)
        ws.cell(row=row_num, column=3, value=obj.field3)

    # 设置响应头
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'

    # 将Workbook保存到HttpResponse中
    wb.save(response)

    return response
```



## xlwt

xlwt 是一个用于读写 Excel 97-2003 xls 文件格式的 Python 库。以下是 xlwt 的一些优点：

- 轻量级：xlwt 是一个轻量级库，其安装包的体积比 openpyxl 小得多。
- 较快的速度：由于 xlwt 是用 C++ 编写的，并提供了 Python 接口，因此其速度比 openpyxl 快得多，特别是处理大型数据集时会更加明显。
- 兼容性：xlwt 支持所有版本的 Microsoft Excel（97-2003），并可以与其他基于 COM 的开发工具无缝协作。

xlwt 的一些缺点包括：

- 不支持新版 Excel 格式：尽管 xlwt 支持 Excel 97-2003 中的 XLS 格式，但它不支持新版的 Excel 格式，如 XLSX、XLSM 等。
- 功能较少：相比于 openpyxl，xlwt 提供的功能要少得多，不支持像数据透视表和条件格式等高级功能。

综上所述，选择使用 openpyxl 还是 xlwt 取决于您的具体需求。
如果需要处理 Excel 2010 中的 XLSX/XLSM 格式文件或希望使用更多自定义选项和高级功能，则应选择 openpyxl。
如果需要处理 Excel 97-2003 中的 XLS 格式文件或关注速度和轻量级，则应选择 xlwt。



### 2、安装

```bash
pip install xlwt
```

### 3、使用

#### 3.1 基本使用

建立工作簿对象 ——> 新建sheet表 ——> 将数据写入 ——> 保存文件

```python
import xlwt
workbook = xlwt.Workbook()                  # 新建一个表，xlwt与 xlswriter 的区别，后面不跟文件路径
sheet_name = "Test"
worksheet = workbook.add_sheet(sheetname=sheet_name,cell_overwrite_ok=True)  # 在工作薄中新建一个表格，与 xlswriter 的区别是 add_worksheet 多了work
worksheet.write(0,1,'test01')               # worksheet.write(rowx,colx,value,style) 行、列、单元格的值、单元格格式
path = 'test.xlsx'
workbook.save(path)                         # 保存工作薄，与 xlswriter 的区别是 xlswriter是 close 关闭，不是保存

#### 3.2 单元格操作


- 写入单个单元格数据（write）

```python
worksheet.write(0,1,'test01')  # worksheet.write(rowx,colx,value,style) 行、列、单元格的值、单元格格式
```

- 将列表数据写入一个单元格（write_rich_text）

```python
test_list = [str(i) for i in range(5)]
worksheet.write_rich_text(0,0,test_list)  # worksheet.write_rich_text(rowx,colx,rich_text_list,style=Style.default_style)
```

- 合并单元格（merge）

```python
worksheet.merge(2,3,0,3)   # worksheet.merge(start_rowx,end_rowx,start_colx,end_colx,style=Style.default_style)
```

- 合并单元格并写入数据（write_merge）

```python
worksheet.write_merge(4,4,0,3,'合并单元格数据')  # write_merge(start_rowx, end_rowx, start_colx, end_colx, label="", style=Style.default_style)
```

### 4、参考链接

https://xlwt.readthedocs.io/en/latest/


## 具体案例



```python

import xlrd, xlwt
from xlutils.copy import copy


def write_excel_xls(path, sheet_name, value):
    index = len(value)                       # 获取需要写入数据的行数
    workbook = xlwt.Workbook()               # 新建一个工作薄
    sheet = workbook.add_sheet(sheet_name)   # 在工作薄中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])   # 像表格中写入数据(对应的行、列、值的位置)
    workbook.save(path)                      # 保存工作薄
    print("xls格式表格写入数据成功")


def write_excel_xls_append(path, value):
    index = len(value)                             # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)            # 打开工作簿
    sheets = workbook.sheet_names()                # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows                     # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)                  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)      # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


book_name_xls = '刘伟杰-蓝鲸运营.xls'

sheet_name_xls = 'Sheet1'

value_title = [["邮件条码","收件人姓名","收件人电话","收件人公司名称","收件人地址","寄达城市","收件人客户代码","收件人邮编","内件品名","信函","文件资料","物品","是否保价","声明价值1","声明价值2","总件数","实际重量","计费重量","总体积","妥投短信","实物返单","电子返单","其它","代收货款","货款金额1","货款金额2","邮费","保价费","封装费","其它费用","费用合计","投递应收寄递费","寄件人付","收件人付","刷卡","月结","第三方付费","现金","收寄人员","寄件人","寄件人电话","寄件人公司名称","寄件人地址","寄件人客户代码","客户单号","寄件人邮编","寄件人签署"], ]

value1 = [["","老王","155xxxxx","","青海省西宁市城西区xxxxxxx","","","","蓝鲸T-shirt白衣小图（男）-XXL","","X","","X","","","","0.1",'','','','','','','','','','','','','','','',"Ⅹ",'','','','','',"xxxx","腾讯蓝鲸","xxxxxx","","深圳市南山区科技园中区科兴科学园C1栋","","","xxxx",""], ]


write_excel_xls(book_name_xls, sheet_name_xls, value_title)
write_excel_xls_append(book_name_xls, value1)

```



```python
def create_excel(sheet_name, headers=[], data=[]):
    """
    生成一个excel文件的IO流
    :param sheet_name: 工作簿名称
    :param headers: 标题栏名称列表
    :param data: 数据，二维数组
    :return: Bytes
    """
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    # 写入首行标题栏
    for i in range(len(headers)):
        sheet.write(0, i, headers[i])
        # sheet.col(i).width = 256 * 32
        # sheet.row(0).set_style(xlwt.easyxf('font:height 600'))
    # 写入数据
    for row in range(len(data)):
        for li in range(len(data[row])):
            sheet.write(row + 1, li, data[row][li])
    # 保存
    output = BytesIO()
    workbook.save(output)
    return output
```


## xlsxwriter

https://www.w3ccoo.com/python_xlsxwriter/index.html

```bash
pip3 install xlsxwriter
```

```python
import xlsxwriter

# 创建 Excel 文件
workbook = xlsxwriter.Workbook('results.xlsx')
worksheet = workbook.add_worksheet('new_sheet')  # 将新工作表添加到工作簿。

# 定义 Excel 表头
headers = ['Thread', 'Request', 'Status Code', 'Response']
for col, header in enumerate(headers):
    worksheet.write(0, col, header)  # row, col, *args 行,列,内容

# 将结果写入 Excel 文件
row = 1
for result in results:
    thread_num, request_num, status_code, response_text = result
    try:
        worksheet.write(row, 0, thread_num)
        worksheet.write(row, 1, request_num)
        worksheet.write(row, 2, status_code)
        worksheet.write(row, 3, response_text)
        row += 1
    except Exception as e:
        print(f"Error writing row {row}: {e}")
        

worksheet.set_column(2, 2, 30)  # 设置第3列的宽度为30
worksheet.set_column(4, 4, 30)  # 设置第5列的宽度为30
# 关闭 Excel 文件
workbook.close()  # 关闭工作簿对象并写入 XLSX 文件。
```


```python
import io
from django.http import HttpResponse
from xlsxwriter.workbook import Workbook

def export_excel(request):
    # 创建一个内存缓冲区
    output = io.BytesIO()

    # 创建一个 Excel 工作簿
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # 添加一些示例数据
    worksheet.write(0, 0, 'Hello, world!')
    worksheet.write(1, 0, 'This is an example')

    # 关闭工作簿
    workbook.close()

    # 重置缓冲区指针
    output.seek(0)

    # 创建 HTTP 响应
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # 设置文件名称
    response['Content-Disposition'] = 'attachment; filename=my_excel_file.xlsx'

    # 返回响应
    return response
```
