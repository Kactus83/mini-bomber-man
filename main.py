import tkinter as tk

def draw_grid(canvas, grid, cell_size):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            color = 'black' if cell == 1 else 'white'
            x, y = j * cell_size, i * cell_size
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color)

def draw_character(canvas, x, y, cell_size):
    canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='blue')

def is_valid_move(x, y, grid, cell_size, grid_size):
    row, col = y // cell_size, x // cell_size
    if 0 <= row < grid_size and 0 <= col < grid_size:
        return grid[row][col] == 0
    return False

def place_wall(x, y, grid, cell_size):
    row, col = y // cell_size, x // cell_size
    grid[row][col] = 1

def on_key(event):
    global player_x, player_y
    new_x, new_y = player_x, player_y

    if event.keysym == 'Up':
        new_y -= cell_size
    elif event.keysym == 'Down':
        new_y += cell_size
    elif event.keysym == 'Left':
        new_x -= cell_size
    elif event.keysym == 'Right':
        new_x += cell_size

    if is_valid_move(new_x, new_y, grid, cell_size, grid_size):
        player_x, player_y = new_x, new_y

    canvas.delete('all')
    draw_grid(canvas, grid, cell_size)
    draw_character(canvas, player_x, player_y, cell_size)

root = tk.Tk()
root.title('Mini Bomberman')

# Constants and grid initialization
grid_size = 10
cell_size = 50
player_x, player_y = 0, 0
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Initialize canvas
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Place some walls
place_wall(100, 100, grid, cell_size)
place_wall(150, 250, grid, cell_size)
place_wall(200, 200, grid, cell_size)
place_wall(50, 150, grid, cell_size)

# Draw grid and character
draw_grid(canvas, grid, cell_size)
draw_character(canvas, player_x, player_y, cell_size)

# Key binding
canvas.bind('<Key>', on_key)
canvas.focus_set()

# Run the Tkinter event loop
root.mainloop()
