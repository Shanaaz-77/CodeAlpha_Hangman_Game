import tkinter as tk
import random
import string
import time

# Word categories
word_categories = {
    "Fruit": ["apple", "banana", "orange", "grape", "mango"],
    "Body Part": ["hand", "leg", "heart", "brain", "eye"],
    "Animal": ["tiger", "elephant", "zebra", "lion", "giraffe"]
}

# Game variables
guessed_letters = set()
max_attempts = 6
attempts_left = max_attempts
word = ""
category = ""
letter_buttons = []

# Create GUI
root = tk.Tk()
root.title("Hangman Game")
root.geometry("550x700")
root.configure(bg="#ffe6f0")  # Light pink background

# Canvas for hangman drawing
canvas = tk.Canvas(root, width=200, height=250, bg="#f0f8ff", highlightthickness=2, highlightbackground="#444")
canvas.pack(pady=10)

# Labels
category_label = tk.Label(root, text="", font=("Comic Sans MS", 16, "bold"), bg="#ffe6f0", fg="#333")
category_label.pack()

word_display = tk.Label(root, text="", font=("Courier New", 22, "bold"), bg="#ffe6f0", fg="#000")
word_display.pack()

message_label = tk.Label(root, text="", font=("Arial", 14, "italic"), bg="#ffe6f0", fg="green")
message_label.pack()

# Draw hanger base
def draw_hanger():
    canvas.create_line(20, 230, 180, 230, width=4, fill="#8B4513")   # Base
    canvas.create_line(50, 230, 50, 20, width=4, fill="#8B4513")     # Pole
    canvas.create_line(50, 20, 150, 20, width=4, fill="#8B4513")     # Beam
    canvas.create_line(150, 20, 150, 50, width=3, fill="#DC7C38")        # Rope

# Animated hangman drawing
def draw_hangman(stage):
    parts = {
        1: lambda: canvas.create_oval(130, 50, 170, 90, width=2, outline="black", fill="#ffe4b5"),
        2: lambda: canvas.create_line(150, 90, 150, 150, width=4, fill="blue"),
        3: lambda: canvas.create_line(150, 110, 120, 130, width=3, fill="blue"),
        4: lambda: canvas.create_line(150, 110, 180, 130, width=3, fill="blue"),
        5: lambda: canvas.create_line(150, 150, 130, 190, width=3, fill="green"),
        6: lambda: canvas.create_line(150, 150, 170, 190, width=3, fill="green")
    }
    root.after(200, parts[stage])  # small delay for animation

# Handle guesses from button clicks
def guess_letter(letter, button):
    global attempts_left

    button.config(state="disabled", bg="gray")  # Disable button after click

    if letter in guessed_letters:
        return

    guessed_letters.add(letter)

    if letter in word:
        display_word = " ".join([l if l in guessed_letters else "_" for l in word])
        word_display.config(text=display_word)

        if "_" not in display_word:
            message_label.config(text="🎉 You win!", fg="darkgreen")
            disable_all_buttons()
    else:
        attempts_left -= 1
        draw_hangman(max_attempts - attempts_left)

        if attempts_left == 0:
            message_label.config(text=f"💀 You lose! Word was '{word}'.", fg="red")
            disable_all_buttons()

# Disable all letter buttons
def disable_all_buttons():
    for btn in letter_buttons:
        btn.config(state="disabled", bg="gray")
    reset_button.pack(pady=10)

# Create A–Z buttons
letter_frame = tk.Frame(root, bg="#ffe6f0")
letter_frame.pack(pady=15)

def create_letter_buttons():
    global letter_buttons
    letter_buttons.clear()
    for widget in letter_frame.winfo_children():
        widget.destroy()

    for idx, letter in enumerate(string.ascii_uppercase):
        btn = tk.Button(letter_frame, text=letter, width=4, height=2,
                        font=("Arial", 12, "bold"), bg="#ff69b4", fg="white",
                        activebackground="#ff1493", activeforeground="white",
                        command=lambda l=letter.lower(), b=None: None)  # placeholder
        btn.grid(row=idx // 9, column=idx % 9, padx=3, pady=3)
        letter_buttons.append(btn)

    for btn in letter_buttons:
        btn.config(command=lambda l=btn["text"].lower(), b=btn: guess_letter(l, b))

# Reset game
def reset_game():
    global guessed_letters, attempts_left, word, category
    guessed_letters.clear()
    attempts_left = max_attempts
    canvas.delete("all")
    draw_hanger()

    category, word_list = random.choice(list(word_categories.items()))
    word = random.choice(word_list).lower()

    category_label.config(text=f"Category: {category}")
    word_display.config(text="_ " * len(word))
    message_label.config(text="", fg="green")

    create_letter_buttons()
    reset_button.pack_forget()

# Reset button
reset_button = tk.Button(root, text="🔄 Play Again", font=("Arial", 12, "bold"),
                         bg="#4CAF50", fg="white", activebackground="#45a049",
                         activeforeground="white", command=reset_game)

# Start the first game
reset_game()

root.mainloop()
