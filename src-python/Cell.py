class Cell:
    def __init__(self, row: int, col: int, table: list, path_value: int, goal_value: int, path: list,
                 path_cost: int = 0):
        self.row = row
        self.col = col
        self.path_value = path_value
        self.path_cost = path_cost
        self.path = path
        self.goal_value = goal_value
        self.table = table
        self.table[row][col] = True

    def __eq__(self, other):
        if type(other) != Cell:
            return False
        if other.row == self.row and other.col == self.col:
            return True
        return False

    def __hash__(self):
        return ','.join(str(item) for innerlist in self.table for item in innerlist) + '@@@' + str(
            self.row) + ' ' + str(self.col) + '###' + str(self.path_value) + ' ' + str(self.goal_value)

    def __str__(self):
        return f'({self.row + 1}, {self.col + 1})'
