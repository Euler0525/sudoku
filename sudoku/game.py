import pprint

class Grid(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def initField(origin: list) -> list:
    init = []
    for i in range(9):
        for j in range(9):
            if len(origin[i][j]) == 1:
                init.append([origin[i][j][0]])
            else:
                init.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
    pprint.pprint(init)
    return init


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
    initField(test)
