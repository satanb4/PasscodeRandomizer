# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
	
# Developer: Sayan Bandopadhyay
# Date: 24/02/2023
# Version: 1.0
# Description: This is the main code for the project. It contains the GUI for the Password Randomizer.
# License: http://creativecommons.org/licenses/by-sa/3.0/

import tkinter as tk
from tkinter import messagebox
import time
import random
import os

LARGE_FONT= ("Verdana", 12)
passcode = ""
time_taken = 0


class PasswordRandomizer(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.user_mode = ""
        self.error_codes = []
        self.given_up = False

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont, **kwargs):
        frame = self.frames[cont]
        frame.tkraise()
    
    def restart(self):
        self.destroy()
        self.__init__()
        

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        self.number = ""
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Set Password", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        tk.Label(self, text="Enter Passcode (Integer):- ")
        e = tk.Entry(self)
        e.pack(pady=20,padx=20)

        variable = tk.StringVar(self)
        variable.set("Victim") # default value
        w = tk.OptionMenu(self, variable, "Victim", "Attacker")
        w.pack(pady=20,padx=20)

        submit_button = tk.Button(self, text="Submit", font=("Arial", 20), width="12",
                                command=lambda: self.submit(e.get(), variable.get()))

        submit_button.pack()
    
    def submit(self, num, mode):
        if not num:
            print("No secret code entered")
            messagebox.showinfo("C'mon!", "Atleast enter a secret code!")
            return
        else:
            global passcode
            passcode = num
            self.controller.user_mode = mode
            print(f"Secret Code:- {passcode}")
            print(f"User Mode:- {self.controller.user_mode}")
        self.controller.show_frame(PageOne)
        

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        # Add entered code variables
        self.entered_code = ""
        self.start_time = 0
        self.controller = controller
        self.trial = 0

        # Setup for the page
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Check Passcode Validity", font=LARGE_FONT)
        label.grid(row=0, columnspan=3)

        # Create display for showing entered code as asterisks
        self.display = tk.Label(self, font=("Arial", 20), width=4)
        self.display.grid(row=1, columnspan=3)

        # Assign the buttons
        self.assignButtons()

        # Create submit button
        submit_button = tk.Button(self, text="Submit", font=("Arial", 20), width="12",
                                command=lambda: self.check_code())
        submit_button.grid(row="7", columnspan="3")

        exit_button = tk.Button(self, text="Give Up?", font=("Arial", 20), width="12", command=lambda:  self.give_up())
        exit_button.grid(row="8", columnspan="3")

    def assignButtons(self):
        # Create keypad buttons with numbers 0-9
        self.buttons = []
        for i in range(10):
            button = tk.Button(self, text=str(i), font=("Arial", 20), width=4,
                            command=lambda num=i: self.press(num))
            self.buttons.append(button)

        # Arrange keypad buttons in grid layout
        self.buttons[1].grid(row=2, column=0)
        self.buttons[2].grid(row=2, column=1)
        self.buttons[3].grid(row=2, column=2)
        self.buttons[4].grid(row=3, column=0)
        self.buttons[5].grid(row=3, column=1)
        self.buttons[6].grid(row=3, column=2)
        self.buttons[7].grid(row=4, column=0)
        self.buttons[8].grid(row=4, column=1)
        self.buttons[9].grid(row=4, column=2)
        self.buttons[0].grid(row=5, columnspan="3")
    
    # Define functions for keypad buttons
    def press(self,num):

        # Append pressed number to entered code
        self.entered_code += str(num)

        # Update display with asterisks
        self.display.config(text="*" * len(self.entered_code))
        self.display.update()

        # Record start time if first digit is entered
        if len(self.entered_code) == 1:
            self.start_time = time.time()
            print(f"start_time:- {self.start_time}")
        # self.shuffle_numbers() # Uncomment to shuffle numbers after each button press
    
    def shuffle_numbers(self):
        # Get a list of numbers from 0 to 9 and shuffle them randomly
        numbers = list(range(10))
        random.shuffle(numbers)
        # Update each button's text with a new number from the list
        for i in range(10):
            self.buttons[i].config(text=numbers[i], command=lambda num=numbers[i]: self.press(num))
    
    def reset(self):
        # Clear entered code and display, go back to login screen
        self.entered_code = ""
        self.display.config(text="")
        self.display.update()
    
    def check_code(self):
        # Check if entered code matches passcode
        print(f"User Code:- {self.entered_code}")
        self.trial+=1
        print(f"Trial:- {self.trial}")
        if passcode == self.entered_code:
            # Show success message and go to next screen
            messagebox.showinfo("Success", "Correct passcode!")
            end_time = time.time()
            print(f"end_time:- {end_time}")
            global time_taken
            time_taken = end_time - self.start_time
            print(f"time_taken:- {time_taken}")
            self.go_to_page_two()
        else:
            # Show error message and clear entered code and display
            self.controller.error_codes.append(self.entered_code)
            messagebox.showerror("Error", "Wrong passcode!")
            self.entered_code = ""
            self.reset()
    
    def give_up(self):
        # Clear entered code and display, go back to login screen
        end_time = time.time()
        global time_taken
        time_taken = end_time - self.start_time
        self.controller.given_up = True
        self.go_to_page_two()

    def go_to_page_two(self):
        self.controller.frames[PageTwo].update_label(trials=self.trial)
        self.controller.show_frame(PageTwo)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Final Result", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        print(f"Time Taken Final:- {time_taken}")
        self.label1 = tk.Label(self, text=f"0", font=LARGE_FONT)
        self.label1.pack(pady=10,padx=10)

        self.label2 = tk.Label(self, text=f"0", font=LARGE_FONT)
        self.label2.pack(pady=10,padx=10)

        self.label3 = tk.Label(self, text=f"0", font=LARGE_FONT)
        self.label3.pack(pady=10,padx=10)
        
        self.label4 = tk.Label(self, text=f"0", font=LARGE_FONT)
        self.label4.pack(pady=10,padx=10)

        self.label5 = tk.Label(self, text=f"0", font=LARGE_FONT)
        self.label5.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Restart",
                            command=lambda: self.restart())
        button1.pack()
        button2 = tk.Button(self, text="Exit",
                            command=lambda: controller.destroy())
        button2.pack()
    
    def restart(self):
        global time_taken, passcode
        time_taken = 0
        passcode = "" 
        self.controller.restart()
    
    def update_label(self, trials):
        global time_taken, passcode
        self.time_taken = time_taken
        self.passcode = passcode
        self.trials = trials
        self.label1.config(text=f"User Mode:- {self.controller.user_mode}", font=LARGE_FONT)
        self.label1.update()
        self.label2.config(text=f"Time Taken:- {self.time_taken:.2f}s", font=LARGE_FONT)
        self.label2.update()
        self.label3.config(text=f"Passcode Length:- {len(self.passcode)} char(s)", font=LARGE_FONT)
        self.label3.update()
        self.label4.config(text=f"Trials:- {trials}", font=LARGE_FONT)
        self.label4.update()
        self.label5.config(text=f"Erroneous Codes:- {' | '.join(self.controller.error_codes)}", font=LARGE_FONT)
        self.label5.update()
        self.write_to_file()

    def write_to_file(self):
        __location__ = os.path.realpath(os.getcwd())
        output_file = os.path.join(__location__,"control.csv")
        with open(output_file, 'a+') as f:
            if os.stat(output_file).st_size == 0:
                f.write("user_mode,passcode,given_up,time_taken,passcode_length,trial,error_codes\n")
            f.write(f"{self.controller.user_mode},{self.passcode},{self.controller.given_up},{self.time_taken:.2f},{len(self.passcode)},{self.trials},{self.controller.error_codes}\n")
        return 0
        
if __name__ == "__main__":
    app = PasswordRandomizer()
    app.mainloop()