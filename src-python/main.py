from Board import Board
from Find import Find
import math


def bfs_search(board: Board):
    find_forward = Find(board)
    ff = find_forward.bfs()
    while True:
        try:
            next(ff)
        except StopIteration:
            break


def bds_search(board: Board):
    find_forward = Find(board)
    find_backward = Find(board, isBackward=True)

    ff = find_forward.bfs()
    fb = find_backward.bfs()

    while True:
        try:
            next(ff)
            next(fb)
            for ffe in find_forward.explored:
                for fbe in find_backward.explored:
                    if str(fbe) == str(ffe) and ffe.path_value >= fbe.path_value:
                        fbe.path.reverse()
                        for i in ffe.path:
                            print(i)
                        for j in fbe.path:
                            print(j)
                        return
        except StopIteration:
            break


def ids_search(board: Board):  # TODO: Has problem with sample 3
    find_forward = Find(board)
    find_forward.iddfs(100)


def a_star_search(board: Board):
    find_forward = Find(board, applyCost=True)
    find_forward.a_star()


def ida_star_search(board: Board):
    find_forward = Find(board, applyCost=True)
    find_forward.ida_star()


if __name__ == '__main__':
    m, n = map(int, input().split(' '))
    b = []
    for i in range(m):
        b.append(input().split(' '))
    board = Board(m, n, b)
    a_star_search(board)
