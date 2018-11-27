"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import random

import pygame

from src.color import RandomColorDictionary


class Grid:

    def __init__(self):

        self.neighbourhood_type = 'Moore'
        self.grain_growth = False

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = 7
        self.HEIGHT = 7

        # This sets the margin between each cell
        self.MARGIN = 1

    def init_grid(self, X, Y):
        # Define grid sizes
        self.GRID_SIZE_X = X
        self.GRID_SIZE_Y = Y

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
        #self.grid[19][19] = 1

    def clean_grid(self):
        for row in range(self.GRID_SIZE_X):
            for column in range(self.GRID_SIZE_Y):
                self.grid[row][column] = 0

    def change_neighbour(self, neighbour):
        self.neighbourhood_type = neighbour

    def set_grain_growth(self, grain_growth_bool):
        self.grain_growth = grain_growth_bool


class PyGameWindow:

    def __init__(self, Grid):
        # Initialize pygame
        pygame.init()
        # Set the HEIGHT and WIDTH of the screen
        # WINDOW_SIZE = [600, 600]
        self.WINDOW_SIZE = [Grid.GRID_SIZE_Y * (Grid.HEIGHT + Grid.MARGIN) + Grid.MARGIN,
                            Grid.GRID_SIZE_X * (Grid.WIDTH + Grid.MARGIN) + Grid.MARGIN]
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        # Set title of screen
        pygame.display.set_caption("Grain Growth")

        # Loop until the user clicks the close button.
        self.done = False
        self.color_class = RandomColorDictionary()

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.main_loop(Grid)

    def moore_growth(self, Grid, row, column):
        grain_to_grow = []
        color_to_grow = Grid.grid[row][column]
        grain_to_grow.append(color_to_grow)

        if column + 1 < Grid.GRID_SIZE_Y:
            grain_to_grow.append(row)
            grain_to_grow.append(column + 1)

        if row - 1 >= 0 and column + 1 < Grid.GRID_SIZE_Y:
            grain_to_grow.append(row - 1)
            grain_to_grow.append(column + 1)

        if row - 1 >= 0:
            grain_to_grow.append(row - 1)
            grain_to_grow.append(column)

        if row - 1 >= 0 and column - 1 >= 0:
            grain_to_grow.append(row - 1)
            grain_to_grow.append(column - 1)

        if column - 1 >= 0:
            grain_to_grow.append(row)
            grain_to_grow.append(column - 1)

        if row + 1 < Grid.GRID_SIZE_X and column - 1 >= 0:
            grain_to_grow.append(row + 1)
            grain_to_grow.append(column - 1)

        if row + 1 < Grid.GRID_SIZE_X:
            grain_to_grow.append(row + 1)
            grain_to_grow.append(column)

        if row + 1 < Grid.GRID_SIZE_X and column + 1 < Grid.GRID_SIZE_X:
            grain_to_grow.append(row + 1)
            grain_to_grow.append(column + 1)


        return grain_to_grow


    def main_loop(self, Grid):
        # -------- Main Program Loop -----------
        while not self.done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (Grid.WIDTH + Grid.MARGIN)
                    row = pos[1] // (Grid.HEIGHT + Grid.MARGIN)
                    # Set that location to one
                    Grid.grid[row][column] = random.choice(list(self.color_class.colors))
                    # TEST Methods of click in here
                    print("Click ", pos, "Grid coordinates: ", row, column)

            # Set the screen background
            self.screen.fill(self.color_class.colors['black'])

            # Draw the grid
            grains_to_grow = []
            for row in range(Grid.GRID_SIZE_X):
                for column in range(Grid.GRID_SIZE_Y):
                    color = self.color_class.colors['white']
                    if Grid.grid[row][column] != 0:
                        if Grid.grain_growth == True:
                            # MOORE test
                            if Grid.neighbourhood_type == 'Moore':
                                grain_to_grow = self.moore_growth(Grid, row, column)
                                grains_to_grow.append(grain_to_grow)
                                grain_to_grow = []

                        color = self.color_class.colors[Grid.grid[row][column]]
                    pygame.draw.rect(self.screen,
                                     color,
                                     [(Grid.MARGIN + Grid.WIDTH) * column + Grid.MARGIN,
                                      (Grid.MARGIN + Grid.HEIGHT) * row + Grid.MARGIN,
                                      Grid.WIDTH,
                                      Grid.HEIGHT])

            if Grid.grain_growth == True:
                for i in range(0, len(grains_to_grow)):
                    for j in range(1, len(grains_to_grow[i]), 2):
                        row = grains_to_grow[i][j]
                        column = grains_to_grow[i][j+1]
                        Grid.grid[row][column] = grains_to_grow[i][0]
            grains_to_grow = []

            # Limit to 60 frames per second
            self.clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()
        exit()
