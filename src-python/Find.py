import copy
import math
from typing import List

from Board import Board
from Cell import Cell

INFINITY = 9999999


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
        self.applyCosts = applyCost

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
        x_power_two = math.fabs(self.goal[0] - row) ** 2
        y_power_two = math.fabs(self.goal[1] - col) ** 2
        return x_power_two + y_power_two * 3  # 3 = average cost

    def __successor(self, currentCell: Cell) -> List[Cell]:

        cells = []

        def common_part(nextCell):
            nextCell.path.append(nextCell)
            if self.isBackward:
                nextCell.path_value, nextCell.goal_value = self.__apply_reversed_opt(currentCell.path_value,
                                                                                     currentCell.goal_value,
                                                                                     nextCell.row, nextCell.col)
            else:
                nextCell.path_value, nextCell.goal_value = self.__apply_opt(currentCell.path_value,
                                                                            currentCell.goal_value,
                                                                            nextCell.row, nextCell.col)

            if self.applyCosts:
                nextCell.path_cost = self.__apply_cost(currentCell.path_cost, nextCell.row, nextCell.col)

            if not self.explored_hashes.__contains__(nextCell.__hash__()):
                cells.append(nextCell)

        if currentCell.row > 0:
            if self.__get_opt(currentCell.row - 1, currentCell.col) != 'w':
                c = Cell(currentCell.row - 1, currentCell.col, copy.deepcopy(currentCell.table), 0, 0,
                         currentCell.path.copy())
                common_part(c)
        if currentCell.col > 0:
            if self.__get_opt(currentCell.row, currentCell.col - 1) != 'w':
                c = Cell(currentCell.row, currentCell.col - 1, copy.deepcopy(currentCell.table), 0, 0,
                         currentCell.path.copy())
                common_part(c)
        if currentCell.row < self.board.m - 1:
            if self.__get_opt(currentCell.row + 1, currentCell.col) != 'w':
                c = Cell(currentCell.row + 1, currentCell.col, copy.deepcopy(currentCell.table), 0, 0,
                         currentCell.path.copy())
                common_part(c)
        if currentCell.col < self.board.n - 1:
            if self.__get_opt(currentCell.row, currentCell.col + 1) != 'w':
                c = Cell(currentCell.row, currentCell.col + 1, copy.deepcopy(currentCell.table), 0, 0,
                         currentCell.path.copy())
                common_part(c)
        return cells

    def __apply_reversed_opt(self, path_sum, goal_value, row, col):
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

    def __apply_opt(self, path_sum, goal_value, row, col):
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

        return path_sum, goal_value

    def __apply_cost(self, current_cost, row, col):
        operation = self.__get_opt(row, col)
        amount = self.Costs[operation]
        return current_cost + amount

    def __check_goal(self, cell: Cell) -> bool:
        if (cell.path_value <= cell.goal_value and self.isBackward) or (
                cell.path_value > cell.goal_value and not self.isBackward):
            self.__print_solution(cell)
            return True
        return False

    def __calculate_f_value(self, cell: Cell) -> float:
        return cell.path_cost + self.__get_euclidean_heuristic_distance(cell.row, cell.col)

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
                if c.row == endRow and c.col == endCol and self.__check_goal(cell):
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

    def ida_star(self):
        startRow, startCol, endRow, endCol = self.source[0], self.source[1], self.goal[0], self.goal[1]
        src = Cell(startRow, startCol, [[False for _ in range(self.board.n)] for _ in range(self.board.m)],
                   self.__get_number(startRow, startCol),
                   self.__get_number(endRow, endCol), [])
        bound = self.__get_euclidean_heuristic_distance(startRow, startCol)
        while True:
            threshold = self.ida_star_search(src, bound)
            if threshold == "FOUND":
                return "FOUND"
            if threshold == INFINITY:
                print('No solution!')
                return "NOT FOUND"
            bound = threshold

    def ida_star_search(self, src: Cell, bound: float):
        startRow, startCol, endRow, endCol = self.source[0], self.source[1], self.goal[0], self.goal[1]
        src_f = self.__calculate_f_value(src)
        if src_f > bound: return src_f
        if src.row == endRow and src.col == endCol and self.__check_goal(src):
            return "FOUND"
        minimum_cost = INFINITY
        neighbors = self.__successor(src)
        for neighbor in neighbors:
            if not src.table[neighbor.row][neighbor.col]:
                threshold = self.ida_star_search(neighbor, bound)
                if threshold == "FOUND": return "FOUND"
                if threshold < minimum_cost: minimum_cost = threshold
        return minimum_cost

    def a_star(self):
        startRow, startCol, endRow, endCol = self.source[0], self.source[1], self.goal[0], self.goal[1]
        open_list = [
            Cell(startRow, startCol, [[False for _ in range(self.board.n)] for _ in range(self.board.m)],
                 self.__get_number(startRow, startCol),
                 self.__get_number(endRow, endCol), [])]

        open_list[0].path.append(open_list[0])

        while len(open_list) > 0:
            # Finding the best neighbor
            best_cell_index = -1
            best_cell_f = 9999999

            for (index, cell) in enumerate(open_list):
                cell_f = self.__calculate_f_value(open_list[index])
                if cell_f < best_cell_f:
                    best_cell_index = index
                    best_cell_f = cell_f

            cell = open_list.pop(best_cell_index)
            neighbors = self.__successor(cell)

            for neighbor in neighbors:
                # Check to see if reached the goal
                if neighbor.row == endRow and neighbor.col == endCol and self.__check_goal(cell):
                    return
                #
                # # Check to see if the cell is in closed list
                # match_in_closed_list = None
                # for exploredCell in self.explored:
                #     if exploredCell.row == neighbor.row and exploredCell.col == neighbor.col:
                #         match_in_closed_list = exploredCell
                #         continue
                # if match_in_closed_list is not None:
                #     continue

                # # Check to see if the cell is in open list
                # match_in_open_list = None
                # for openNode in open_list:
                #     if openNode.row == neighbor.row and openNode.col == neighbor.col \
                #             and openNode.path_cost <= neighbor.path_cost:
                #         match_in_open_list = openNode
                #         continue
                # if match_in_open_list is not None:
                #     continue

                if not cell.table[neighbor.row][neighbor.col]:
                    open_list.append(neighbor)

            self.explored.append(cell)

        print('no solution!!!')

    def __print_solution(self, cell: Cell):
        print(len(cell.path))

        for p in cell.path:
            print(str(p.row + 1) + ' ' + str(p.col + 1))

        if self.isBackward:
            print(str(self.source[0] + 1) + ' ' + str(self.source[1] + 1))
        else:
            print(str(self.goal[0] + 1) + ' ' + str(self.goal[1] + 1))
