import random
from copy import deepcopy
from typing import List

import pygame
import math

from color import RandomColorDictionary


class GridClass:

    def __init__(self, thread):

        self.neighbourhood_type = 'Moore'
        self.grain_growth = False
        self.bound_choice = 'Periodical'

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = 7
        self.HEIGHT = 7
        self.GROWTH_SPEED = 60

        # This sets the margin between each cell
        self.MARGIN = 1
        self.grid = []
        self.thread = thread

    def init_grid(self, x, y):
        self.GRID_SIZE_X = x
        self.GRID_SIZE_Y = y
        for row in range(self.GRID_SIZE_X):
            self.grid.append([])
            for column in range(self.GRID_SIZE_Y):
                self.grid[row].append(0)

    def clean_grid(self):
        for row in range(self.GRID_SIZE_X):
            for column in range(self.GRID_SIZE_Y):
                self.grid[row][column] = 0

    def change_neighbour(self, neighbour):
        self.neighbourhood_type = neighbour

    def set_grain_growth(self, grain_growth_bool):
        self.grain_growth = grain_growth_bool

    def randomize_cells(self, value):
        color_dict = RandomColorDictionary()
        if value > self.GRID_SIZE_X * self.GRID_SIZE_Y:
            value = self.GRID_SIZE_X * self.GRID_SIZE_Y
        for i in range(value + 1):
            random_row = random.randint(0, self.GRID_SIZE_X - 1)
            random_column = random.randint(0, self.GRID_SIZE_Y - 1)
            random_color = random.choice(list(color_dict.colors.keys()))
            self.grid[random_row][random_column] = random_color

    def randomize_radius_cells(self, radius, cell_amount):

        if cell_amount <= 0 or (radius > self.GRID_SIZE_X or radius > self.GRID_SIZE_Y):
            return

        color_dict = RandomColorDictionary()
        already_placed_circles = []
        radius_squared = radius ** 2

        random_row = random.randint(0, self.GRID_SIZE_X - 1)
        random_column = random.randint(0, self.GRID_SIZE_Y - 1)
        already_placed_circles.append([random_row, random_column])

        ERROR_THRESHOLD = 0
        ERROR_THRESHOLD_LIMIT = 100000

        while len(already_placed_circles) != cell_amount:
            inside_circle = False
            random_row = random.randint(0, self.GRID_SIZE_X - 1)
            random_column = random.randint(0, self.GRID_SIZE_Y - 1)

            for cell in already_placed_circles:
                circle_row = cell[0]
                circle_column = cell[1]
                distance_squared = (random_row - circle_row) ** 2 + (random_column - circle_column) ** 2
                if distance_squared <= radius_squared:
                    inside_circle = True
                    break

            if not inside_circle:
                already_placed_circles.append([random_row, random_column])
            else:
                ERROR_THRESHOLD += 1
                if ERROR_THRESHOLD == ERROR_THRESHOLD_LIMIT:
                    break

        for i in range(0, len(already_placed_circles)):
            row = already_placed_circles[i][0]
            column = already_placed_circles[i][1]
            color = random.choice(list(color_dict.colors.keys()))
            self.grid[row][column] = color

    def evenly_cells(self, cell_amount):
        color_dict = RandomColorDictionary()
        ratio = self.GRID_SIZE_X / self.GRID_SIZE_Y
        sqrt_cell_amount = math.ceil(math.sqrt(int(cell_amount)))
        points_x = ratio * sqrt_cell_amount
        points_y = sqrt_cell_amount / ratio
        step_y = int(self.GRID_SIZE_Y / (points_y + 1))
        step_x = int(self.GRID_SIZE_X / (points_x + 1))
        for j in range(0, self.GRID_SIZE_Y, step_y):
            for i in range(0, self.GRID_SIZE_X, step_x):
                row = i
                column = j
                color = random.choice(list(color_dict.colors.keys()))
                self.grid[row][column] = color


