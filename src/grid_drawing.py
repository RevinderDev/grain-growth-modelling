"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import random
from copy import deepcopy

import pygame

from src.color import RandomColorDictionary


class GridClass:

    def __init__(self):

        self.neighbourhood_type = 'Moore'
        self.grain_growth = False

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = 7
        self.HEIGHT = 7

        self.GROWTH_SPEED = 60

        # This sets the margin between each cell
        self.MARGIN = 1

    def init_grid(self, x, y):
        # Define grid sizes
        self.GRID_SIZE_X = x
        self.GRID_SIZE_Y = y

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        self.grid = []
        for row in range(self.GRID_SIZE_X):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(self.GRID_SIZE_Y):
                self.grid[row].append(0)  # Append a cell

        # Set row 1, cell 5 to one. (Remember rows and
        # column numbers start at zero.)
        # self.grid[1][5] = 1
        # self.grid[19][19] = 1

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
        for i in range(value):
            random_row = random.randint(0, self.GRID_SIZE_X-1)
            random_column = random.randint(0, self.GRID_SIZE_Y-1)
            random_color = random.choice(list(color_dict.colors.keys()))
            self.grid[random_row][random_column] = random_color


class PyGameWindow:

    def __init__(self, grid):
        # Initialize pygame
        pygame.init()
        # Set the HEIGHT and WIDTH of the screen
        # WINDOW_SIZE = [600, 600]
        self.WINDOW_SIZE = [grid.GRID_SIZE_Y * (grid.HEIGHT + grid.MARGIN) + grid.MARGIN,
                            grid.GRID_SIZE_X * (grid.WIDTH + grid.MARGIN) + grid.MARGIN]
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        # Set title of screen
        pygame.display.set_caption("Grain Growth")

        # Loop until the user clicks the close button.
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

    def moore_growth(self, old_grid, row, column):
        neighbours = []

        if column + 1 < self.gridClass.GRID_SIZE_Y:
            neighbours.append(old_grid[row][column + 1])

        if row - 1 >= 0 and column + 1 < self.gridClass.GRID_SIZE_Y:
            neighbours.append(old_grid[row - 1][column + 1])

        if row - 1 >= 0:
            neighbours.append(old_grid[row - 1][column])

        if row - 1 >= 0 and column - 1 >= 0:
            neighbours.append(old_grid[row - 1][column - 1])

        if column - 1 >= 0:
            neighbours.append(old_grid[row][column - 1])

        if row + 1 < self.gridClass.GRID_SIZE_X and column - 1 >= 0:
            neighbours.append(old_grid[row + 1][column - 1])

        if row + 1 < self.gridClass.GRID_SIZE_X:
            neighbours.append(old_grid[row + 1][column])

        if row + 1 < self.gridClass.GRID_SIZE_X and column + 1 < self.gridClass.GRID_SIZE_X:
            neighbours.append(old_grid[row + 1][column + 1])

        color_to_paint = self.determine_color(neighbours)
        self.gridClass.grid[row][column] = color_to_paint

    def von_neumann_growth(self, old_grid, row, column):
        neighbours = []

        if column + 1 < self.gridClass.GRID_SIZE_Y:
            neighbours.append(old_grid[row][column + 1])

        if row - 1 >= 0:
            neighbours.append(old_grid[row - 1][column])

        if column - 1 >= 0:
            neighbours.append(old_grid[row][column - 1])

        if row + 1 < self.gridClass.GRID_SIZE_X:
            neighbours.append(old_grid[row + 1][column])

        color_to_paint = self.determine_color(neighbours)
        self.gridClass.grid[row][column] = color_to_paint

    def hexagonal_left_growth(self, old_grid, row, column):
        # TODO 1:
        neighbours = []
        # color_to_paint = self.determine_color(neighbours)
        # self.gridClass.grid[row][column] = color_to_paint

    def hexagonal_right_growth(self, old_grid, row, column):
        # TODO 2:
        neighbours = []
        # color_to_paint = self.determine_color(neighbours)
        # self.gridClass.grid[row][column] = color_to_paint

    def hexagonal_random_growth(self, old_grid, row, column):
        # TODO 3:
        neighbours = []
        # color_to_paint = self.determine_color(neighbours)
        # self.gridClass.grid[row][column] = color_to_paint

    def pentagonal_random_growth(self, old_grid, row, column):
        # TODO 4:
        neighbours = []
        # color_to_paint = self.determine_color(neighbours)
        # self.gridClass.grid[row][column] = color_to_paint

    def main_loop(self):
        # -------- Main Program Loop -----------
        while not self.done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (self.gridClass.WIDTH + self.gridClass.MARGIN)
                    row = pos[1] // (self.gridClass.HEIGHT + self.gridClass.MARGIN)
                    # Set that location to random color
                    self.gridClass.grid[row][column] = random.choice(list(self.color_class.colors))
                    # TEST Methods of click in here
                    print("Click ", pos, "Grid coordinates: ", row, column)

            # Check grid for neighbours
            if self.gridClass.grain_growth:
                old_grid = deepcopy(self.gridClass.grid)
                for row in range(self.gridClass.GRID_SIZE_X):
                    for column in range(self.gridClass.GRID_SIZE_Y):
                        # MOORE test
                        if old_grid[row][column] == 0:
                            if self.gridClass.neighbourhood_type == 'Moore':
                                self.moore_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Von Neumann':
                                self.von_neumann_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Hexagonal Left':
                                self.hexagonal_left_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Hexagonal Right':
                                self.hexagonal_right_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Random Hexagonal':
                                self.hexagonal_random_growth(old_grid, row, column)
                            elif self.gridClass.neighbourhood_type == 'Random Pentagonal':
                                self.pentagonal_random_growth(old_grid, row, column)

            # Set the screen background
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
            # Limit to 60 frames per second
            self.clock.tick(self.gridClass.GROWTH_SPEED)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()
        exit()
