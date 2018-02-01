# 数独与AI

学习是为了寻找解决问题的答案，若脱离了问题只为知晓而进行的打call，那么随时间流逝所沉淀下来的，估计就只有“重在参与”的虚幻存在感了，自学的人就更应善于发现可供解决的问题。为了入门AI，定个小目标，解决数独问题。
## 一、问题描述

【图1】

一个9*9的方格中，部分方格已预先填入数字，目的是按照如下规则将空白方格填上1-9中的一个：
1.  每个方格中填且仅填一个数字，数字取值范围1-9
2.  以**每行**九个方格为单元来看，1-9每个数字都要出现，且仅出现一次
3.  以**每列**九个方格为单元来看，1-9每个数字都要出现，且仅出现一次
4.  以**3*3**九个方格为单元来看，1-9每个数字都要出现，且仅出现一次

> 描述问题是解决问题的第一步（将问题转化为程序所能理解的数据模型，才能做进一步有效地思考）

### 1.1 问题记录方式
1.  从左到右从上到下，以一个字符串的方式记下所有方格中的内容，有数字记数字，空白记作点（.），如：`..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..`
2.  以字典的方式记录，将每行标记为`ABCDEFGHI`，每列标记为`123456789`，字典的`key`值为标记的单元格描述，如：`A1`,`G4`等；字典的`value`值为方格中的记录：有数字记数字，空白记作点（.）
```py
{
  'A1': '.'
  'A2': '.',
  'A3': '3',
  'A4': '.',
  'A5': '2',
  ...
  'I9': '.'
}
```

> 字符串方式，记录简洁占用空间小，但处理起来比较麻烦；字典方式，方便查找处理，但记录空间较大。

所以，我们以字符串方式记录存储，以字典方式进行运算求解。那么在运算求解前需要对**记录方式的转换**。
### 1.2 字典方式记录
#### 1.2.1 所有`key`值数组
```py
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
```
#### 1.2.2 规则单元
```py
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
```
#### 1.2.3 指定单元格所属规则单元
```py
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
```
【sum用法】
### 1.3 记录方式转换
```py
def grid_values(grid):
    return dict(zip(boxes, grid))
```
`zip()` 将可迭代的对象作为参数，把对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表

## 二、策略1：过滤淘汰
首先明确一个概念：
*  规则单元：一个方格所属的水平行、垂直列以及3*3方阵的所有方格
*  规则同胞：一个方格的规则单元中除了自己的其他方格

如果没有任何限制，每个方格可填入的数字可以是`123456789`中的任何一个，而根据数独游戏规则，预先填入数字的方格会限制，该方格的**规则单元**中，其他待填数方格的数字取值范围。所以显而易见的解决策略，便是根据限制规则，缩小取值范围。

开始进行过滤淘汰之前，我们需要的初始数独方格字典中，代表空方格的（.）用可取值的数字范围替换，初始范围为`123456789`
```py
def grid_values(grid):
    valueLst = []
    digits = '123456789'
    for item in grid:
        if item == '.':
            valueLst.append(digits)
        elif item in digits:
            valueLst.append(item)
    return dict(zip(boxes, valueLst))
```
如此获得的初始数独方格字典为：
```py
{
    'A1': '123456789',
    'A2': '123456789',
    'A3': '3',
    'A4': '123456789'
    'A5': '2',
    ...
    'I9': '123456789'
}
```
> **过滤淘汰**策略：找到已确定的数独方格，再依次遍历这些方格的规则同胞方格，从待确定方格的取值范围中，把已确定的数字去掉，以缩小取值范围。
```py
def eliminate(values):
    solvedBoxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solvedBoxes:
        value = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(value, '')
    return values
```
过滤淘汰策略，是在**规则单元**上进行取值范围缩小的。这只覆盖了数独游戏规则的一部分，而数独规则还包括：
每个最小规则单元中九个方格中的数字`123456789`仅出现一次。特别说明一下，**最小规则单元**：
单行的九个方格，单列的九个方格，或3*3的九个方格，也可以说一个规则单元包含了三个最小规则单元。
## 三、策略2：唯一可选
根据最小规则单元，进一步缩小规则同胞中待填数的取值范围，便引出了第二条规则：**唯一可选策略**
【图2】
> 如果最小规则单元中，只有一个方格出现了某个数字，那么这个方格就该填这个数字

```py
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            places = [box for box in unit if digit in values[box]]
            if len(places) == 1:
                values[places[0]] = digit
    return values
```
## 四、策略3：约束搜索
