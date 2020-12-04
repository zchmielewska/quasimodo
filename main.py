import tkinter as tk
from tkinter import ttk
from compare import *

# Create instance
window = tk.Tk()
# window.resizable(0, 0)

# Add a title
window.title("quasimodo | compare tables")

tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Main")
tabControl.pack(expand=1, fill="both")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="Settings")

# Left entry box
lhs_filepath = tk.StringVar()
tk.Label(tab1, text="First file:").grid(row=0, column=0, sticky="W")
lhs_entry = tk.Entry(tab1, textvariable=lhs_filepath, width=32)
lhs_entry.grid(row=0, column=1)
lhs_entry.focus()

# Right entry box
rhs_filepath = tk.StringVar()
tk.Label(tab1, text="Second file:").grid(row=1, column=0, sticky="W")
rhs_entry = tk.Entry(tab1, textvariable=rhs_filepath, width=32)
rhs_entry.grid(row=1, column=1)

# Output folder
tk.Label(tab1, text="Output folder:").grid(row=2, column=0, sticky="W")
output_folder = tk.StringVar()
output_entry = tk.Entry(tab1, textvariable=output_folder, width=32)
output_entry.grid(row=2, column=1)

# Compare button
compare_button = tk.Button(tab1, text="Compare", command=lambda: run_comparison(lhs_filepath.get(), rhs_filepath.get()))
compare_button.grid(row=3, columnspan=2)

# Add padding to each widget
for child in tab1.winfo_children():
    child.grid_configure(padx=5, pady=3)

# Start GUI
window.mainloop()
