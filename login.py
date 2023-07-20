import tkinter
from tkinter import messagebox

def handle_login(event=None):
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        with open('Credentials.txt', 'w') as file:
            file.write(f"Username: {username}\nPassword: {password}")
        messagebox.showinfo("Login Success", "Credentials saved to 'Credentials.txt'")
    else:
        messagebox.showwarning("Login Failed", "Please enter both username and passphrase.")

window = tkinter.Tk()
window.title('Login to UCD Schedule Builder')
window.geometry('750x550')
window.configure(bg='#022851')
window.bind('<Return>', handle_login)

frame = tkinter.Frame(bg='#022851')
login_label = tkinter.Label(frame, bg='#022851', fg='#FFFFFF', text='Login using your UCD Credentials')
username_label = tkinter.Label(frame, text='Username', bg='#022851', fg='#FFFFFF')
password_label = tkinter.Label(frame, text='Passphrase', bg='#022851', fg='#FFFFFF')

username_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))

login_button = tkinter.Button(frame, text="Login", bg="#FFBF00", fg="#FFFFFF", command=handle_login)

login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()

window.mainloop()
