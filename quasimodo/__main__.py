import ast
import threading
import tkinter as tk
from quasimodo import run_comparison
from tkinter import ttk
from tkinter import scrolledtext
from pathlib import Path

# todo: what is subset is selected and there are no columns in this subset
# todo: progressbar
# todo: order of the columns
# todo: output folder cant be empty


# Separate thread for the main run function
def thread_run(settings, progress_bar, log):
    # Call work function
    t=threading.Thread(target=run_comparison.run, args=(settings, progress_bar, log))
    t.start()


def main():
    entry_width = 80

    # Load configuration
    # If settings file doesn't exist, create it; otherwise read it
    if not Path("settings.txt").exists():
        file = open("settings.txt", "w+")
        current_settings = {
            'lhs': "",
            'rhs': "",
            'output': "",
            'delimiter': ",",
            'decimal': ".",
            'numerical_precision': "",
            'comment': "",
            'columns_subset': "",
            'blank_tile': ""
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
    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Main")
    tab_control.pack(expand=1, fill="both")
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Settings")

    # Tab1 configuration
    tab1.columnconfigure(0, weight=0)
    tab1.columnconfigure(1, weight=1)

    # Tab1 | Left entry box
    lhs = tk.StringVar()
    lhs_label = tk.Label(tab1, text="Left:")
    lhs_label.grid(row=0, column=0, sticky="W", padx=5, pady=(12, 3))
    lhs_entry = tk.Entry(tab1, textvariable=lhs)
    lhs_entry.insert(0, settings['lhs'])
    lhs_entry.grid(row=0, column=1, sticky="WE", padx=5, pady=(12, 3))
    lhs_entry.focus()

    # Tab1 | Right entry box
    rhs = tk.StringVar()
    rhs_label = tk.Label(tab1, text="Right:")
    rhs_label.grid(row=1, column=0, sticky="W", padx=5, pady=3)
    rhs_entry = tk.Entry(tab1, textvariable=rhs)
    rhs_entry.insert(0, settings['rhs'])
    rhs_entry.grid(row=1, column=1, sticky="WE", padx=5, pady=3)

    # Tab1 | Output folder
    output_label = tk.Label(tab1, text="Output folder:")
    output_label.grid(row=2, column=0, sticky="W", padx=5, pady=3)
    output = tk.StringVar()
    output_entry = tk.Entry(tab1, textvariable=output)
    output_entry.insert(0, settings['output'])
    output_entry.grid(row=2, column=1, sticky="WE", padx=5, pady=3)

    # Tab 1 | Progressbar
    progress_bar = ttk.Progressbar(tab1, orient="horizontal", mode="determinate")
    progress_bar.grid(row=3, column=1, sticky="NSEW", padx=5, pady=10)
    progress_bar['maximum'] = 100
    # progress_bar['value'] = 50
    
    # Tab1 | Log
    log = scrolledtext.ScrolledText(tab1, height=12)
    log.grid(row=4, columnspan=2, sticky="NSEW", padx=5, pady=(3, 12))
    log.insert(tk.END, "Log...\n")
    log.configure(state='disabled')

    # Tab2 | Delimiter
    tk.Label(tab2, text="Delimiter:").grid(row=0, column=0, sticky="W")
    delimiter = tk.StringVar(tab2, settings["delimiter"])
    delimiter_rad1 = tk.Radiobutton(tab2, text="Comma", variable=delimiter, value=",")
    delimiter_rad2 = tk.Radiobutton(tab2, text="Semicolon", variable=delimiter, value=";")
    delimiter_rad3 = tk.Radiobutton(tab2, text="Tab", variable=delimiter, value="\t")
    delimiter_rad1.grid(row=0, column=1, sticky="W")
    delimiter_rad2.grid(row=0, column=2, sticky="W")
    delimiter_rad3.grid(row=0, column=3, sticky="W")

    # Tab2 | Decimal
    tk.Label(tab2, text="Decimal:").grid(row=1, column=0, sticky="W")
    decimal = tk.StringVar(tab2, settings["decimal"])
    decimal_rad1 = tk.Radiobutton(tab2, text="Dot", variable=decimal, value=".")
    decimal_rad2 = tk.Radiobutton(tab2, text="Comma", variable=decimal, value=",")
    decimal_rad1.grid(row=1, column=1, sticky="W")
    decimal_rad2.grid(row=1, column=2, sticky="W")

    # Tab2 | Comment
    tk.Label(tab2, text="Comment:").grid(row=2, column=0, sticky="W")
    comment = tk.StringVar(tab2, "")
    comment_entry = tk.Entry(tab2, textvariable=comment, width=10)
    comment_entry.grid(row=2, column=1, columnspan=2, sticky="W")
    comment_entry.insert(0, settings['comment'])

    # Tab2 | Numerical precision
    tk.Label(tab2, text="Numerical precision (10^x):").grid(row=3, column=0, sticky="W")
    numerical_precision = tk.IntVar(tab2)
    numerical_precision.set(settings['numerical_precision'])
    numerical_precision_spin = tk.Spinbox(tab2, from_=-10, to=10, textvariable=numerical_precision)
    numerical_precision_spin.grid(row=3, column=1, sticky="W")

    # Tab 2 | Columns subset
    tk.Label(tab2, text="Columns subset:").grid(row=4, column=0, sticky="W")
    columns_subset = tk.StringVar(tab2, "")
    columns_subset_entry = tk.Entry(tab2, textvariable=columns_subset, width=entry_width)
    columns_subset_entry.grid(row=4, column=1, columnspan=3)
    columns_subset_entry.insert(0, settings['columns_subset'])

    # Tab2 | Blank tile
    tk.Label(tab2, text="Blank tile <*>:").grid(row=5, column=0, sticky="W")
    blank_tile = tk.StringVar(tab2, "")
    blank_tile_entry = tk.Entry(tab2, textvariable=blank_tile, width=entry_width)
    blank_tile_entry.grid(row=5, column=1, columnspan=3)
    blank_tile_entry.insert(0, settings['blank_tile'])

    # Tab2 | Add padding to each widget
    for child in tab2.winfo_children():
        child.grid_configure(padx=5, pady=3)

    # Final: Compare button
    compare_button = tk.Button(tab1, text="Compare", command=lambda: thread_run(settings={
        'lhs': lhs.get(),
        'rhs': rhs.get(),
        'output': output.get(),
        'delimiter': delimiter.get(),
        'decimal': decimal.get(),
        'comment': comment.get(),
        'numerical_precision': numerical_precision.get(),
        'columns_subset': columns_subset.get(),
        'blank_tile': blank_tile.get()
    }, progress_bar=progress_bar, log=log))
    compare_button.grid(row=3, column=0, sticky="NSEW", padx=5, pady=10)

    # Start GUI
    window.mainloop()


if __name__ == "__main__":
    main()
