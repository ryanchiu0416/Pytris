import pygame
import random


from block import *
from board import *


class GameManager:
    def __init__(self):
        self.window_width = 500
        self.window_height = 640
        self.block_size = 30
        self.top_left_x = 20
        self.top_left_y = 20
        self.window = pygame.display.set_mode([self.window_width, self.window_height])
        self.font = pygame.font.Font('freesansbold.ttf', 32)


    def start_program(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.window_width / 2 + 90 <= mouse[0] <= self.window_width / 2 + 230 and \
                            self.window_height / 2 <= mouse[1] <= self.window_height / 2 + 40:
                        self.start_game()
                    elif self.window_width / 2 + 90 <= mouse[0] <= self.window_width / 2 + 230 and \
                            self.window_height / 2 + 100 <= mouse[1] <= self.window_height / 2 + 140:
                        pygame.quit()

            mouse = pygame.mouse.get_pos()
            self.show_buttons(mouse)


    def start_game(self):
        running = True
        blocks = [O_Block, L_Block, J_Block, I_Block, S_Block, Z_Block, T_Block]

        pygame.key.set_repeat(100, 100)
        board = Board()
        chosen_block = random.choice(blocks)
        current_piece = chosen_block()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.22

        while running:
            fall_time += clock.get_rawtime()
            clock.tick()
            has_moved_down = False

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                current_piece.move_down()
                has_moved_down = True
                if current_piece.row >= board.ROW:
                    current_piece.move_up()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.move_left()
                    if event.key == pygame.K_RIGHT:
                        current_piece.move_right()
                    if event.key == pygame.K_UP:
                        current_piece.rotate()
                    if event.key == pygame.K_DOWN and has_moved_down is False:
                        current_piece.move_down()



            self.window.fill((0, 0, 0))
            board.reset_grid_for_current_piece(current_piece)

            current_piece.occupy_positions.clear()
            current_piece.convert_shape_to_grid()

            for key in current_piece.occupy_positions:
                if key in board.locked_pos:
                    running = False
                    board.reset_grid()
                    current_piece.occupy_positions.clear()
                    break

            current_piece.check_movable()

            if current_piece.is_locked_in_position(board.grid):
                # only need to check if there's row to remove when current block piece is locked in position
                rows_to_check = set()
                for (row, col) in current_piece.occupy_positions:
                    board.add_locked_position((row, col), current_piece.occupy_positions[(row, col)])
                    rows_to_check.add(row)
                board.update_grid_from(board.locked_pos)

                # clear rows
                board.clear_rows_and_get_scores(rows_to_check)
                rows_to_check.clear()

                # create new piece
                chosen_block = random.choice(blocks)
                current_piece = chosen_block()
            else:
                board.update_grid_from(current_piece.occupy_positions)

            self.draw_grid_on_window(board.grid)
            self.show_score(board.score)
            pygame.display.update()

    def show_score(self, score):
        score1 = self.font.render("Score:", True, (255, 255, 255))
        self.window.blit(score1, (360, 200))
        score2 = self.font.render(str(score), True, (255, 255, 255))
        self.window.blit(score2, (400, 250))



    def draw_grid_on_window(self, grid):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                to_fill = grid[row][col] != (128, 128, 128)
                pygame.draw.rect(self.window, grid[row][col],
                                 (self.top_left_x + col * self.block_size, self.top_left_y + row * self.block_size,
                                  self.block_size,
                                  self.block_size), 0 if to_fill else 1)

    def show_buttons(self, mouse):
        if self.window_width / 2 + 90 <= mouse[0] <= self.window_width / 2 + 230 and self.window_height / 2 <= \
                mouse[1] <= self.window_height / 2 + 40:
            pygame.draw.rect(self.window, (170, 170, 170),
                             [self.window_width / 2 + 90, self.window_height / 2, 140, 40])
        else:
            pygame.draw.rect(self.window, (100, 100, 100),
                             [self.window_width / 2 + 90, self.window_height / 2, 140, 40])

        start_text = self.font.render('Start', True, (255, 255, 255))
        self.window.blit(start_text, (self.window_width / 2 + 125, self.window_height / 2))

        if self.window_width / 2 + 90 <= mouse[0] <= self.window_width / 2 + 230 \
                and self.window_height / 2 + 100 <= mouse[1] <= self.window_height / 2 + 140:
            pygame.draw.rect(self.window, (170, 170, 170),
                             [self.window_width / 2 + 90, self.window_height / 2 + 100, 140, 40])
        else:
            pygame.draw.rect(self.window, (100, 100, 100),
                             [self.window_width / 2 + 90, self.window_height / 2 + 100, 140, 40])

        start_text = self.font.render('Quit', True, (255, 255, 255))
        self.window.blit(start_text, (self.window_width / 2 + 125, self.window_height / 2 + 100))

        pygame.display.update()
