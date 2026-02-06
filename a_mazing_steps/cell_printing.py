#!/usr/bin/env python3
import curses


class Cell:
    """
    Characteristic of a cell position and wall sitiation
    """
    WALL = "█"
    EMPTY = " "
    ENTRANCE = "*"
    OUT = "E"

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]

    def draw(self, stdscr):
        """Draws the cell at its position."""
        # Screen position (account for double-spacing for better proportions)
        sy = self.y * 2
        sx = self.x * 4

        # Top wall
        if self.walls[0]:  # North
            stdscr.addstr(sy, sx, self.WALL * 4)

        # Left wall
        if self.walls[3]:  # West
            stdscr.addstr(sy + 1, sx, self.WALL)

        # Interior space
        stdscr.addstr(sy + 1, sx + 1, self.EMPTY * 2)

        # Right wall (only on last column to avoid overwrite)
        if self.walls[1]:  # East
            stdscr.addstr(sy + 1, sx + 3, self.WALL)

        # Bottom wall (only on last row to avoid overwrite)
        if self.walls[2]:  # South
            stdscr.addstr(sy + 2, sx, self.WALL * 4)


def create_grid(width: int, height: int):
    """Creates a grid of cells with given width and height."""
    return [[Cell(x, y) for x in range(width)] for y in range(height)]


def draw_grid(stdscr, grid, width: int, height: int):
    """Draws the entire grid by calling each cell's draw method."""
    stdscr.clear()

    for row in grid:
        for cell in row:
            cell.draw(stdscr)

    stdscr.refresh()


def main(stdscr):
    """Main function to set up curses and display the grid."""
    curses.curs_set(0)  # Hide cursor

    # Define grid dimensions
    width, height = 10, 7

    #  Create and draw the grid
    grid = Cell(0, 0)
    grid.draw(stdscr)
    #grid = create_grid(width, height)
    #draw_grid(stdscr, grid, width, height)

    # Wait for user input before exiting
    stdscr.addstr(height * 2 + 3, 0, "Press any key to exit")
    stdscr.getch()
    print(grid[0])


if __name__ == "__main__":
    curses.wrapper(main)
