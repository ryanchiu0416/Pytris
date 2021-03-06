import pygame
from random import *
pygame.init()

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0),
                (0, 0, 255), (128, 0, 128)]

window_width = 500
window_height = 640
row = 20
col = 10
block_size = 30
top_left_x = 20
top_left_y = 20
locked_pos = {}
curr_occupy = {}

window = pygame.display.set_mode([window_width, window_height])
pygame.display.set_caption("Tetris")

font = pygame.font.Font('freesansbold.ttf', 32)
score = 0

pygame.draw.line(window, (255, 255, 255), (17, 17), (17, 621), 4) #left border
pygame.draw.line(window, (255, 255, 255), (16, 17), (320, 17), 4) #top border
pygame.draw.line(window, (255, 255, 255), (16, 621), (320, 621), 4) #bottom border
pygame.draw.line(window, (255, 255, 255), (320, 16), (320, 623), 4) #right border

grid = [ [(128,128,128) for i in range(col)] for j in range(row)] # create color grid with default gray

def show_font():
    score1 = font.render("Score:", True, (255,255,255))
    window.blit(score1, (360, 250))
    score2 = font.render(str(score), True, (255,255,255))
    window.blit(score2, (400, 300))


class Piece():
    def __init__(self, shape):
        self.x = 0
        self.y = 0
        self.rotate = 0
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
    
    def convert_shape_to_grid(self):
        list = self.shape[self.rotate % (len(self.shape))]
        for row in range(len(list)):
            for col in range(len(list[row])):
                if list[row][col] == '0':
                    curr_occupy[(self.y + row, self.x + col)] = self.color

def add_locked(key, color):
    locked_pos[key] = color

def fill_currOccupy():
    for pos in curr_occupy:
        if pos[0] < row and pos[0] >= 0 and pos[1] < col and pos[1] >= 0:
            grid[pos[0]][pos[1]] = curr_occupy.get(pos)

def reset_currOccupy():
    for pos in curr_occupy:
        if pos[0] < row and pos[0] >= 0 and pos[1] < col and pos[1] >= 0:
            grid[pos[0]][pos[1]] = (128,128,128)
    curr_occupy.clear()

def update_grid(occupy):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (row, col) in occupy:
                grid[row][col] = occupy[(row, col)]

def draw_grid():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            fill = 1 
            if grid[row][col] != (128, 128, 128):
                fill = 0
            pygame.draw.rect(window, grid[row][col],
                    (top_left_x + col * block_size, top_left_y + row * block_size, block_size,
                     block_size), fill)

def leftBoundCheck():
    for pos in curr_occupy:
        if pos[1] < 0:
            return True
        return False

def rightBoundCheck():
    for pos in curr_occupy:
        if pos[1] >= col: #col = 10
            return True
        return False

def rotateLeftCheck():
    count = 0
    for pos in curr_occupy:
        if pos[1] < 0:
            count += 1
    return count

def rotateRightCheck():
    count = 0
    for pos in curr_occupy:
        if pos[1] >= col: #col = 10
            count += 1
    return count

def lockCheck():
    for pos in curr_occupy:
        if pos[0] == row - 1:
            return True
        if pos[0] + 1 < row and grid[pos[0] + 1][pos[1]] != (128,128,128):
            return True
    return False

def row_check(row):
    colored_count = 0
    print("row", row)
    print("grid[row]", len(grid[row]))
    for i in range(len(grid[row])):
        if grid[row][i] != (128,128,128):
            colored_count += 1

    if (colored_count == 10): # move every row's value to its next row
        return True
    return False

def update_locked_pos(row):
    keys_to_remove = []
    keys_to_change = []
    for pos in locked_pos:
        if pos[0] == row:
            keys_to_remove.append(pos)
        if pos[0] < row:
            keys_to_change.append(pos)
    
    for key in keys_to_remove:
        locked_pos.pop(key)
    for key in keys_to_change:
        locked_pos[key[0]+1, key[1]] = locked_pos.pop(key)
    


def removeRow(row):
    emptyRow = [(128,128,128) for i in range(col)]
    grid.pop(row)
    grid.insert(0, emptyRow)

def main():
    global curr_occupy
    global score
    running = True
    

    pygame.key.set_repeat(True)
    currentPiece = Piece(shapes[randrange(len(shapes))])
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.22
    

    while running:
        fall_time += clock.get_rawtime()
        clock.tick()
        hasDropped = False

        if fall_time/1000 > fall_speed:
            fall_time = 0
            currentPiece.y += 1
            hasDropped = True
            if currentPiece.y >= row:
                currentPiece.y -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1
                if event.key == pygame.K_RIGHT:
                    currentPiece.x += 1
                if event.key == pygame.K_UP:
                    currentPiece.rotate += 1
                if event.key == pygame.K_DOWN and hasDropped is False:
                    currentPiece.y += 1
        window.fill((0,0,0))
        reset_currOccupy()

        currentPiece.convert_shape_to_grid()
        if leftBoundCheck():
            curr_occupy.clear()
            currentPiece.x += 1
            currentPiece.convert_shape_to_grid()
        if rightBoundCheck():
            curr_occupy.clear()
            currentPiece.x -= 1
            currentPiece.convert_shape_to_grid()
        while rotateLeftCheck() > 0:
            curr_occupy.clear()
            currentPiece.x += 1
            currentPiece.convert_shape_to_grid()
        while rotateRightCheck() > 0:
            curr_occupy.clear()
            currentPiece.x -= 1
            currentPiece.convert_shape_to_grid()
        rows_to_check = set()
        if lockCheck():
            for pos in curr_occupy:
                if pos[0] < row and pos[0] >= 0 and pos[1] < col and pos[1] >= 0:
                    add_locked((pos[0], pos[1]), curr_occupy[(pos[0], pos[1])])
                    rows_to_check.add(pos[0])
            curr_occupy.clear()
            currentPiece = Piece(shapes[randrange(len(shapes))])
            currentPiece.convert_shape_to_grid()
    
        update_grid(locked_pos)

        # for a more continuous visual when clearing lines. 
        draw_grid()
        pygame.display.update()
        #

        # iterate over a set of "rows" (from locked) to check if there's a row that can be removed from grid
        for r in rows_to_check:
            if row_check(r) is True:
                removeRow(r)
                update_locked_pos(r)
                score += 10
        rows_to_check.clear()

        fill_currOccupy()

        draw_grid()
        show_font()
        pygame.display.update()

    pygame.quit()

main()

# Done with removing rows and stacking up. In progress for the rest such as
# game over, etc.