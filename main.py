from tkinter import *
from tkinter import messagebox
import pandas
import pandas as pd
import random
import csv
import os

background_color = "AntiqueWhite2"
# --------------------Creating words_to_learn.csv---------------------------------
with open("data/french_words.csv", "r", encoding= "utf-8") as input_file:
    output_file = "data/words_to_learn.csv"

    if not os.path.exists(output_file):
        with open(output_file, "w",newline="", encoding= "utf-8") as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)
            # pass : next(reader) # skip headers of reader.csv
            writer.writerows(reader)  # iterate through and write rows of reader into writer
            print("User csv created.")
    else:
        pass
# ------------------------------------------------------
with open("data/words_to_learn.csv", "r", encoding= "utf-8") as flashcard_csv:
    flashcard_df = pd.read_csv(flashcard_csv)
    # this following code becomes so complicated solely due to a different approach to turning df into dict
    d = {}
    records = flashcard_df.to_dict(orient = "records") # random.choice can gain access to a list but not a dict


def next_card():    # next card function
    global flip_timer, d
    window.after_cancel(flip_timer) # stop the timer
    canvas.itemconfig(canvas_image, image= card_front_img)  # switch to front image
    canvas.itemconfig(canvas_title, text="French", fill = "Black")  # title switch to french
    # select a pair and store it in the dict
    d.update(random.choice(records))
    # you have to type text = ...
    canvas.itemconfig(canvas_word, text= d["French"], fill = "Black",  font=("Arial Unicode MS", 40, "italic"))  # switching current card
    flip_timer = window.after(3000, flipping)

def flipping():
    canvas.itemconfig(canvas_image, image = card_back_img)
    canvas.itemconfig(canvas_title, text = "English", fill = "White") # switch the title
     # importing the two returned variables from next_card()
    canvas.itemconfig(canvas_word, text = d["English"], fill = "White") # switch to english word

#------------------------------------------------------
def removing():
    with open("data/words_to_learn.csv", "r+") as flashcard_csv:
        df = pandas.read_csv(flashcard_csv)
        french_word_to_remove = d["French"]

        mask = df["French"] != french_word_to_remove
        df_filtered = df[mask]

        df_filtered.to_csv("data/words_to_learn.csv", index = False)

        print(f"'{french_word_to_remove}' removed from words_to_learn.csv (if it existed).")

def confirm_removal():
    # message box
    response = messagebox.askquestion("Confirm removal", f'Do you wish to remove {d["French"]}')
    if response.lower() == "yes":
        removing()


def known_button_clicked():
    confirm_removal()
    next_card()


#------------------------------------------------------
# window
window = Tk()
window.title("Flash Cards")
window.config(padx= 30, pady= 30, bg = background_color)
# canvas
canvas = Canvas(width = 800, height = 526)
canvas.config(bg = background_color, highlightthickness= 0)
canvas.grid(row = 0, column = 0, columnspan = 2)
# canvas images
card_front_img = PhotoImage(file= "images/card_front.png")
canvas_image = canvas.create_image(400,263, image = card_front_img)
card_back_img = PhotoImage(file= "images/card_back.png")
# canvas_word
canvas_title = canvas.create_text(400, 150, text = "French", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text = "", font=("Ariel", 40, "italic"))

cross_image = PhotoImage(file = "images/wrong.png")
# cross button
unknown_button = Button(image = cross_image, command=next_card)
unknown_button.config(bg = background_color,highlightthickness = 0)
unknown_button.grid(row = 1, column = 0)
# right button
check_image = PhotoImage(file= "images/right.png")

known_button = Button(image = check_image, command= known_button_clicked)
known_button.config(bg = background_color,highlightthickness= 0)
known_button.grid(row = 1, column = 1)

#----------------------------------------
# watch out the sequence of these two lines
flip_timer = window.after(3000, flipping)
next_card() # display the first French word once the code is run


window.mainloop()

