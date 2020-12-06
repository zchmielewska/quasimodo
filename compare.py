import numpy as np
import pandas as pd
import os
from tkinter import messagebox as msg
from datetime import datetime
from pathlib import Path
from utils import *


def run_comparison(lhs, rhs, output, settings, new_settings):

    # Output folder can't have space at the end
    while output[-1] == " ":
        output = output[:-1]

    # New settings will be saved to settings.txt for future usage
    new_settings['lhs_filepath'] = lhs
    new_settings['rhs_filepath'] = rhs
    new_settings['output_folder'] = output

    # Paths need to be properly formatted
    lhs_filepath = Path(lhs)
    rhs_filepath = Path(rhs)
    output_folder = Path(output)

    # Filepath must exist
    if not lhs_filepath.exists():
        msg.showwarning("File does not exist", "The left file does not exist. Please try again.")
        return

    if not rhs_filepath.exists():
        msg.showwarning("File does not exist", "The right file does not exist. Please try again.")
        return

    if not output_folder.exists():
        answer = msg.askyesno("Create output folder", "The output folder does not exist. Do you want to create it?")
        if answer is True:
            try:
                os.makedirs(output_folder)
                print(output_folder)
            except OSError:
                msg.showwarning("Creation of the directory %s failed" % str(output_folder))
        else:
            return

    output = compare(lhs_filepath, rhs_filepath)

    # Results are stored in quasimodo_YYYYMMDD.xlsx file
    # todo: what is user want output as csv
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "quasimodo_" + timestamp + ".xlsx"
    filepath = output_folder / filename
    output.to_excel(filepath, index = False)
    msg.showinfo("Output file", "Created file:\n" + str(filepath))

    # If users changed settings, they are written to text file
    if new_settings != settings:
        file = open("settings.txt", "w")
        file.write(str(new_settings))
        file.close()


def compare(lhs_filepath, rhs_filepath):
    # todo: what if separator is comma?
    # todo: what if file is excel?
    lhs = pd.read_csv(lhs_filepath, sep=";")
    rhs = pd.read_csv(rhs_filepath, sep=";")

    print(lhs)

    common_cols = np.intersect1d(np.array(lhs.columns), np.array(rhs.columns))
    lhs_only_cols = np.setdiff1d(np.array(lhs.columns), common_cols)
    rhs_only_cols = np.setdiff1d(np.array(rhs.columns), common_cols)

    # rhs has fewer rows
    if len(lhs) - len(rhs):
        zero_like_row = []
        for c in rhs.columns:
            if is_string_dtype(rhs[c]):
                zero_like_row.append("")
            else:
                zero_like_row.append(0)

        zeros = pd.DataFrame(data=[zero_like_row], columns=list(rhs.columns))
        frames = [rhs, zeros]
        rhs = pd.concat(frames)

    # lhs has fewer rows
    if len(rhs) - len(lhs):
        zero_like_row = []
        for c in lhs.columns:
            if is_string_dtype(lhs[c]):
                zero_like_row.append("")
            else:
                zero_like_row.append(0)

        zeros = pd.DataFrame(data=[zero_like_row], columns=list(lhs.columns))
        frames = [lhs, zeros]
        lhs = pd.concat(frames)

    output = pd.DataFrame()

    # Compare common columns
    for col in common_cols:
        result = compare_cols(lhs[col], rhs[col])
        output[col] = list(result)

    # Add LHS only cols
    for col in lhs_only_cols:
        output[col] = "only_in_left"

    # Add RHS only cols
    for col in rhs_only_cols:
        output[col] = "only_in_right"

    return output
