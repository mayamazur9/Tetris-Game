import pygame
import sys

X=350
Y=400
grid_width=200
block_size=20

tetris_blue= (26, 41, 107)
white= (255, 255, 255)
dark_gray= (128, 128, 128)

grid_color= (38, 56, 138)

#brown 
cyan= (255, 255, 255)
#pink
yellow= (199, 255, 130)
#teal
purple= (194, 242, 208)
#yellow
orange= (253, 245, 201)
#orange
blue= (255, 203, 133)
#brown
lime_green= (107, 62, 38)
#pink
red= (255, 197, 217)
#teal
pink= (194, 242, 208)

shape= {
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'I': [(0, 0), (1, 0), (2, 0), (3, 0)],
    'S': [(1, 1), (1, 0), (2, 0), (2, 1)],
    'Z': [(0, 1), (1, 1), (1, 0), (2, 0)],
    'L': [(0, 2), (1, 2), (2, 2), (2, 1)],
    'J': [(0, 1), (0, 2), (1, 2), (2, 2)],
    'T': [(0, 1), (1, 1), (1, 0), (2, 1)]
}

shape_color= {
    'O': yellow,
    'I': cyan,
    'S': red,
    'Z': lime_green,
    'L': orange,
    'J': pink,
    'T': purple
}


def draw_grid(screen):
    for x in range(0, grid_width, block_size):
        for y in range(0, Y, block_size):
            rect= pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, grid_color, rect, 1)