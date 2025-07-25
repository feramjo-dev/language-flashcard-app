from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")
FLIP_TIME = 5000 # 5 seconds




# ---------------------------- DATA SETUP ------------------------------- #
try:
    data = pandas.read_csv("./data/french_words.csv")
except FileNotFoundError:
    print("CSV file not found")
    exit()

# Create a list from the data.csv
to_learn_words = data.to_dict(orient="records")
known_words_indices = set()
current_card = {}
card_index = 0
countdown_time = 5
flip_timer = None
countdown_timer = None


# ---------------------------- FUNCTIONS ------------------------------- #
def next_card():
    global card_index, current_card, countdown_time, countdown_timer, flip_timer

    # Cancel previous timers if any
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    if countdown_timer is not None:
        window.after_cancel(countdown_timer)

    while True:
        card_index = random.randint(0, len(to_learn_words) - 1)
        if card_index not in known_words_indices:
            break

    current_card = to_learn_words[card_index]

    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(timer_text, text=f"00:0{countdown_time}")

    # Reset and start countdown
    countdown_time = 5
    countdown()
    flip_timer = window.after(FLIP_TIME, flip_card)

def flip_card():
    global countdown_timer
    if countdown_timer is not None:
        window.after_cancel(countdown_timer)
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(timer_text, text="")

def  known_words():
    known_words_indices.add(card_index)
    next_card()

def unknown_words():
    next_card()

def countdown():
    global countdown_time, countdown_timer
    if countdown_time > 0:
        canvas.itemconfig(timer_text, text=f"00:0{countdown_time}" if countdown_time < 10 else f"00:{countdown_time}")
        countdown_time -= 1
        countdown_timer = window.after(1000, countdown)
    else:
        canvas.itemconfig(timer_text, text="")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Language Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Setup canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)

card_title = canvas.create_text(400, 150, text="", font=FONT_TITLE)
card_word = canvas.create_text(400, 263, text="", font=FONT_WORD)
timer_text = canvas.create_text(600, 50, text="", fill=BACKGROUND_COLOR, font=("Courier", 35, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=known_words)
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=unknown_words)
wrong_button.grid(row=1, column=0)

next_card()
window.mainloop()
