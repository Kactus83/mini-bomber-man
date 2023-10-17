import random
import tkinter as tk
import time

# Define the Grid class to handle the game grid
class Grid:
    def __init__(self, canvas, size, cell_size):
        """Initialize the Grid class."""
        self.canvas = canvas
        self.size = size
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def draw(self, bombs):
        """Draw the grid and bombs on the canvas."""
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = 'white'
                if cell == 1:
                    color = 'grey'
                elif cell == 2:
                    color = 'black'
                x, y = j * self.cell_size, i * self.cell_size
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill=color)

        for bomb in bombs:
            bomb.draw(self.canvas, self.cell_size)

# Define the Player class to handle the player character
class Player:
    def __init__(self, x, y, cell_size):
        """Initialize the Player class."""
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def draw(self, canvas):
        """Draw the player on the canvas."""
        canvas.create_rectangle(self.x, self.y, self.x + self.cell_size, self.y + self.cell_size, fill='blue')

# Define the Bomb class to handle the bombs
class Bomb:
    def __init__(self, row, col, time_placed):
        """Initialize the Bomb class."""
        self.row = row
        self.col = col
        self.time_placed = time_placed

    def draw(self, canvas, cell_size):
        """Draw the bomb on the canvas."""
        x, y = self.col * cell_size, self.row * cell_size
        canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='red')

# Define the MiniBomberman class to handle the game logic
class MiniBomberman:
    def __init__(self):
        """Initialize the game variables."""
        self.grid_size = 20
        self.cell_size = 50
        self.player_x, self.player_y = 0, 0
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.bombs = []
        self.max_bombs = 3
        self.root = tk.Tk()
        self.root.title('Mini Bomberman')
        self.canvas = tk.Canvas(self.root, width=(self.grid_size + 150) * self.cell_size, height=self.grid_size * self.cell_size)
        self.canvas.pack()
        self.canvas.bind('<Key>', self.on_key)
        self.canvas.focus_set()

    def draw_grid(self):
        """Draw the game grid on the canvas."""
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = 'grey' if cell == 1 else 'black' if cell == 2 else 'white'
                x, y = j * self.cell_size, i * self.cell_size
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill=color)
        self.canvas.create_rectangle(self.grid_size * self.cell_size, 0, (self.grid_size + 150) * self.cell_size, self.grid_size * self.cell_size, fill='lightgrey')
        self.canvas.create_text((self.grid_size + 1.5) * self.cell_size, self.cell_size, text=f'Bombs: {self.max_bombs}', font=('Arial', 14))

    def initialize_walls(self, n_light_walls=50, n_hard_walls=50):
        """Initialize walls on the grid."""
        available_positions = [(row, col) for row in range(self.grid_size) for col in range(self.grid_size)]
        available_positions.remove((self.player_y // self.cell_size, self.player_x // self.cell_size)) 
        random.shuffle(available_positions)

        for row, col in available_positions[:n_light_walls]:
            self.grid[row][col] = 1  # Light wall

        for row, col in available_positions[n_light_walls:n_light_walls + n_hard_walls]:
            self.grid[row][col] = 2  # Hard wall

    def draw_character(self):
        """Draw the player character on the canvas."""
        self.canvas.create_rectangle(self.player_x, self.player_y, self.player_x + self.cell_size, self.player_y + self.cell_size, fill='blue')

    def draw_bomb(self, x: int, y: int):
        """Draw a bomb on the canvas at the specified location."""
        self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill='red')

    def is_valid_move(self, x: int, y: int) -> bool:
        """Check if the player can move to the specified location."""
        row, col = y // self.cell_size, x // self.cell_size
        return 0 <= row < self.grid_size and 0 <= col < self.grid_size and self.grid[row][col] == 0

    def place_wall(self, x: int, y: int, wall_type: int):
        """Place a wall on the grid at the specified location."""
        row, col = y // self.cell_size, x // self.cell_size
        self.grid[row][col] = wall_type

    def place_bomb(self):
        """Place a bomb on the player's current location."""
        if len(self.bombs) < self.max_bombs:
            row, col = self.player_y // self.cell_size, self.player_x // self.cell_size
            self.bombs.append((row, col, time.time()))
            self.max_bombs -= 1

    def explode_bomb(self, row: int, col: int, radius: int):
        """Explode a bomb at the specified location."""
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if abs(i) + abs(j) <= radius:
                    r, c = row + i, col + j
                    if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]) and self.grid[r][c] == 1:
                        self.grid[r][c] = 0

    def on_key(self, event):
        """Handle key events for moving the player and placing bombs."""
        new_x, new_y = self.player_x, self.player_y
        if event.keysym == 'Up':
            new_y -= self.cell_size
        elif event.keysym == 'Down':
            new_y += self.cell_size
        elif event.keysym == 'Left':
            new_x -= self.cell_size
        elif event.keysym == 'Right':
            new_x += self.cell_size
        elif event.keysym == 'space':
            self.place_bomb()

        if self.is_valid_move(new_x, new_y):
            self.player_x, self.player_y = new_x, new_y

        self.canvas.delete('all')
        self.draw_grid()
        for bomb in self.bombs:
            row, col, time_placed = bomb
            if time.time() - time_placed > 2:
                self.explode_bomb(row, col, 2)
                self.bombs.remove(bomb)
                self.draw_grid()
            else:
                self.draw_bomb(col * self.cell_size, row * self.cell_size)
        self.draw_character()
        
    def start(self):
        """Start the game loop."""
        self.initialize_walls()
        while True:
            self.canvas.delete('all')
            self.draw_grid()
            self.draw_character()
            for row, col, _ in self.bombs:
                self.draw_bomb(col * self.cell_size, row * self.cell_size)
            self.canvas.update()
            time.sleep(0.05)

if __name__ == '__main__':
    game = MiniBomberman()
    game.start()