class PyGameWindow:

    def __init__(self, grid):
        pygame.init()
        self.WINDOW_SIZE = [grid.GRID_SIZE_Y * (grid.HEIGHT + grid.MARGIN) + grid.MARGIN,
                            grid.GRID_SIZE_X * (grid.WIDTH + grid.MARGIN) + grid.MARGIN]
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        pygame.display.set_caption("Grain Growth")
        self.done = False
        self.color_class = RandomColorDictionary()
        self.gridClass = grid

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.main_loop()

    def determine_color(self, array_of_neighbours):
        color_dict = {}
        for i in range(0, len(array_of_neighbours)):
            if array_of_neighbours[i] != 0:
                color_dict[array_of_neighbours[i]] = color_dict.get(array_of_neighbours[i], 0) + 1

        if color_dict.__len__() == 0:
            return 0
        else:
            return max(color_dict)

    def finish_drawing(self, conditions: List, old_grid: List,
                       row: int, column: int) -> None:
        neighbours = []
        for possible_neigh in conditions:
            is_neighbour = possible_neigh[0]
            if is_neighbour:
                x = possible_neigh[1][0]
                y = possible_neigh[1][1]
                neighbours.append(old_grid[x][y])

        color_to_paint = self.determine_color(neighbours)
        self.gridClass.grid[row][column] = color_to_paint

    def moore_growth(self, old_grid, row, column):
        moores = [(column + 1 < self.gridClass.GRID_SIZE_Y,                                          (row,     column + 1)),
                  (row - 1 >= 0 and column + 1 < self.gridClass.GRID_SIZE_Y,                         (row - 1, column + 1)),
                  (row - 1 >= 0,                                                                     (row - 1, column)),
                  (row - 1 >= 0 and column - 1 >= 0,                                                 (row - 1, column - 1)),
                  (column - 1 >= 0,                                                                  (row,     column - 1)),
                  (row + 1 < self.gridClass.GRID_SIZE_X and column - 1 >= 0,                         (row + 1, column - 1)),
                  (row + 1 < self.gridClass.GRID_SIZE_X,                                             (row + 1, column)),
                  (row + 1 < self.gridClass.GRID_SIZE_X and column + 1 < self.gridClass.GRID_SIZE_Y, (row + 1, column + 1))]

        if self.gridClass.bound_choice == 'Periodical':
            periodical_moores = [(column + 1 == self.gridClass.GRID_SIZE_Y,                                           (row, 0)),
                                 (row - 1 == -1 and column + 1 == self.gridClass.GRID_SIZE_Y,                         (self.gridClass.GRID_SIZE_X - 1, 0)),
                                 (row - 1 == -1,                                                                      (self.gridClass.GRID_SIZE_X - 1, column)),
                                 (row - 1 == -1 and column - 1 == -1,                                                 (self.gridClass.GRID_SIZE_X - 1, self.gridClass.GRID_SIZE_Y - 1)),
                                 (column - 1 == -1,                                                                   (row, self.gridClass.GRID_SIZE_Y - 1)),
                                 (row + 1 == self.gridClass.GRID_SIZE_X and column - 1 == -1,                         (0, self.gridClass.GRID_SIZE_Y - 1)),
                                 (row + 1 == self.gridClass.GRID_SIZE_X,                                              (0, column)),
                                 (row + 1 == self.gridClass.GRID_SIZE_X and column + 1 == self.gridClass.GRID_SIZE_Y, (0, 0))]
            moores += periodical_moores

        self.finish_drawing(conditions=moores, old_grid=old_grid, row=row, column=column)

    def von_neumann_growth(self, old_grid, row, column):
        von_neumanns = [(column + 1 < self.gridClass.GRID_SIZE_Y, (row,    column + 1)),
                        (row - 1 >= 0,                            (row - 1,column)),
                        (column - 1 >= 0,                         (row,    column - 1)),
                        (row + 1 < self.gridClass.GRID_SIZE_X,    (row + 1,column))]

        if self.gridClass.bound_choice == 'Periodical':
            perodical_neumnas = [(column + 1 == self.gridClass.GRID_SIZE_Y, (row, 0)),
                                 (row - 1 == -1, (self.gridClass.GRID_SIZE_X - 1, column)),
                                 (column - 1 == -1, (row, self.gridClass.GRID_SIZE_Y - 1)),
                                 (row + 1 == self.gridClass.GRID_SIZE_X, (0, column))]
            von_neumanns += perodical_neumnas

        self.finish_drawing(conditions=von_neumanns, old_grid=old_grid, row=row, column=column)

    def hexagonal_right_growth(self, old_grid, row, column):
        hexagonal_rights = [(row - 1 >= 0 and column + 1 < self.gridClass.GRID_SIZE_Y,  (row - 1, column + 1)),
                            (column + 1 < self.gridClass.GRID_SIZE_Y,                   (row,     column + 1)),
                            (row - 1 >= 0,                                              (row - 1, column)),
                            (column - 1 >= 0,                                           (row,     column - 1)),
                            (row + 1 < self.gridClass.GRID_SIZE_X and column - 1 >= 0,  (row + 1, column - 1)),
                            (row + 1 < self.gridClass.GRID_SIZE_X,                      (row + 1, column))]

        if self.gridClass.bound_choice == 'Periodical':
            hexagonal_rights_periodicals = [(row - 1 == -1 and column + 1 == self.gridClass.GRID_SIZE_Y,    (self.gridClass.GRID_SIZE_X - 1, 0)),
                                            (column + 1 == self.gridClass.GRID_SIZE_Y,                      (row, 0)),
                                            (row - 1 == -1,                                                 (self.gridClass.GRID_SIZE_X - 1, column)),
                                            (column - 1 == -1,                                              (row, self.gridClass.GRID_SIZE_Y - 1)),
                                            (row + 1 == self.gridClass.GRID_SIZE_X and column - 1 == -1,    (0, self.gridClass.GRID_SIZE_Y - 1)),
                                            (row + 1 == self.gridClass.GRID_SIZE_X,                         (0, column))]

            hexagonal_rights += hexagonal_rights_periodicals

        self.finish_drawing(conditions=hexagonal_rights, old_grid=old_grid, row=row, column=column)

    def hexagonal_left_growth(self, old_grid, row, column):
        hexagonal_lefties = [(row + 1 < self.gridClass.GRID_SIZE_X,                                             (row + 1,column)),
                             (column + 1 < self.gridClass.GRID_SIZE_Y,                                          (row,    column + 1)),
                             (row - 1 >= 0,                                                                     (row - 1,column)),
                             (column - 1 >= 0,                                                                  (row,    column - 1)),
                             (row - 1 >= 0 and column - 1 >= 0,                                                 (row - 1,column - 1)),
                             (row + 1 < self.gridClass.GRID_SIZE_X and column + 1 < self.gridClass.GRID_SIZE_Y, (row + 1,column + 1))]

        if self.gridClass.bound_choice == 'Periodical':
            hexagonal_lefties_periodicals = [(row + 1 == self.gridClass.GRID_SIZE_X,                            (0,column)),
                                             (column + 1 == self.gridClass.GRID_SIZE_Y,                         (row,0)),
                                             (row - 1 == -1,                                                    (self.gridClass.GRID_SIZE_X - 1, column)),
                                             (column - 1 == -1,                                                 (row,self.gridClass.GRID_SIZE_Y - 1)),
                                             (row - 1 == -1 and column - 1 == -1,                               (self.gridClass.GRID_SIZE_X - 1,self.gridClass.GRID_SIZE_Y - 1)),
                                             (row + 1 == self.gridClass.GRID_SIZE_X and column + 1 == self.gridClass.GRID_SIZE_Y,   (0,0))]

            hexagonal_lefties += hexagonal_lefties_periodicals

        self.finish_drawing(conditions=hexagonal_lefties, old_grid=old_grid, row=row, column=column)


    def hexagonal_random_growth(self, old_grid, row, column):
        hexagonal = random.choice([self.hexagonal_left_growth, self.hexagonal_right_growth])
        hexagonal(old_grid, row, column)

    def pentagonal_random_growth(self, old_grid, row, column):
        random_int = random.randint(1, 4)
        if random_int == 1:
            down = [(row + 1 < self.gridClass.GRID_SIZE_X,                     (row + 1, column)),
                    (row - 1 >= 0,                                             (row - 1, column)),
                    (column - 1 >= 0,                                          (row,     column - 1)),
                    (row + 1 < self.gridClass.GRID_SIZE_X and column - 1 >= 0, (row + 1, column - 1)),
                    (row - 1 >= 0 and column - 1 >= 0,                         (row - 1, column - 1))]

            if self.gridClass.bound_choice == 'Periodical':
                down_perodicals = [(row + 1 == self.gridClass.GRID_SIZE_X,                       (0, column)),
                                   (row - 1 == -1,                                               (self.gridClass.GRID_SIZE_X - 1, column)),
                                   (column - 1 == -1,                                            (row, self.gridClass.GRID_SIZE_Y - 1)),
                                   (row + 1 == self.gridClass.GRID_SIZE_X and column - 1 == -1,  (0, self.gridClass.GRID_SIZE_Y - 1)),
                                   (row - 1 == -1 and column - 1 == -1,                          (self.gridClass.GRID_SIZE_X - 1, self.gridClass.GRID_SIZE_Y - 1))]

                down += down_perodicals

                self.finish_drawing(conditions=down, old_grid=old_grid, row=row, column=column)

        elif random_int == 2:
            lefts = [(row - 1 >= 0,                                             (row - 1, column)),
                     (column - 1 >= 0,                                          (row,     column - 1)),
                     (column + 1 < self.gridClass.GRID_SIZE_Y,                  (row,     column + 1)),
                     (row - 1 >= 0 and column - 1 >= 0,                         (row - 1, column - 1)),
                     (row - 1 >= 0 and column + 1 < self.gridClass.GRID_SIZE_Y, (row - 1, column + 1))]

            if self.gridClass.bound_choice == 'Perodical':
                lefts_perodicals = [(row - 1 == -1,                                                 (self.gridClass.GRID_SIZE_X - 1, column)),
                                    (column - 1 == -1,                                              (row, self.gridClass.GRID_SIZE_Y - 1)),
                                    (column + 1 == self.gridClass.GRID_SIZE_Y,                      (row, 0)),
                                    (row - 1 == -1 and column - 1 == -1,                            (self.gridClass.GRID_SIZE_X - 1, self.gridClass.GRID_SIZE_Y - 1)),
                                    (row - 1 == -1 and column + 1 == self.gridClass.GRID_SIZE_Y,    (self.gridClass.GRID_SIZE_X - 1, 0))]

                lefts += lefts_perodicals

            self.finish_drawing(conditions=lefts, old_grid=old_grid, row=row, column=column)


        elif random_int == 3:
            uppers = [(row - 1 >= 0,                                                                            (row - 1,column)),
                      (row + 1 < self.gridClass.GRID_SIZE_X,                                                    (row + 1,column)),
                      (column + 1 < self.gridClass.GRID_SIZE_Y,                                                 (row,    column + 1)),
                      (row - 1 >= 0 and column + 1 < self.gridClass.GRID_SIZE_Y,                                (row - 1,column + 1)),
                      (row + 1 < self.gridClass.GRID_SIZE_X and column + 1 < self.gridClass.GRID_SIZE_X,        (row + 1,column + 1))]

            if self.gridClass.bound_choice == 'Periodical':
                uppers_perodicals = [(row - 1 == -1,                                                                        (self.gridClass.GRID_SIZE_X - 1,column)),
                                     (row + 1 == self.gridClass.GRID_SIZE_X,                                                (0,column)),
                                     (column + 1 == self.gridClass.GRID_SIZE_Y,                                             (row,0)),
                                     (row - 1 == -1 and column + 1 == self.gridClass.GRID_SIZE_Y,                           (self.gridClass.GRID_SIZE_X - 1,0)),
                                     (row + 1 == self.gridClass.GRID_SIZE_X and column + 1 == self.gridClass.GRID_SIZE_X,   (0,0)),]

                uppers += uppers_perodicals

                self.finish_drawing(conditions=uppers, old_grid=old_grid, row=row, column=column)

        elif random_int == 4:

            righties = [(row + 1 < self.gridClass.GRID_SIZE_X and column + 1 < self.gridClass.GRID_SIZE_Y,  (row + 1,column + 1)),
                        (column + 1 < self.gridClass.GRID_SIZE_Y,                                           (row,    column +1)),
                        (row + 1 < self.gridClass.GRID_SIZE_X,                                              (row + 1,column)),
                        (row + 1 < self.gridClass.GRID_SIZE_X and column - 1 >= 0,                          (row + 1,column - 1)),
                        (column - 1 >= 0,                                                                   (row,    column - 1))]

            if self.gridClass.bound_choice == 'Periodical':
                righties_periodical = [(row + 1 == self.gridClass.GRID_SIZE_X and column + 1 == self.gridClass.GRID_SIZE_X, (0,0)),
                                       (column + 1 == self.gridClass.GRID_SIZE_Y,                                           (row,0)),
                                       (row + 1 == self.gridClass.GRID_SIZE_X,                                              (0,column)),
                                       (row + 1 == self.gridClass.GRID_SIZE_X and column - 1 == -1,                         (0,self.gridClass.GRID_SIZE_Y - 1)),
                                       (column - 1 == -1,                                                                   (row,self.gridClass.GRID_SIZE_Y - 1))]

                righties += righties_periodical

            self.finish_drawing(conditions=righties, old_grid=old_grid, row=row, column=column)

    def close(self):
        self.done = True
        self.gridClass.thread.grid = None
        del self.gridClass
        pygame.quit()
        exit()

    def main_loop(self):
        # -------- Main Program Loop -----------
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (self.gridClass.WIDTH + self.gridClass.MARGIN)
                    row = pos[1] // (self.gridClass.HEIGHT + self.gridClass.MARGIN)
                    self.gridClass.grid[row][column] = random.choice(list(self.color_class.colors))

            if self.gridClass.grain_growth:
                old_grid = deepcopy(self.gridClass.grid)
                for row in range(self.gridClass.GRID_SIZE_X):
                    for column in range(self.gridClass.GRID_SIZE_Y):
                        if old_grid[row][column] == 0:
                            if self.gridClass.neighbourhood_type == 'Moore':
                                self.moore_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Von Neumann':
                                self.von_neumann_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Hexagonal Right':
                                self.hexagonal_right_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Hexagonal Left':
                                self.hexagonal_left_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Random Hexagonal':
                                self.hexagonal_random_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Random Pentagonal':
                                self.pentagonal_random_growth(old_grid, row, column)
            self.screen.fill(self.color_class.colors['black'])

            # Draw the grid
            for row in range(self.gridClass.GRID_SIZE_X):
                for column in range(self.gridClass.GRID_SIZE_Y):
                    color = self.color_class.colors['white']
                    if self.gridClass.grid[row][column] != 0:
                        color = self.color_class.colors[self.gridClass.grid[row][column]]
                    pygame.draw.rect(self.screen,
                                     color,
                                     [(self.gridClass.MARGIN + self.gridClass.WIDTH) * column + self.gridClass.MARGIN,
                                      (self.gridClass.MARGIN + self.gridClass.HEIGHT) * row + self.gridClass.MARGIN,
                                      self.gridClass.WIDTH,
                                      self.gridClass.HEIGHT])
            self.clock.tick(self.gridClass.GROWTH_SPEED)

            pygame.display.flip()

        self.close()
