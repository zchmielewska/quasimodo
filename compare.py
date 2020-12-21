import numpy as np
import pandas as pd
import os
from tkinter import messagebox as msg
from datetime import datetime
from utils import *
from pathlib import Path


def run(settings):
    lhs_filepath = Path(settings['lhs'])
    rhs_filepath = Path(settings['rhs'])

    # Output folder can't have space(s) at the end
    if settings['output'] != "":
        while settings['output'][-1] == " ":
            settings['output'] = settings['output'][:-1]
    output_folder = Path(settings['output'])

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
            except OSError:
                msg.showwarning("Creation of the directory %s failed" % str(settings['output_folder']))
        else:
            return

    # Main comparison function
    output = compare(lhs_filepath, rhs_filepath, settings['delimiter'])

    # Results are stored in quasimodo_YYYYMMDD.xlsx file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "quasimodo_" + timestamp + ".xlsx"
    filepath = output_folder / filename
    output.to_excel(filepath, index=False)
    msg.showinfo("Output file", "Created file:\n" + str(filepath))

    # Save settings for future use
    file = open("settings.txt", "w")
    file.write(str(settings))
    file.close()


def compare(lhs_filepath, rhs_filepath, delimiter):

    # todo: what if file is excel?
    lhs = pd.read_csv(lhs_filepath, sep=delimiter)
    rhs = pd.read_csv(rhs_filepath, sep=delimiter)

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
