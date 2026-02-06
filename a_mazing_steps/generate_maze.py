#!/usr/bin/env python3
import curses
import random
import time

class Cell:
    """
    Characteristic of a cell position and wall situation
    """
    WALL = "█"
    EMPTY = " "
    ENTRANCE = "*"
    OUT = "E"
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True]

    def draw(self, stdscr):
        """Draws the cell at its position."""
        sy = self.y * 2
        sx = self.x * 4

        # Top wall - draw corners separately
        if self.walls[0]:  # North
            stdscr.addstr(sy, sx, self.WALL * 4)
        else:
            stdscr.addstr(sy, sx, self.WALL)
            stdscr.addstr(sy, sx + 1, self.EMPTY * 2, curses.color_pair(1))
            stdscr.addstr(sy, sx + 3, self.WALL)

        # Right wall
        if self.walls[1]:  # East
            stdscr.addstr(sy + 1, sx + 3, self.WALL)
        else:
            stdscr.addstr(sy + 1, sx + 3, self.EMPTY, curses.color_pair(1))

        # Bottom wall - draw corners separately
        if self.walls[2]:  # South
            stdscr.addstr(sy + 2, sx, self.WALL * 4)
        else:
            stdscr.addstr(sy + 2, sx, self.WALL)
            stdscr.addstr(sy + 2, sx + 1, self.EMPTY * 2, curses.color_pair(1))
            stdscr.addstr(sy + 2, sx + 3, self.WALL)

        # Left wall
        if self.walls[3]:  # West
            stdscr.addstr(sy + 1, sx, self.WALL)
        else:
            stdscr.addstr(sy + 1, sx, self.EMPTY, curses.color_pair(1))

        # Interior space
        if self.visited:
            stdscr.addstr(sy + 1, sx + 1, self.EMPTY * 2, curses.color_pair(1))
        else:
            stdscr.addstr(sy + 1, sx + 1, self.EMPTY * 2)

    def get_neighbors(self, grid, rows, cols):
        neighbors = []

        # Check top neighbor (North)
        if self.y - 1 >= 0:
            top = grid[self.y - 1][self.x]
            if not top.visited:
                neighbors.append(top)

        # Check right neighbor (East)
        if self.x + 1 < cols:
            rig = grid[self.y][self.x + 1]
            if not rig.visited:
                neighbors.append(rig)

        # Check bottom neighbor (South)
        if self.y + 1 < rows:
            bot = grid[self.y + 1][self.x]
            if not bot.visited:
                neighbors.append(bot)

        # Check left neighbor (West)
        if self.x - 1 >= 0:
            lef = grid[self.y][self.x - 1]
            if not lef.visited:
                neighbors.append(lef)

        return neighbors


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


def remove_walls(cell_a, cell_b):
    """Remove walls between two adjacent cells"""
    # Horizontal difference
    diff_x = cell_a.x - cell_b.x
    if diff_x == 1:  # cell_b is to the left
        cell_a.walls[3] = False
        cell_b.walls[1] = False
    elif diff_x == -1:  # cell_b is to the right
        cell_a.walls[1] = False
        cell_b.walls[3] = False

    # Vertical difference
    diff_y = cell_a.y - cell_b.y
    if diff_y == 1:  # cell_b is above
        cell_a.walls[0] = False
        cell_b.walls[2] = False
    elif diff_y == -1:  # cell_b is below
        cell_a.walls[2] = False
        cell_b.walls[0] = False


def generate_maze(stdscr, grid, width, height):
    """Generate maze using recursive backtracking"""
    # Start from top-left
    current = random.choice(grid)
    current = random.choice(current)
    current.visited = True

    draw_grid(stdscr, grid, width, height)
    time.sleep(1)

    # Stack for backtracking
    stack = [current]

    # Continue while there are cells in the stack
    while stack:
        neighbors = current.get_neighbors(grid, height, width)

        if neighbors:
            # Choose random unvisited neighbor
            next_cell = random.choice(neighbors)

            # Mark as visited
            next_cell.visited = True

            # Remove walls between current and next
            remove_walls(current, next_cell)

            # Push current to stack
            stack.append(current)

            # Move to next cell
            current = next_cell

            # Draw and animate
            draw_grid(stdscr, grid, width, height)
            time.sleep(1)
        else:
            # No unvisited neighbors - backtrack by popping from stack
            current = stack.pop()


def main(stdscr):
    """Main function to set up curses and display the grid."""
    curses.curs_set(0)  # Hide cursor

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    # Define grid dimensions
    width, height = 20, 15

    # Create the grid
    grid = create_grid(width, height)

    # Generate the maze
    generate_maze(stdscr, grid, width, height)

    # Final display
    draw_grid(stdscr, grid, width, height)
    stdscr.addstr(height * 2 + 3, 0, "Press any key to exit")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
