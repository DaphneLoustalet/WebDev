# receive inputs and echo in an encrypted manner
import tkinter as tk
from tkinter import messagebox

def submit_password():
    password = entry.get()
    # You can use the password variable here for further processing
    # For example, you can print it to verify that it's working
    print("Your password is:", password)
    root.destroy()

root = tk.Tk()
root.title("Password Input")
root.geometry("300x100")

label = tk.Label(root, text="Enter your password:")
label.pack()

entry = tk.Entry(root, show="*")
entry.pack()

button = tk.Button(root, text="Submit", command=submit_password)
button.pack()

root.mainloop()
