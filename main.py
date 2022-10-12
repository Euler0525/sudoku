# -*- coding: utf-8 -*-
import copy


def initSudoku(test: list) -> list:
    """Create a 3D list of all poss values"""
    poss_value = [[[] for _ in range(10)] for _ in range(10)]
    for i in range(9):
        for j in range(9):
            if test[i][j] != 0:
                poss_value[i][j] = [test[i][j]]
            else:
                poss_value[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    return poss_value


def firstOperateValue(poss_value: list):
    for i in range(9):
        for j in range(9):
            if len(poss_value[i][j]) == 1:
                firstRemoveValue(i, j, poss_value)


def firstRemoveValue(i: int, j: int, poss_value: list):
    """Delete the value which has been determined according to a single-valued grid"""
    for k in range(9):
        firstConfirmValue(i, k, poss_value[i][j][0], poss_value)
        firstConfirmValue(k, j, poss_value[i][j][0], poss_value)

    for k in range(i // 3 * 3, i // 3 * 3 + 3):
        for m in range(j // 3 * 3, j // 3 * 3 + 3):
            firstConfirmValue(k, m, poss_value[i][j][0], poss_value)


def firstConfirmValue(i: int, j: int, value: int, poss_value: list):
    if len(poss_value[i][j]) == 1:
        return

    if value in poss_value[i][j]:
        poss_value[i][j].remove(value)
    if len(poss_value[i][j]) == 1:
        firstRemoveValue(i, j, poss_value)


def secondRemoveValue(poss_value: list):
    """Find out the value that appears only once to fill in the box."""
    count_row = [[0] * 10 for _ in range(10)]  # value:1-9, Prevent "list index out of range"
    count_col = [[0] * 10 for _ in range(10)]
    count_grd = [[0] * 10 for _ in range(10)]

    # The valueber of times statistical values appear in rows, columns, and 9×9 grids.
    for i in range(9):
        for j in range(9):
            for value in poss_value[i][j]:
                count_row[i][value] += 1
                count_col[j][value] += 1
                count_grd[i // 3 * 3 + j // 3][value] += 1

    for i in range(9):
        for j in range(1, 10):
            if count_row[i][j] == 1:
                for k in range(9):
                    secondConfirmValue(i, k, j, poss_value)
            if count_col[i][j] == 1:
                for k in range(9):
                    secondConfirmValue(k, i, j, poss_value)
            if count_grd[i][j] == 1:
                for k in range(i // 3 * 3, i // 3 * 3 + 3):
                    for n in range(i % 3 * 3, i % 3 * 3 + 3):
                        secondConfirmValue(k, n, j, poss_value)


def secondConfirmValue(i: int, j: int, sole_value: int, poss_value: list):
    if len(poss_value[i][j]) == 1:
        return

    if sole_value in poss_value[i][j]:
        poss_value[i][j] = [sole_value]
        firstRemoveValue(i, j, poss_value)


"""
This is the end of the primary solution. The above methods can solve some simple Sudoku.
The difficult ones need to be further eliminated.
"""


def dfsSearch(node: list, poss_value: list) -> list:
    if node is None:  # Sudoku has been solved by exclusion algorithm.
        return poss_value

    r, c = node[0], node[1]
    for value in poss_value[r][c]:
        tmp = copy.deepcopy(poss_value)
        tmp[r][c] = [value]
        firstRemoveValue(r, c, tmp)
        secondRemoveValue(tmp)

        if judge(tmp):
            node = getLeastNode(tmp)
            tmp = dfsSearch(node, tmp)
            if tmp is not None:
                return tmp


def getLeastNode(poss_value: list) -> list:
    minn = 9
    node = None
    for i in range(9):
        for j in range(9):
            if 1 < len(poss_value[i][j]) < minn:
                minn = len(poss_value[i][j])
                node = [i, j]

    return node


def judge(poss_value: list):
    """Determine whether a certain value can be stored at a certain location."""
    count_row = [[False] * 10 for _ in range(10)]
    count_col = [[False] * 10 for _ in range(10)]
    count_grd = [[False] * 10 for _ in range(10)]

    for i in range(9):
        for j in range(9):
            if len(poss_value[i][j]) == 1:
                if count_row[i][poss_value[i][j][0]] or count_col[j][poss_value[i][j][0]] or \
                        count_grd[i // 3 * 3 + j // 3][poss_value[i][j][0]]:
                    return False

                count_row[i][poss_value[i][j][0]] = True
                count_col[j][poss_value[i][j][0]] = True
                count_grd[i // 3 * 3 + j // 3][poss_value[i][j][0]] = True

    return True


def main(test: list):
    r = 0
    while True:
        sudoku = initSudoku(test)
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
