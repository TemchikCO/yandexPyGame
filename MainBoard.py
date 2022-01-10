import pygame
import data


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = min((data.size[0] - 2 * self.left) // self.width - 10, (data.size[1] - 2 * self.top) // self.height)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = min((data.size[0] - 2 * self.left) // self.width - 10, (data.size[1] - 2 * self.top) // self.height)

    def render(self, surface):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(surface, 'white', (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                    self.cell_size, self.cell_size), 1 if self.board[i][j] == 0 else 0)

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords is None:
            return
        self.on_click(cell_coords)

    def get_cell(self, mouse_pos):
        board_width = self.width * self.cell_size
        board_height = self.height * self.cell_size
        if self.left < mouse_pos[0] < self.left + board_width:
            if self.top < mouse_pos[1] < self.top + board_height:
                cell_coords = (mouse_pos[1] - self.left) // self.cell_size, \
                              (mouse_pos[0] - self.top) // self.cell_size
                return cell_coords
        return None

    def on_click(self, cell_coords):
        self.i = cell_coords[0]
        self.j = cell_coords[1]
        self.board[self.i][self.j] = 0 if self.board[self.i][self.j] == 1 else 1
        for y in range(self.height):
            self.board[y][self.j] = 0 if self.board[y][self.j] == 1 else 1
        for x in range(self.width):
            self.board[self.i][x] = 0 if self.board[self.i][x] == 1 else 1