# -*- coding: utf-8 -*-
from copy import deepcopy
from pprint import pprint

from sudoku.test import *


class Solution(object):
    def __init__(self, sudoku: list):
        self.sudoku = sudoku

    def tmpSolve(self):
        self.initField()
        self.firstRemoveValue()
        self.secondRemoveValue()

    def initField(self):
        """Create a 3D list of all possible values"""
        for i in range(9):
            for j in range(9):
                if len(self.sudoku[i][j]) != 1:
                    self.sudoku[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def firstRemoveValue(self):
        """Delete the value which has been determined according to a single-valued grid"""
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if len(self.sudoku[i][k]) == 1 and self.sudoku[i][k][0] in self.sudoku[i][j] and k != j:
                        self.sudoku[i][j].remove(self.sudoku[i][k][0])
                    if len(self.sudoku[k][j]) == 1 and self.sudoku[k][j][0] in self.sudoku[i][j] and k != i:
                        self.sudoku[i][j].remove(self.sudoku[k][j][0])
                for m in range(i // 3 * 3, i // 3 * 3 + 3):
                    for n in range(j // 3 * 3, j // 3 * 3 + 3):
                        if len(self.sudoku[m][n]) == 1 and self.sudoku[m][n][0] in self.sudoku[i][
                            j] and m != i and n != j:
                            self.sudoku[i][j].remove(self.sudoku[m][n][0])

    def secondRemoveValue(self):
        """Find out the value that appears only once to fill in the box."""
        count_row = [[0] * 10 for _ in range(9)]
        count_col = [[0] * 10 for _ in range(9)]
        count_grd = [[0] * 10 for _ in range(9)]
        # The number of times statistical values appear in rows, columns, and 9×9 grids.
        for i in range(9):
            for j in range(9):
                for num in self.sudoku[i][j]:
                    count_row[i][num] += 1
                    count_col[j][num] += 1
                    count_grd[i // 3 * 3 + j // 3][num] += 1

        for i in range(9):
            for j in range(9):
                if count_row[i][j] == 1:
                    for k in range(9):
                        self.confirmLocation(i, k, j)
                if count_col[i][j] == 1:
                    for k in range(9):
                        self.confirmLocation(k, j, i)
                if count_grd[i][j] == 1:
                    for m in range(i // 3 * 3, i // 3 * 3 + 3):
                        for n in range(i % 3 * 3, i % 3 * 3 + 3):
                            self.confirmLocation(m, n, j)

    def confirmLocation(self, row, col, num):
        if num in self.sudoku[row][col]:
            self.sudoku[row][col][0] = num
            self.firstRemoveValue()


class DFS(Solution):
    def __init__(self, sudoku: list):
        self.node = []
        super().__init__(sudoku)
        self.tmpSolve()

    def solve(self):
        self.getLeastGrid()
        if len(self.node) == 0:
            return
        x, y = self.node[0], self.node[1]
        for value in self.sudoku[x][y]:
            storage = deepcopy(self.sudoku)
            self.sudoku[x][y] = [value]
            self.firstRemoveValue()
            self.secondRemoveValue()
            if self.judge():
                self.getLeastGrid()
                self.solve()
                if self.sudoku is not None:
                    return self.sudoku
                else:
                    self.sudoku = storage

    def getLeastGrid(self):
        minn = 100
        for i in range(9):
            for j in range(9):
                if 1 < len(self.sudoku[i][j]) < minn:
                    minn = len(self.sudoku[i][j])
                    self.node = [i, j]

    def judge(self):
        """Determine whether a certain value can be stored at a certain location."""
        count_row = [[False] * 10 for _ in range(12)]
        count_col = [[False] * 10 for _ in range(12)]
        count_grd = [[False] * 10 for _ in range(12)]
        for i in range(9):
            for j in range(9):
                if len(self.sudoku[i][j]) == 1:
                    if count_row[i][self.sudoku[i][j][0]] or count_col[j][self.sudoku[i][j][0]] or \
                            count_grd[i // 3 * 3 + j // 3][self.sudoku[i][j][0]]:
                        return False
                    count_row[i][self.sudoku[i][j][0]] = True
                    count_col[j][self.sudoku[i][j][0]] = True
                    count_row[i // 3 * 3 + j // 3][self.sudoku[i][j][0]] = True

        return True


def main(sudoku):
    while True:
        obj = DFS(sudoku)
        obj.solve()
        if obj.sudoku is not None:
            pprint(obj.sudoku)
            return
        if not obj.judge():
            print("Tmp Wrong")


if __name__ == "__main__":
    print("************************************************************")
    main(test0)
    print("************************************************************")
    main(test1)
    print("************************************************************")
    main(test2)
    print("************************************************************")
    main(test3)
