import ast
import tkinter as tk
from quasimodo import run_comparison
from tkinter import ttk
from tkinter import scrolledtext
from pathlib import Path


def main():
    # todo: log scroll to the end
    # todo: compare only the first row of files
    # todo: what is subset is selected and there are no columns in this subset
    # todo: the same/different flag
    # todo: what if file is excel?
    # todo: progressbar
    # todo: # LHS has fewer rows + # RHS has fewer rows --> externalize as functions
    entry_width = 72

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
    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Main")
    tab_control.pack(expand=1, fill="both")
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Settings")

    # Tab1 | Paths frame
    paths_frame = ttk.LabelFrame(tab1, text="Paths")
    paths_frame.grid(row=0, columnspan=2)
    paths_frame.grid_configure(padx=10, pady=10)

    # Tab1 | Paths frame | Left entry box
    lhs = tk.StringVar()
    tk.Label(paths_frame, text="Left:").grid(row=0, column=0, sticky="W")
    lhs_entry = tk.Entry(paths_frame, textvariable=lhs, width=entry_width)
    lhs_entry.insert(0, settings['lhs'])
    lhs_entry.grid(row=0, column=1)
    lhs_entry.focus()

    # Tab1 | Paths frame | Right entry box
    rhs = tk.StringVar()
    tk.Label(paths_frame, text="Right:").grid(row=1, column=0, sticky="W")
    rhs_entry = tk.Entry(paths_frame, textvariable=rhs, width=entry_width)
    rhs_entry.insert(0, settings['rhs'])
    rhs_entry.grid(row=1, column=1)

    # Tab1 | Paths frame | Output folder
    tk.Label(paths_frame, text="Output folder:").grid(row=2, column=0, sticky="W")
    output = tk.StringVar()
    output_entry = tk.Entry(paths_frame, textvariable=output, width=entry_width)
    output_entry.insert(0, settings['output'])
    output_entry.grid(row=2, column=1)

    # Tab 1 | Paths frame | Add padding to widgets
    for child in paths_frame.winfo_children():
        child.grid_configure(padx=5, pady=3)

    # Tab1 | Log
    log_scr = scrolledtext.ScrolledText(tab1, width=65, height=12)
    log_scr.grid(row=5, columnspan=2)
    log_scr.grid_configure(padx=10, pady=10)
    log_scr.insert(tk.END, "Log...\n\n")

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
    columns_subset_entry = tk.Entry(tab2, textvariable=columns_subset, width=entry_width)
    columns_subset_entry.grid(row=1, column=1, columnspan=2)
    columns_subset_entry.insert(0, settings['columns_subset'])

    # Add padding to each widget in tab2
    for child in tab2.winfo_children():
        child.grid_configure(padx=5, pady=3)

    # Final: Compare button
    compare_button = tk.Button(tab1, text="Compare", command=lambda: run_comparison.run(settings={
        'lhs': lhs.get(),
        'rhs': rhs.get(),
        'output': output.get(),
        'delimiter': delimiter.get(),
        'columns_subset': columns_subset.get()
    }, log_scr=log_scr))
    compare_button.grid(row=3, columnspan=2)

    # Start GUI
    window.mainloop()


if __name__ == "__main__":
    main()
