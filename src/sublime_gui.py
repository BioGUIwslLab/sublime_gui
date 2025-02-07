import os
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def run_pipeline(input_file, mac2unix):
    # Select input file
    infile = os.path.basename(input_file)
    os.chdir(os.path.dirname(input_file))
    input_file_fixed = str(input_file).replace("/","\\")
    # Choose between dos and mac
    os_opt = "dos" if not mac2unix else "mac"

    command = f"{os_opt}2unix -e {infile}; subl -w {infile}"

    try:
        app.after(0, lambda: messagebox.showinfo("Success", f"Opening {input_file_fixed} in Sublime Text..."))
        subprocess.run(["wsl", "bash", "-c", command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

    except subprocess.CalledProcessError as e:
        app.after(0, lambda: messagebox.showerror("Error", str(e)))

def start_thread():
    input_file = input_file_var.get()
    mac2unix = mac2unix_var.get()

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input file.")
        return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, mac2unix))
    thread.start()

def select_operation():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("Sublime GUI")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_operation).grid(row=0, column=2, padx=10, pady=10)

# Checkbox for additional option
mac2unix_var = tk.BooleanVar(value=False)
tk.Checkbutton(app, text="Input file derived from a mac machine", variable=mac2unix_var).grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=2, column=1, padx=10, pady=20)

app.mainloop()
