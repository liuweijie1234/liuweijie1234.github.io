---
title: Python3 模块 pandas
date: 2022-08-15 10:22:00
tags:
- Python module
- pandas
categories:
- Python
---

## 简介

Pandas 可以从各种文件格式比如 CSV、JSON、SQL、Microsoft Excel 导入数据。

Pandas 可以对各种数据进行运算操作，比如归并、再成形、选择，还有数据清洗和数据加工特征。


Pandas 是数据分析的利器，它不仅提供了高效、灵活的数据结构，还能帮助你以极低的成本完成复杂的数据操作和分析任务。

Pandas 提供了丰富的功能，包括：

数据清洗：处理缺失数据、重复数据等。
数据转换：改变数据的形状、结构或格式。
数据分析：进行统计分析、聚合、分组等。
数据可视化：通过整合 Matplotlib 和 Seaborn 等库，可以进行数据可视化。

## 参考

https://pandas.pydata.org/docs/user_guide/index.html
https://pandas.pydata.org/docs/reference/index.html


## 安装

```bash
pip install pandas
```

## 操作文件

### 操作Excel文件

[Python Pandas库批量处理Excel数据](https://mp.weixin.qq.com/s?__biz=MzU3Mjc2MjU5Mg==&mid=2247484355&idx=1&sn=f0c3ac04083e7ca1829c041b831dc771&chksm=fccab34ccbbd3a5a75ba3af8193b82f28a32b32b55a700cb699454e534751c781767e0928ba1&scene=21#wechat_redirect)

### read_excel()

pandas.read_excel()是Pandas库中用于读取Excel文件的函数。它可以将Excel文件中的数据读入到Pandas的DataFrame对象中，方便后续的数据处理和分析。

以下是read_excel()函数的一些常用参数：

io: 要读取的Excel文件名或者文件路径，支持本地文件路径、URL和文件内存的句柄，默认为None。

sheet_name: 指定要读取的Excel工作表的名称或编号。如果指定为None，则默认读取第一个工作表。可以传入一个整数表示工作表的索引，也可以传入一个字符串表示工作表的名称，默认为0。

header: 指定Excel文件中哪一行作为列名，可以是行号或者列表。默认值为0，即使用第一行作为列名。如果设置为None，则不使用列名，会自动将第一行数据作为索引。

names: 可选参数，用于指定DataFrame的列名，如果header=None，则必须设置该参数。

index_col: 指定哪列作为行索引，可以是列名或者列号，默认值为None。

usecols: 指定要读取的列的列表，可以是列名或者列号，默认值为None，表示读取所有列。

dtype: 指定每一列的数据类型，可以是字典或者函数。例如，{'a': np.float64, 'b': str, 'c': int}。

na_values: 指定某些特殊值在读取时应当被视为缺失值。

keep_default_na: 如果设置为False，将无条件地保留所有的NA值。默认为True，将使用一组默认的NA标记来表示缺失值（如NaN、#N/A等）。

converters: 指定每一列的类型转换函数，可以是字典或者函数。例如，{'a': lambda x: int(x.strip('%')), 'b': pd.to_datetime}。

parse_dates: 指定要解析为日期的列，可以是列名或者列号，默认值为False，表示不解析任何列。

date_parser: 用于解析日期的函数，默认为None，表示使用pandas.to_datetime函数进行解析。

这些参数中，io、sheet_name和header是最常用的参数，其他参数根据具体情况酌情使用。


### unique()

unique() 是 Pandas 库中的一个方法，用于返回给定序列中的唯一元素。它返回一个包含所有唯一值的数组，并按照它们出现的顺序排列。

例如，如果你有一个 Pandas Series 对象：

你可以使用 unique() 方法来获取该 Series 中的唯一值：

```python
import pandas as pd

my_series = pd.Series([1, 2, 3, 4, 5, 6, 3, 4, 5])

unique_values = my_series.unique()

print(unique_values)
```


输出结果为：

[1 2 3 4 5 6]

unique() 方法的作用是帮助你找到一个给定序列中的唯一值。在很多数据分析应用中，这是非常有用的操作，因为它可以让你知道某个数据集中都有哪些不同的数据。


### groupby()

groupby()是一个在Python Pandas库中非常有用的函数，它可以将数据按照一定的规则分组。通常情况下，我们使用groupby()函数对数据进行分组，并计算每个组的统计量。

groupby()函数的基本语法如下：

```python
DataFrame.groupby(by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, observed=False)
```
参数说明如下：

by: 根据哪些列进行分组。可以传递多个列名或者字典来指定分组方式。
axis: 沿着哪个轴进行分组，默认值为0，表示沿着行的方向进行分组。
level: 如果轴是多层索引，则根据某个级别分组。
as_index: 是否将分组依据的列设置为索引，默认为True。
sort: 分组后是否按照分组依据的列排序，默认为True。
group_keys: 是否添加分组键到输出结果中，默认为True。
squeeze: 是否压缩返回的数据，默认为False。
observed: 是否仅考虑观察到的标签值，默认为False。

下面是一个简单的示例，假设我们有一个包含姓名、性别和年龄的表格数据：
我们可以使用groupby()函数按照性别来分组，然后计算每个性别的平均年龄：

```python
import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emily', 'Frank', 'Grace', 'Henry', 'Isabella', 'Jack'],
        'Gender': ['F', 'M', 'M', 'M', 'F', 'M', 'F', 'M', 'F', 'M'],
        'Age': [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]}

df = pd.DataFrame(data)

gender_group = df.groupby('Gender')
mean_age_by_gender = gender_group['Age'].mean()
print(mean_age_by_gender)
```
输出结果如下：
```python
Gender
F    40.0
M    42.5
Name: Age, dtype: float64
```
这里我们首先使用groupby()函数将数据按照性别进行分组，然后选取年龄列，并使用mean()方法计算每个组的平均值。最终输出了每个性别的平均年龄。

#### group.iterrows()

group 是 GroupBy 对象 , iterrows()获取每行数据


### iloc()

iloc() 是 pandas 中用于按位置（即行号和列号）访问数据的方法。它可以接受一个或多个整数、整数序列或布尔数组作为参数，用于选择 DataFrame 或 Series 的行和列。

下面是一些 iloc() 的示例：
```python
import pandas as pd

# 创建一个 3 行 2 列的 DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})

# 使用 iloc() 选择第一行和第二行
print(df.iloc[[0, 1]])

# 输出：
#    A  B  C
# 0  1  4  7
# 1  2  5  8

# 使用 iloc() 选择第一行和第二行，以及第一列和第三列
print(df.iloc[[0, 1], [0, 2]])

# 输出：
#    A  C
# 0  1  7
# 1  2  8

# 使用 iloc() 选择第一行和第二行，以及第一列到第二列的所有列
print(df.iloc[[0, 1], 0:2])

# 输出：
#    A  B
# 0  1  4
# 1  2  5
```

可以看到，iloc() 可以很方便地对 DataFrame 进行按位置的选择和切片。当需要根据行号和列号来访问数据时，iloc() 是一个非常有用的方法。

### iterrows()

iterrows() 是 Pandas 库中的一个函数，它可以用来按行迭代 DataFrame 中的数据。具体来说，该函数返回一个生成器(generator)，每次迭代时会返回一个包含当前行索引和对应行数据的元组。

下面是一个示例：

```python
import pandas as pd

# 创建一个 DataFrame
df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]})

# 使用 iterrows() 迭代 DataFrame
for index, row in df.iterrows():
    print(index, row['name'], row['age'])
```
运行上述代码将输出以下结果：
```python
0 Alice 25
1 Bob 30
2 Charlie 35
```
在这个示例中，我们首先创建了一个包含三行数据的 DataFrame，然后使用 iterrows() 函数按行迭代该 DataFrame。对于每一行数据，iterrows() 函数会返回当前行的索引以及包含该行数据的 Pandas Series 对象。我们可以通过 Series 对象的键名（即列名）访问该行数据的各个字段，并进行相应的处理。