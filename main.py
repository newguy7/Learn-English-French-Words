from tkinter import *
import pandas
import random


current_card = {}
to_learn = {}

# --------------------------- GENERATE DATA --------------------------- #
try:
    data_file = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_word.csv")
    to_learn = original_data.to_dict(orient='records')
else:    
    to_learn = data_file.to_dict(orient="records")


def generate_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French",fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image,image=front_img_file)
    flip_timer = window.after(3000,func=flip_card)

# ------------------- FLIP CARD TO SHOW WORD IN ENGLISH OR FRENCH ---------------- #
def flip_card():
    canvas.itemconfig(card_title, text="English",fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image,image=back_img_file)

# -------------------- REMOVE THE KNOWN WORD FROM WORDS TO LEARN ----------------- #
def known_words():
    
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)
    generate_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg="#9bdeac")

# change the card every 3 seconds
flip_timer = window.after(3000,func=flip_card)

canvas = Canvas(width=800, height=526, bg="#9bdeac",highlightthickness=0)


# add image to canvas
front_img_file = PhotoImage(file="images/card_front.png")
back_img_file = PhotoImage(file="images/card_back.png")
right_img_file = PhotoImage(file="images/right.png")
wrong_img_file = PhotoImage(file="images/wrong.png")

canvas_image = canvas.create_image(400,263,image=front_img_file)
canvas.grid(row=0, column=0, columnspan=2)

card_title = canvas.create_text(400,150,text="",font=("Ariel",40,"italic"))
canvas.grid(row=0, column=0, columnspan=2)

card_word = canvas.create_text(400,253,text="",font=("Ariel",60,"bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_button = Button(image=right_img_file,highlightthickness=0,command=known_words)
right_button.grid(row=1, column=1)

wrong_button = Button(image=wrong_img_file,highlightthickness=0,command=generate_word)
wrong_button.grid(row=1, column=0)

# initialize the first word
generate_word()

window.mainloop()