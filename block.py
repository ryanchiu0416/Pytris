from abc import ABC, abstractmethod


class Block(ABC):

    def __init__(self):
        self.col = 0  # x
        self.row = 0  # y
        self.MAX_COL = 10
        self.MAX_ROW = 20
        self.rotate_count = 0
        self.occupy_positions = {}

    @property
    @abstractmethod
    def shape(self):
        return self.shape

    @property
    @abstractmethod
    def color(self):
        return self.color

    def move_left(self):
        self.col -= 1

    def move_right(self):
        self.col += 1

    def move_down(self):
        self.row += 1

    def move_up(self):
        self.row -= 1


    def rotate(self):
        self.rotate_count += 1

    def draw_to_grid(self):
        pass

    def check_movable(self):
        while self._is_left_out_of_bounds():
            self.occupy_positions.clear()
            self.col += 1
            self.convert_shape_to_grid()
        while self._is_right_out_of_bounds():
            self.occupy_positions.clear()
            self.col -= 1
            self.convert_shape_to_grid()

    def convert_shape_to_grid(self):
        curr_shape = self.shape[self.rotate_count % (len(self.shape))]
        for r in range(len(curr_shape)):
            for c in range(len(curr_shape[r])):
                if curr_shape[r][c] == '0':
                    self.occupy_positions[(self.row + r, self.col + c)] = self.color

    def _is_left_out_of_bounds(self):
        for (row_idx, col_idx) in self.occupy_positions.keys():
            if col_idx < 0:
                return True
        return False

    def _is_right_out_of_bounds(self):
        for (row_idx, col_idx) in self.occupy_positions.keys():
            if col_idx >= self.MAX_COL:  # col = 10
                return True
        return False

    def is_locked_in_position(self, grid):
        for (row, col) in self.occupy_positions:
            if row == self.MAX_ROW - 1 or (row < self.MAX_ROW - 1 and grid[row + 1][col] != (128, 128, 128)):
                return True
        return False


class O_Block(Block):
    def __init__(self):
        super().__init__()

    @property
    def shape(self):
        return [[
                 '.00..',
                 '.00..',
                 '.....']]

    @property
    def color(self):
        return 255, 255, 0


class L_Block(Block):
    def __init__(self):
        super().__init__()

    @property
    def color(self):
        return 0, 0, 255

    @property
    def shape(self):
        return [[
                 '...0.',
                 '.000.',
                 '.....',
                 '.....'],
                [
                 '..0..',
                 '..0..',
                 '..00.',
                 '.....'],
                [
                 '.000.',
                 '.0...',
                 '.....'],
                [
                 '.00..',
                 '..0..',
                 '..0..',
                 '.....']]


class J_Block(Block):
    def __init__(self):
        super().__init__()

    @property
    def color(self):
        return 255, 165, 0

    @property
    def shape(self):
        return [[
                 '.0...',
                 '.000.',
                 '.....',
                 '.....'],
                [
                 '..00.',
                 '..0..',
                 '..0..',
                 '.....'],
                [
                 '.000.',
                 '...0.',
                 '.....'],
                [
                 '..0..',
                 '..0..',
                 '.00..',
                 '.....']]


class I_Block(Block):
    def __init__(self):
        super().__init__()

    @property
    def color(self):
        return 0, 255, 255

    @property
    def shape(self):
        return [['..0..',
                 '..0..',
                 '..0..',
                 '..0..',
                 '.....'],
                [
                 '0000.',
                 '.....',
                 '.....',
                 '.....']]


class S_Block(Block):
    def __init__(self):
        super().__init__()

    @property
    def color(self):
        return 0, 255, 0

    @property
    def shape(self):
        return [[
                 '..00..',
                 '.00...',
                 '.....'],
                [
                 '..0..',
                 '..00.',
                 '...0.',
                 '.....']]


class Z_Block(Block):
    def __init__(self):
        super().__init__()

    @property
    def color(self):
        return 255, 0, 0

    @property
    def shape(self):
        return [[
                 '.00..',
                 '..00.',
                 '.....'],
                [
                 '..0..',
                 '.00..',
                 '.0...',
                 '.....']]



class T_Block(Block):
    def __init__(self):
        super().__init__()

    @property
    def color(self):
        return 128, 0, 128

    @property
    def shape(self):
        return [[
                 '..0..',
                 '.000.',
                 '.....',
                 '.....'],
                [
                 '..0..',
                 '..00.',
                 '..0..',
                 '.....'],
                [
                 '.000.',
                 '..0..',
                 '.....'],
                [
                 '..0..',
                 '.00..',
                 '..0..',
                 '.....']]
