"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame

class Grid:

    def __init__(self):
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Define grid sizes
        self.GRID_SIZE_X = 20
        self.GRID_SIZE_Y = 20

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = 5
        self.HEIGHT = 5

        # This sets the margin between each cell
        self.MARGIN = 1

    def init_grid(self):
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
        self.grid[1][5] = 1
        self.grid[19][19] = 1


class PyGameWindow:

    def __init__(self, Grid):
        # Initialize pygame
        pygame.init()
        # Set the HEIGHT and WIDTH of the screen
        # WINDOW_SIZE = [600, 600]
        self.WINDOW_SIZE = [Grid.GRID_SIZE_Y * (Grid.HEIGHT + Grid.MARGIN) + Grid.MARGIN, Grid.GRID_SIZE_X * (Grid.WIDTH + Grid.MARGIN) + Grid.MARGIN]
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        # Set title of screen
        pygame.display.set_caption("Array Backed Grid")

        # Loop until the user clicks the close button.
        self.done = False

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.main_loop(Grid)

    def main_loop(self,Grid):
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
                    Grid.grid[row][column] = 1
                    print("Click ", pos, "Grid coordinates: ", row, column)

            # Set the screen background
            self.screen.fill(Grid.BLACK)

            # Draw the grid
            for row in range(Grid.GRID_SIZE_X):
                for column in range(Grid.GRID_SIZE_Y):
                    color = Grid.WHITE
                    if Grid.grid[row][column] == 1:
                        color = Grid.GREEN
                    pygame.draw.rect(self.screen,
                                     color,
                                     [(Grid.MARGIN + Grid.WIDTH) * column + Grid.MARGIN,
                                      (Grid.MARGIN + Grid.HEIGHT) * row + Grid.MARGIN,
                                      Grid.WIDTH,
                                      Grid.HEIGHT])

            # Limit to 60 frames per second
            self.clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()


