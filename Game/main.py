from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
DEFAULT_SPEED = 100

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )

def next_turn():
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food.__init__()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
    )
    snake.squares.insert(0, square)
    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn)

def change_direction(new_direction):
    global direction
    if new_direction == "up" and direction != "down":
        direction = "up"
    elif new_direction == "down" and direction != "up":
        direction = "down"
    elif new_direction == "left" and direction != "right":
        direction = "left"
    elif new_direction == "right" and direction != "left":
        direction = "right"

def check_collisions():
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        font=("consolas", 40),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )
    restart_button.place(relx=0.5, rely=0.9, anchor=CENTER)

def restart_game():
    global snake, food, score, direction
    restart_button.place_forget()
    canvas.delete(ALL)
    score = 0
    label.config(text="Score:{}".format(score))
    direction = "down"
    snake = Snake()
    food = Food()
    next_turn()

def set_difficulty(event):
    global SPEED
    difficulty = difficulty_var.get()
    if difficulty == "Easy":
        SPEED = 150
    elif difficulty == "Medium":
        SPEED = 100
    elif difficulty == "Hard":
        SPEED = 50

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

difficulty_var = StringVar(value="Medium")
difficulty_menu = OptionMenu(window, difficulty_var, "Easy", "Medium", "Hard", command=set_difficulty)
difficulty_menu.pack()

restart_button = Button(window, text="Restart Game", font=("consolas", 20), command=restart_game)
restart_button.place_forget()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

SPEED = DEFAULT_SPEED
snake = Snake()
food = Food()

window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))

next_turn()

window.mainloop()
