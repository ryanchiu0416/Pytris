import pygame
from game_manager import GameManager


def main():
    pygame.init()
    game_manager = GameManager()

    pygame.display.set_caption("Tetris")
    pygame.draw.line(game_manager.window, (255, 255, 255), (17, 17), (17, 621), 4)  # left border
    pygame.draw.line(game_manager.window, (255, 255, 255), (16, 17), (320, 17), 4)  # top border
    pygame.draw.line(game_manager.window, (255, 255, 255), (16, 621), (320, 621), 4)  # bottom border
    pygame.draw.line(game_manager.window, (255, 255, 255), (320, 16), (320, 623), 4)  # right border

    game_manager.start_program()


if __name__ == "__main__":
    main()
