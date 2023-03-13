# Import Tkinter library
import tkinter as tk
import time
import random
from tkinter import messagebox

# Define global variables
passcode = "1234"  # Hardcoded passcode
entered_code = ""  # Code entered by user
start_time = None  # Time when user starts entering code
end_time = None  # Time when user submits code


# Define functions for keypad buttons
def press(num):
    global entered_code
    global start_time

    # Append pressed number to entered code
    entered_code += str(num)

    # Update display with asterisks
    display.config(text="*" * len(entered_code))

    # Record start time if first digit is entered
    if len(entered_code) == 1:
        start_time = time.perf_counter()

def shuffle_numbers():
    # Declare buttons as global variable
    global buttons
    # Get a list of numbers from 0 to 9 and shuffle them randomly
    numbers = list(range(10))
    random.shuffle(numbers)
    # Update each button's text with a new number from the list
    for i in range(10):
        buttons[i].config(text=numbers[i], command=lambda num=numbers[i]: press(num))



def submit():
    global entered_code
    global end_time

    # Record end time when submit button is pressed
    end_time = time.perf_counter()

    # Check if entered code matches passcode
    if entered_code == passcode:
        # Show success message and go to next screen
        messagebox.showinfo("Success", "Correct passcode!")
        next_screen()

    else:
        # Show error message and clear entered code and display
        messagebox.showerror("Error", "Wrong passcode!")
        entered_code = ""
        display.config(text="")


def reset(top):
    global entered_code

    # Clear entered code and display, go back to login screen
    entered_code = ""
    display.config(text="")
    top.destroy()
    root.deiconify()


def next_screen():
    root.withdraw()
    top = tk.Toplevel(root)
    top.title("Next Screen")

    reset_button = tk.Button(top, text="Reset",  command=lambda: reset(top))
    reset_button.pack(pady=10)

    timer_label = tk.Label(top, text=f"Time taken: {end_time - start_time:.2f} seconds")
    timer_label.pack(pady=10)



# Create root window for login screen
root = tk.Tk()
root.configure(background="white")
root.update()

root.title("Login Screen")

# Create display for showing entered code as asterisks
display = tk.Label(root, font=("Arial", 20), width=4)
display.grid(row=0, columnspan=3)

# Create keypad buttons with numbers 0-9
buttons = []

# def assignButtons():
for i in range(10):
    button = tk.Button(root, text=str(i), font=("Arial", 20), width=4,
                       command=lambda num=i: press(num))
    buttons.append(button)

# Arrange keypad buttons in grid layout
buttons[1].grid(row=1, column=0)
buttons[2].grid(row=1, column=1)
buttons[3].grid(row=1, column=2)
buttons[4].grid(row=2, column=0)
buttons[5].grid(row=2, column=1)
buttons[6].grid(row=2, column=2)
buttons[7].grid(row=3, column=0)
buttons[8].grid(row=3, column=1)
buttons[9].grid(row=3, column=2)
buttons[0].grid(row=4, columnspan="3")

# Create a button to shuffle  the numbers
shuffle_button = tk.Button(root, text="Randomize", font=("Arial", 20), width="12", command=lambda: shuffle_numbers())
shuffle_button.grid(row="5",columnspan="3")

# Create submit button
submit_button = tk.Button(root, text="Submit", font=("Arial", 20), width="12",
                          command=lambda: submit())
submit_button.grid(row="6", columnspan="3")

# Start main loop of root window
root.mainloop()