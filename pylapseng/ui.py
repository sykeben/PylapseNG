# Perform imports.
import tkinter.simpledialog as sd
import tkinter.messagebox   as mb

# Integer choice dialog.
def chooseInt(title:str, prompt:str, choices:list[int], default:int|None = None) -> int:
    while True:
        choice = sd.askinteger(title, prompt, initialvalue=default)
        if (choice in choices):
            return choice
        elif (choice is None):
            return None
        else:
            mb.showerror("Input Error", "Please choose a valid number.")
