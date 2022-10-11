# -*- coding: utf-8 -*-
import copy


def init(test: list) -> list:
    """Create a 3D list of all possible values"""
    possible_value = [[[] for _ in range(10)] for _ in range(10)]
    for i in range(9):
        for j in range(9):
            if test[i][j] != 0:
                possible_value[i][j] = [test[i][j]]
            else:
                possible_value[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    return possible_value


def firstOperateValue(possible_value: list):
    for i in range(9):
        for j in range(9):
            if len(possible_value[i][j]) == 1:
                firstRemoveValue(i, j, possible_value)


def firstRemoveValue(i: int, j: int, possible_value: list):
    """Delete the value which has been determined according to a single-valued grid"""
    for k in range(9):
        firstConfirmValue(i, k, possible_value[i][j][0], possible_value)
        firstConfirmValue(k, j, possible_value[i][j][0], possible_value)

    for k in range(i // 3 * 3, i // 3 * 3 + 3):
        for m in range(j // 3 * 3, j // 3 * 3 + 3):
            firstConfirmValue(k, m, possible_value[i][j][0], possible_value)


def firstConfirmValue(i: int, j: int, value: int, possible_value: list):
    if len(possible_value[i][j]) == 1:
        return

    if value in possible_value[i][j]:
        possible_value[i][j].remove(value)
    if len(possible_value[i][j]) == 1:
        firstRemoveValue(i, j, possible_value)


def secondRemoveValue(possible_value: list):
    """Find out the value that appears only once to fill in the box."""
    count_row = [[0] * 10 for _ in range(10)]  # value:1-9, Prevent "list index out of range"
    count_col = [[0] * 10 for _ in range(10)]
    count_grd = [[0] * 10 for _ in range(10)]

    # The valueber of times statistical values appear in rows, columns, and 9×9 grids.
    for i in range(9):
        for j in range(9):
            for value in possible_value[i][j]:
                count_row[i][value] += 1
                count_col[j][value] += 1
                count_grd[i // 3 * 3 + j // 3][value] += 1

    for i in range(9):
        for j in range(1, 10):
            if count_row[i][j] == 1:
                for k in range(9):
                    secondConfirmValue(i, k, j, possible_value)
            if count_col[i][j] == 1:
                for k in range(9):
                    secondConfirmValue(k, i, j, possible_value)
            if count_grd[i][j] == 1:
                for k in range(i // 3 * 3, i // 3 * 3 + 3):
                    for n in range(i % 3 * 3, i % 3 * 3 + 3):
                        secondConfirmValue(k, n, j, possible_value)


def secondConfirmValue(i: int, j: int, sole_value, possible_value: list):
    if len(possible_value[i][j]) == 1:
        return

    if sole_value in possible_value[i][j]:
        possible_value[i][j] = [sole_value]
        firstRemoveValue(i, j, possible_value)


def dfsSearch(node: list, possible_value: list) -> list:
    if node is None:
        return possible_value

    x, y = node[0], node[1]
    for value in possible_value[x][y]:
        tmp = copy.deepcopy(possible_value)
        tmp[x][y] = [value]
        firstRemoveValue(x, y, tmp)
        secondRemoveValue(tmp)

        if judge(tmp):
            tmp = dfsSearch(getLeastNode(tmp), tmp)
            if tmp is not None:
                return tmp


def getLeastNode(possible_value: list) -> list:
    minn = 9
    node = None
    for i in range(9):
        for j in range(9):
            if 1 < len(possible_value[i][j]) < minn:
                minn = len(possible_value[i][j])
                node = [i, j]

    return node


def judge(possible_value: list):
    """Determine whether a certain value can be stored at a certain location."""
    count_row = [[False] * 10 for _ in range(10)]
    count_col = [[False] * 10 for _ in range(10)]
    count_grd = [[False] * 10 for _ in range(10)]

    for i in range(9):
        for j in range(9):
            if len(possible_value[i][j]) == 1:
                if count_row[i][possible_value[i][j][0]] or count_col[j][possible_value[i][j][0]] or \
                        count_grd[i // 3 * 3 + j // 3][possible_value[i][j][0]]:
                    return False

                count_row[i][possible_value[i][j][0]] = True
                count_col[j][possible_value[i][j][0]] = True
                count_grd[i // 3 * 3 + j // 3][possible_value[i][j][0]] = True

    return True


def main(test: list):
    r = 0
    while True:
        sudoku = init(test)
        firstOperateValue(sudoku)
        secondRemoveValue(sudoku)

        sudoku = dfsSearch(getLeastNode(sudoku), sudoku)
        if sudoku is not None:
            for i in range(9):
                for j in range(9):
                    print(sudoku[i][j], end="")
                print()
            return

        r += 1
        if r > 81:
            return


if __name__ == "__main__":
    try:
        eg = []
        t = []
        with open("./test.txt") as f:
            lines = f.readlines()
            for line in lines:
                for ch in line:
                    if ch != "\n":
                        t.append(eval(ch))
                eg.append(t)
                t = []

        main(eg)
    except Exception as error:
        print(error)
