import pprint
from copy import deepcopy


class Grid(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def initField(origin: list) -> list:
    init = deepcopy(origin)
    for i in range(9):
        for j in range(9):
            if len(origin[i][j]) == 1:
                init[i][j] = [origin[i][j][0]]
            else:
                init[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    pprint.pprint(init)
    return init


def removeValue(origin: list) -> list:
    result = deepcopy(origin)
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if len(result[i][k]) == 1 and result[i][k][0] in result[i][j]:
                    result[i][j].remove(result[i][k][0])
                if len(result[k][j]) == 1 and result[k][j][0] in result[i][j]:
                    result[i][j].remove(result[k][j][0])
            for m in range(i // 3 * 3, i // 3 * 3 + 3):
                for n in range(j // 3 * 3, j // 3 * 3 + 3):
                    if len(result[m][n]) == 1 and result[m][n][0] in result[i][j]:
                        result[i][j].remove(result[m][n][0])
    pprint.pprint(result)
    return result


if __name__ == "__main__":
    test = [[[8], [], [], [], [], [], [], [], []],
            [[], [], [3], [6], [], [], [], [], []],
            [[], [7], [], [], [9], [], [2], [], []],
            [[], [5], [], [], [], [7], [], [], []],
            [[], [], [], [], [4], [5], [7], [], []],
            [[], [], [], [1], [], [], [], [3], []],
            [[], [], [1], [], [], [], [], [6], [8]],
            [[], [], [8], [5], [], [], [], [1], []],
            [[], [9], [], [], [], [], [4], [], []]]

    removeValue(initField(test))
