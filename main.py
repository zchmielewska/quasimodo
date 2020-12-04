import tkinter as tk
from compare import *

# Create instance
window = tk.Tk()
# window.geometry("800x640")

# Disable resizing
window.resizable(0, 0)

# Add a title
window.title("quasimodo | compare tables")

# Frame for inputs
inputs_frame = tk.LabelFrame(window, text="Inputs")
inputs_frame.grid(row=0, column=0, padx=5, pady=5)

# Left entry box
lhs_filepath = tk.StringVar()
tk.Label(inputs_frame, text="Left").grid(row=0, column=0)
lhs_entry = tk.Entry(inputs_frame, textvariable=lhs_filepath, width=32)
lhs_entry.grid(row=1, column=0, padx=5, pady=5)
lhs_entry.focus()

# Right entry box
rhs_filepath = tk.StringVar()
tk.Label(inputs_frame, text="Right").grid(row=0, column=1)
tk.Entry(inputs_frame, textvariable=rhs_filepath, width=32).grid(row=1, column=1, padx=5, pady=5)

# todo path for output

# Compare button
compare_button = tk.Button(window, text="Compare", command=lambda: quasimodo(lhs_filepath.get(), rhs_filepath.get()))
compare_button.grid(row=2, columnspan=2, padx=5, pady=10)

# Start GUI
window.mainloop()
