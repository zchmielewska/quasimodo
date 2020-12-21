import ast
import tkinter as tk
from tkinter import ttk
from compare import *
from pathlib import Path

# Load configuration
# If settings file doesn't exist, create it; otherwise read it
if not Path("settings.txt").exists():
    file = open("settings.txt", "w+")
    current_settings = {
        'lhs': "",
        'rhs': "",
        'output': "",
        'delimiter': ",",
        'columns_subset': ""
    }
    file.write(str(current_settings))
    file.close()
else:
    file = open("settings.txt", "r")
    contents = file.read()
    current_settings = ast.literal_eval(contents)
    file.close()

# User might change settings
settings = current_settings.copy()

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

# Tab1: Left entry box
lhs = tk.StringVar()
tk.Label(tab1, text="Left:").grid(row=0, column=0, sticky="W")
lhs_entry = tk.Entry(tab1, textvariable=lhs, width=48)
lhs_entry.insert(0, settings['lhs'])
lhs_entry.grid(row=0, column=1)
lhs_entry.focus()

# Tab1: Right entry box
rhs = tk.StringVar()
tk.Label(tab1, text="Right:").grid(row=1, column=0, sticky="W")
rhs_entry = tk.Entry(tab1, textvariable=rhs, width=48)
rhs_entry.insert(0, settings['rhs'])
rhs_entry.grid(row=1, column=1)

# Tab1: Output folder
tk.Label(tab1, text="Output folder:").grid(row=2, column=0, sticky="W")
output = tk.StringVar()
output_entry = tk.Entry(tab1, textvariable=output, width=48)
output_entry.insert(0, settings['output'])
output_entry.grid(row=2, column=1)

# Add padding to each widget in tab1
for child in tab1.winfo_children():
    child.grid_configure(padx=5, pady=3)

# Tab2: Delimiter
tk.Label(tab2, text="Delimiter:").grid(row=0, column=0, sticky="W")
delimiter = tk.StringVar(tab2, settings["delimiter"])
delimiter_rad1 = tk.Radiobutton(tab2, text="Comma", variable=delimiter, value=",")
delimiter_rad2 = tk.Radiobutton(tab2, text="Semicolon", variable=delimiter, value=";")
delimiter_rad1.grid(row=0, column=1, sticky="W")
delimiter_rad2.grid(row=0, column=2, sticky="W")

# Tab2: Subset of columns
tk.Label(tab2, text="Columns subset:").grid(row=1, column=0, sticky="W")
columns_subset = tk.StringVar(tab2, "")
columns_subset_entry = tk.Entry(tab2, textvariable=columns_subset, width=48)
columns_subset_entry.grid(row=1, column=1, columnspan=2)

# Add padding to each widget in tab2
for child in tab2.winfo_children():
    child.grid_configure(padx=5, pady=3)

# Final: Compare button
compare_button = tk.Button(tab1, text="Compare", command=lambda: run(settings = {
    'lhs': lhs.get(),
    'rhs': rhs.get(),
    'output': output.get(),
    'delimiter': delimiter.get(),
    'columns_subset': columns_subset.get()
}))
compare_button.grid(row=3, columnspan=2)

# Start GUI
window.mainloop()