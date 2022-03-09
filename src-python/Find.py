import copy
import math
from typing import List

from Board import Board
from Cell import Cell


class Find:
    Costs = {
        "+": 2,
        "-": 1,
        "*": 5,
        "^": 11,
        "a": 1,
        "b": 2,
        "s": 1,
        "g": 1
    }

    def __init__(self, board: Board, isBackward: bool = False, applyCost: bool = False):
        self.board = board
        self.source = self.__find_source()
        self.goal = self.__find_goal()
        self.explored: List[Cell] = []
        self.explored_hashes = []
        self.isBackward = isBackward
        self.applyCost = applyCost

    def __find_source(self):
        for row in range(self.board.m):
            for col in range(self.board.n):
                if self.__get_opt(row, col).lower() == 's':
                    return [row, col]

    def __find_goal(self):
        for row in range(self.board.m):
            for col in range(self.board.n):
                if self.__get_opt(row, col).lower() == 'g':
                    return [row, col]

    def __get_opt(self, row: int, col: int) -> str:
        return self.board.cells[row][col][0].lower()

    def __get_number(self, row: int, col: int) -> int:
        return int(self.board.cells[row][col][1:])

    def __get_euclidean_heuristic_distance(self, row: int, col: int):
        return int(math.sqrt(math.fabs(self.goal[0] - row) ** 2 + math.fabs(self.goal[1] - col) ** 2))

    def __successor(self, cell: Cell) -> List[Cell]:

        cells = []

        def common_part(c):
            c.path.append(c)
            if self.isBackward:
                c.path_value, c.goal_value = self.__cal_reversed_opt(cell.path_value, cell.goal_value, c.row, c.col)
            else:
                c.path_value, c.goal_value = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)

            if not self.explored.__contains__(c.__hash__()):
                cells.append(c)

        if cell.row > 0:
            if self.__get_opt(cell.row - 1, cell.col) != 'w':
                c = Cell(cell.row - 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                common_part(c)
        if cell.col > 0:
            if self.__get_opt(cell.row, cell.col - 1) != 'w':
                c = Cell(cell.row, cell.col - 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                common_part(c)

        if cell.row < self.board.m - 1:
            if self.__get_opt(cell.row + 1, cell.col) != 'w':
                c = Cell(cell.row + 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                common_part(c)
        if cell.col < self.board.n - 1:
            if self.__get_opt(cell.row, cell.col + 1) != 'w':
                c = Cell(cell.row, cell.col + 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                common_part(c)
        return cells

    def __cal_reversed_opt(self, path_sum, goal_value, row, col):
        opt = self.__get_opt(row, col)

        if opt == '+':
            path_sum -= self.__get_number(row, col)
        elif opt == '-':
            path_sum += self.__get_number(row, col)
        elif opt == '*':
            path_sum /= self.__get_number(row, col)
        elif opt == '^':
            path_sum **= 1 / self.__get_number(row, col)
        elif opt == 'a':
            goal_value -= self.__get_number(row, col)
        elif opt == 'b':
            goal_value += self.__get_number(row, col)

        return path_sum, goal_value

    def __cal_opt(self, path_sum, goal_value, row, col):
        operation = self.__get_opt(row, col)
        amount = self.__get_number(row, col)
        if operation == '+':
            path_sum += amount
        elif operation == '-':
            path_sum -= amount
        elif operation == '*':
            path_sum *= amount
        elif operation == '^':
            path_sum **= amount
        elif operation == 'a':
            goal_value += amount
        elif operation == 'b':
            goal_value -= amount

        if self.applyCost:
            path_sum -= self.Costs[operation]

        return path_sum, goal_value

    def __check_goal(self, cell: Cell) -> bool:
        if (cell.path_value <= cell.goal_value and self.isBackward) or (
                cell.path_value > cell.goal_value and not self.isBackward):
            self.__print_solution(cell)
            return True
        return False

    def __calculate_f_value(self, cell: Cell) -> float:
        return cell.path_value - self.__get_euclidean_heuristic_distance(cell.row, cell.col)

    def bfs(self):
        if self.isBackward:
            startRow, startCol, endRow, endCol = self.goal[0], self.goal[1], self.source[0], self.source[1]
        else:
            startRow, startCol, endRow, endCol = self.source[0], self.source[1], self.goal[0], self.goal[1]

        queue = [
            Cell(startRow, startCol, [[False for _ in range(self.board.n)] for _ in range(self.board.m)],
                 self.__get_number(startRow, startCol),
                 self.__get_number(endRow, endCol), [])]

        queue[0].path.append(queue[0])

        while len(queue) > 0:
            cell = queue.pop(0)
            self.explored_hashes.append(cell.__hash__())
            self.explored.append(cell)
            neighbors = self.__successor(cell)

            for c in neighbors:
                if c.row == endRow and c.col == endCol:
                    if self.__check_goal(cell):
                        return
                else:
                    if not cell.table[c.row][c.col]:
                        queue.append(c)
                        yield

        print('no solution!!!')

    def dls(self, src: Cell, target_row: int, target_col: int, max_depth: int) -> bool:
        self.explored_hashes.append(src.__hash__())
        self.explored.append(src)

        if src.row == self.goal[0] and src.col == self.goal[1]:
            if self.__check_goal(src):
                return True

        if max_depth <= 0:
            return False

        neighbors = self.__successor(src)

        for c in neighbors:
            if self.dls(c, target_row, target_col, max_depth - 1):
                return True
        return False

    def iddfs(self, max_depth: int):
        startRow, startCol, endRow, endCol = self.source[0], self.source[1], self.goal[0], self.goal[1]
        src = Cell(startRow, startCol, [[False for _ in range(self.board.n)] for _ in range(self.board.m)],
                   self.__get_number(startRow, startCol),
                   self.__get_number(endRow, endCol), [])

        for i in range(max_depth):
            if self.dls(src, endRow, endCol, i):
                return

        print('No solution!')
        return

    def a_star(self):
        startRow, startCol, endRow, endCol = self.source[0], self.source[1], self.goal[0], self.goal[1]
        open_list = [
            Cell(startRow, startCol, [[False for _ in range(self.board.n)] for _ in range(self.board.m)],
                 self.__get_number(startRow, startCol),
                 self.__get_number(endRow, endCol), [])]

        open_list[0].path.append(open_list[0])

        while len(open_list) > 0:
            cell = open_list.pop(0)
            self.explored_hashes.append(cell.__hash__())
            self.explored.append(cell)
            neighbors = self.__successor(cell)

            # Finding the best neighbor
            best_neighbor = None
            best_neighbor_f = 0

            for neighbor in neighbors:
                neighbor_f = self.__calculate_f_value(neighbor)

                if neighbor.row == endRow and neighbor.col == endCol and self.__check_goal(neighbor):
                    return
                if neighbor_f >= best_neighbor_f:
                    best_neighbor = neighbor
                    best_neighbor_f = neighbor_f

            if best_neighbor is not None:
                open_list.append(best_neighbor)

        print('no solution!!!')

    def __print_solution(self, cell: Cell):
        print(len(cell.path))

        for p in cell.path:
            print(str(p.row + 1) + ' ' + str(p.col + 1))

        if self.isBackward:
            print(str(self.source[0] + 1) + ' ' + str(self.source[1] + 1))
        else:
            print(str(self.goal[0] + 1) + ' ' + str(self.goal[1] + 1))
