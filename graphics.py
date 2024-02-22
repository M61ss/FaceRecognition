import tkinter as tk

# ---------- functions ----------- #

def first_print():
    text = "Hello World!"
    text_output = tk.Label(root, text=text, fg="red", font=("Helvetica", 16))
    text_output.grid(row=0, column=0)

# ---------- functions ----------- #

root = tk.Tk()

root.geometry("600x600")
root.title("Identifier")
root.configure(background="#322e2e")

name_field = tk.Text(
    root, 
    height=10, 
    width=100, 
    padx=100, 
    pady=10, 
    bg="white", 
    font="Helvetica"
    )

first_button = tk.Button(text="Saluta!", command=first_print)
first_button.grid(row=0, column=0)

if __name__ == "__main__":
    root.mainloop()