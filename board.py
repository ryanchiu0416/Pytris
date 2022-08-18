class Board:
    def __init__(self):
        self.ROW = 20
        self.COL = 10
        self.score = 0
        self.grid = [[(128, 128, 128) for i in range(self.COL)] for j in range(self.ROW)]
        self.locked_pos = {}

    def reset_grid(self):
        self.grid = self.grid = [[(128, 128, 128) for i in range(self.COL)] for j in range(self.ROW)]

    def add_score(self, increment):
        self.score += increment

    def add_locked_position(self, pos_key, color):
        self.locked_pos[pos_key] = color

    def update_locked_pos(self, current_row_idx):
        keys_to_remove = []
        keys_to_modify_position = []
        for (row, col) in self.locked_pos:
            if row == current_row_idx:
                keys_to_remove.append((row, col))
            elif row < current_row_idx:
                keys_to_modify_position.append((row, col))

        for (r, c) in keys_to_remove:
            self.locked_pos.pop((r, c))
        for (r, c) in keys_to_modify_position:
            self.locked_pos[r + 1, c] = self.locked_pos.pop((r, c))

    # for grid operations
    def reset_grid_for_current_piece(self, piece):
        for (row, cow) in piece.occupy_positions:
            if self.ROW > row >= 0 and self.COL > cow >= 0:
                self.grid[row][cow] = (128, 128, 128)

    def update_grid_from(self, positions_map):
        for (row, col) in positions_map:
            self.grid[row][col] = positions_map[(row, col)]

    def is_removable_row(self, row_idx):
        occupied_cell_count = 0
        for i in range(len(self.grid[row_idx])):
            if self.grid[row_idx][i] != (128, 128, 128):
                occupied_cell_count += 1
        return occupied_cell_count == 10

    def remove_curr_row(self, row):
        empty_row = [(128, 128, 128) for i in range(self.COL)]
        self.grid.pop(row)
        self.grid.insert(0, empty_row)

    def clear_rows_and_get_scores(self, rows_to_check):
        curr_round_score = 0
        for r in rows_to_check:
            if self.is_removable_row(r) is True:
                self.remove_curr_row(r)
                self.update_locked_pos(r)
                curr_round_score += 10
        self.score += curr_round_score
