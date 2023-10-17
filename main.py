import tkinter as tk

def draw_grid(canvas, grid_size, cell_size):
    for i in range(0, grid_size * cell_size, cell_size):
        for j in range(0, grid_size * cell_size, cell_size):
            canvas.create_rectangle(i, j, i + cell_size, j + cell_size, fill='white')

def draw_character(canvas, x, y, cell_size):
    canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill='blue')

def on_key(event):
    global player_x, player_y
    if event.keysym == 'Up':
        player_y -= cell_size
    elif event.keysym == 'Down':
        player_y += cell_size
    elif event.keysym == 'Left':
        player_x -= cell_size
    elif event.keysym == 'Right':
        player_x += cell_size

    canvas.delete('all')
    draw_grid(canvas, grid_size, cell_size)
    draw_character(canvas, player_x, player_y, cell_size)

root = tk.Tk()
root.title('Mini Bomberman')

# Constants
grid_size = 10
cell_size = 50
player_x, player_y = 0, 0

# Initialize canvas
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Draw grid and character
draw_grid(canvas, grid_size, cell_size)
draw_character(canvas, player_x, player_y, cell_size)

# Key binding
canvas.bind('<Key>', on_key)
canvas.focus_set()

# Run the Tkinter event loop
root.mainloop()
