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
        
        # Top wall
        if self.walls[0]:  # North
            stdscr.addstr(sy, sx, self.WALL * 4)
        else:
            stdscr.addstr(sy, sx, self.WALL)
            stdscr.addstr(sy, sx + 1, self.EMPTY * 2)
            stdscr.addstr(sy, sx + 3, self.WALL)
        
        # Right wall
        if self.walls[1]:  # East
            stdscr.addstr(sy + 1, sx + 3, self.WALL)
        else:
            stdscr.addstr(sy + 1, sx + 3, self.EMPTY)
        
        # Bottom wall
        if self.walls[2]:  # South
            stdscr.addstr(sy + 2, sx, self.WALL * 4)
        else:
            stdscr.addstr(sy + 2, sx, self.WALL)
            stdscr.addstr(sy + 2, sx + 1, self.EMPTY * 2)
            stdscr.addstr(sy + 2, sx + 3, self.WALL)
        
        # Left wall
        if self.walls[3]:  # West
            stdscr.addstr(sy + 1, sx, self.WALL)
        else:
            stdscr.addstr(sy + 1, sx, self.EMPTY)
        
        # Interior space
        if self.visited:
            stdscr.addstr(sy + 1, sx + 1, self.EMPTY * 2)
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


class Maze:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.create_grid()
    
    def create_grid(self):
        """Creates a grid of cells with given width and height."""
        return [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
    
    def remove_walls(self, cell_a, cell_b):
        diff = cell_a.x - cell_b.x
        if diff == 1:
            cell_a.walls[3] = False
            cell_b.walls[1] = False
        elif diff == -1:
            cell_b.walls[3] = False
            cell_a.walls[1] = False
        
        diff = cell_a.y - cell_b.y
        if diff == 1:
            cell_a.walls[0] = False
            cell_b.walls[2] = False
        elif diff == -1:
            cell_b.walls[0] = False
            cell_a.walls[2] = False
    
    def generate(self, stdscr, animate=True):
        """Generate maze using recursive backtracking"""
        current = self.grid[0][0]
        current.visited = True
        
        stack = [current]
        
        if animate:
            self.draw_grid(stdscr)
            time.sleep(0.3)
        
        while stack:
            neighbors = current.get_neighbors(self.grid, self.height, self.width)
            
            if neighbors:
                nextt = random.choice(neighbors)
                nextt.visited = True
                self.remove_walls(current, nextt)
                
                stack.append(current)
                current = nextt
                
                if animate:
                    self.draw_grid(stdscr)
                    time.sleep(0.05)
            else:
                current = stack.pop()
    
    def draw_grid(self, stdscr):
        """Draws the entire grid by calling each cell's draw method."""
        stdscr.clear()
        for row in self.grid:
            for cell in row:
                cell.draw(stdscr)
        stdscr.refresh()


def main(stdscr):
    """Main function to set up curses and display the grid."""
    curses.curs_set(0)  # Hide cursor
    
    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    
    # Define grid dimensions
    width, height = 20, 15
    
    # Create maze
    maze = Maze(width, height)
    
    # Show initial grid
    maze.draw_grid(stdscr)
    stdscr.addstr(height * 2 + 3, 0, "Press any key to generate maze...")
    stdscr.getch()
    
    # Generate maze with animation
    maze.generate(stdscr, animate=True)
    
    # Show completed maze
    maze.draw_grid(stdscr)
    stdscr.addstr(height * 2 + 3, 0, "Press any key to exit")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
