rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]
# 所有方格标记
boxes = cross(rows, cols)
# 所有最小规则单元
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
# 规则单元
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# 规则同胞
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    将结果以二维网格显示。
    Input: 数独的字典表示形式。
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """
    将数独网格的字符串表示形式转换为字典表示形式。
    Input: 数独网格的字符串表示形式。
    Output: 数独网格的字典表示形式。
            Keys: 方格的标记, 如： 'A1'
            Values: 方格中填入的值, 如： '8'。 如果方格中未确定值，将值暂定为'123456789'。
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def eliminate(values):
    """
    遍历所有已确定值的方格，将该方格的值从该方格的规则同胞方格中去掉。
    Input: 数独网格的字典表示形式。
    Output: 经过过滤淘汰后，数独网格的字典表示形式。
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    遍历所有最小规则单元，将仅出现过一次的数组确定为该方格的值。
    Input: 数独网格的字典表示形式。
    Output: 经过唯一可选后，数独网格的字典表示形式。
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    迭代 eliminate() 和 only_choice(). 如果出现某个格子无合法值时，返回 False，
    如果数独问题解决，返回解决后的字典形式，亦或者在一轮迭代后，数独网格中的值不再变化后的数独字典形式
    Input: 数独网格的字典表示形式。
    Output: 经过过滤淘汰和唯一可选后，数独网格的字典表示形式。
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "使用深度优先搜索，尝试所有可能的值"
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

# 实例数据
grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
values = grid_values(grid)
solved_values = search(values)
display(solved_values)