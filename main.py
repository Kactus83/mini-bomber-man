import tkinter as tk
import time

def draw_grid(canvas, grid, cell_size):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 1:
                color = 'grey'
            elif cell == 2:
                color = 'black'
            else:
                color = 'white'
            x, y = j * cell_size, i * cell_size
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color)

def draw_character(canvas, x, y, cell_size):
    canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='blue')

def draw_bomb(canvas, x, y, cell_size):
    canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='red')

def is_valid_move(x, y, grid, cell_size, grid_size):
    row, col = y // cell_size, x // cell_size
    if 0 <= row < grid_size and 0 <= col < grid_size:
        return grid[row][col] == 0
    return False

def place_hard_wall(x, y, grid, cell_size):
    row, col = y // cell_size, x // cell_size
    grid[row][col] = 2

def place_light_wall(x, y, grid, cell_size):
    row, col = y // cell_size, x // cell_size
    grid[row][col] = 1

def place_bomb(x, y, grid, bombs, cell_size):
    row, col = y // cell_size, x // cell_size
    bombs.append((row, col, time.time()))

is_exploding = False

def explode_bomb(row, col, grid, cell_size, radius):
    global is_exploding
    is_exploding = True
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            if abs(i) + abs(j) <= radius:
                r, c = row + i, col + j
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                    if grid[r][c] == 1:
                        grid[r][c] = 0
                        x, y = c * cell_size, r * cell_size
                        canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='red')
    canvas.update()
    time.sleep(1)
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            if abs(i) + abs(j) <= radius:
                r, c = row + i, col + j
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                    if grid[r][c] != 1:
                        x, y = c * cell_size, r * cell_size
                        canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='white')
    canvas.update()
    is_exploding = False

def on_key(event):
    global player_x, player_y, bombs, is_exploding
    if is_exploding:
        return
    new_x, new_y = player_x, player_y

    if event.keysym == 'Up':
        new_y -= cell_size
    elif event.keysym == 'Down':
        new_y += cell_size
    elif event.keysym == 'Left':
        new_x -= cell_size
    elif event.keysym == 'Right':
        new_x += cell_size
    elif event.keysym == 'space':
        place_bomb(player_x, player_y, grid, bombs, cell_size)

    if is_valid_move(new_x, new_y, grid, cell_size, grid_size):
        player_x, player_y = new_x, new_y

    canvas.delete('all')
    draw_grid(canvas, grid, cell_size)
    for bomb in bombs:
        row, col, time_placed = bomb
        if time.time() - time_placed > 2:
            explode_bomb(row, col, grid, cell_size, 2)
            bombs.remove(bomb)
            draw_grid(canvas, grid, cell_size)
        else:
            draw_bomb(canvas, col * cell_size, row * cell_size, cell_size)
    draw_character(canvas, player_x, player_y, cell_size)

root = tk.Tk()
root.title('Mini Bomberman')

# Constants and grid initialization
grid_size = 20
cell_size = 50
player_x, player_y = 0, 0
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
bombs = []

# Initialize canvas
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Place some hard walls
hard_walls = [
    (50, 150),
    (50, 450),
    (100, 100),
    (100, 400),
    (150, 250),
    (150, 300),
    (200, 100),
    (200, 200),
    (200, 450),
    (250, 350),
    (300, 100),
    (350, 250),
    (400, 200),
    (400, 300),
    (450, 150),
    (450, 400),
    (500, 150),
    (500, 450),
    (600, 100),
    (600, 400),
    (650, 250),
    (650, 300),
    (700, 100),
    (700, 200),
    (700, 450),
    (750, 350),
    (800, 100),
    (850, 250),
    (900, 200),
    (900, 300),
    (950, 150),
    (950, 400)
]

hard_walls = sorted(hard_walls, key=lambda w: (w[0], w[1]))

for hard_wall in hard_walls:
    place_hard_wall(hard_wall[0], hard_wall[1], grid, cell_size)

# Place some light walls
light_walls = [
    (50, 200),
    (50, 800),
    (100, 150),
    (100, 200),
    (150, 200),
    (150, 350),
    (200, 50),
    (200, 100),
    (250, 450),
    (300, 350),
    (350, 100),
    (350, 600),
    (400, 300),
    (400, 300),
    (450, 150),
    (450, 400),
    (550, 200),
    (550, 800),
    (600, 150),
    (600, 200),
    (650, 200),
    (650, 350),
    (700, 50),
    (700, 100),
    (750, 450),
    (800, 350),
    (850, 100),
    (850, 600),
    (900, 300),
    (900, 300),
    (950, 150),
    (950, 400)
]

light_walls = sorted(light_walls, key=lambda w: (w[0], w[1]))

for light_wall in light_walls:
    place_light_wall(light_wall[0], light_wall[1], grid, cell_size)

# Draw grid and character
draw_grid(canvas, grid, cell_size)
draw_character(canvas, player_x, player_y, cell_size)

# Key binding
canvas.bind('<Key>', on_key)
canvas.focus_set()

# Run the Tkinter event loop
root.mainloop()
