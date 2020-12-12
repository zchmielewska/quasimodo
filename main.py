import ast
import tkinter as tk
from tkinter import ttk
from compare import *
from pathlib import Path

# Load configuration
# If settings file doesn't exist, create it; otherwise read it
if not Path("settings.txt").exists():
    file = open("settings.txt", "w+")
    settings = {
        'lhs_filepath': "",
        'rhs_filepath': "",
        'output_folder': "",
        'delimiter': ",",
    }
    file.write(str(settings))
    file.close()
else:
    file = open("settings.txt", "r")
    contents = file.read()
    settings = ast.literal_eval(contents)
    file.close()

# If user changes settings, they will be saved in txt file
new_settings = settings.copy()

# Create instance
window = tk.Tk()

# Add a title
window.title("quasimodo | compare tables")

# Create tabs
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Main")
tabControl.pack(expand=1, fill="both")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="Settings")

# Left entry box
lhs = tk.StringVar()
tk.Label(tab1, text="Left:").grid(row=0, column=0, sticky="W")
lhs_entry = tk.Entry(tab1, textvariable=lhs, width=48)
lhs_entry.insert(0, settings['lhs_filepath'])
lhs_entry.grid(row=0, column=1)
lhs_entry.focus()

# Right entry box
rhs = tk.StringVar()
tk.Label(tab1, text="Right:").grid(row=1, column=0, sticky="W")
rhs_entry = tk.Entry(tab1, textvariable=rhs, width=48)
rhs_entry.insert(0, settings['rhs_filepath'])
rhs_entry.grid(row=1, column=1)

# Output folder
tk.Label(tab1, text="Output folder:").grid(row=2, column=0, sticky="W")
output = tk.StringVar()
output_entry = tk.Entry(tab1, textvariable=output, width=48)
output_entry.insert(0, settings['output_folder'])
output_entry.grid(row=2, column=1)

# Add padding to each widget in tab1
for child in tab1.winfo_children():
    child.grid_configure(padx=5, pady=3)

# todo: tab2 add delimiter button
tk.Label(tab2, text="Delimiter:").grid(column=0, row=0)
delimiter = tk.StringVar(tab2, settings["delimiter"])
delimiter_rad1 = tk.Radiobutton(tab2, text="Comma", variable=delimiter, value=",")
delimiter_rad2 = tk.Radiobutton(tab2, text="Semicolon", variable=delimiter, value=";")
delimiter_rad1.grid(column=1, row=0)
delimiter_rad2.grid(column=2, row=0)

# Compare button
# todo: create a function for new_settings creation where you get and sanitize all inputs
compare_button = tk.Button(tab1, text="Compare", command=lambda: run_comparison(lhs.get(), rhs.get(), output.get(),
                                                                                delimiter.get(),
                                                                                settings, new_settings))
compare_button.grid(row=3, columnspan=2)

# Start GUI
window.mainloop()