import numpy as np
import pandas as pd
import tkinter as tk
import os
from .utils import compare_cols
from pandas.api.types import is_string_dtype
from datetime import datetime
from pathlib import Path
from tkinter import messagebox as msg


def run(settings, log_scr):
    lhs_path = Path(settings['lhs'])
    rhs_path = Path(settings['rhs'])

    # Prepare and check input paths
    output_folder = sanitize_output(settings)
    paths_check = ensure_existence(lhs_path, rhs_path, output_folder, log_scr)  # paths must exist
    if paths_check > 0:
        return

    # folder + folder
    if os.path.isdir(lhs_path) and os.path.isdir(rhs_path):
        lhs_files = [f for f in os.listdir(lhs_path) if os.path.isfile(os.path.join(lhs_path, f))]
        rhs_files = [f for f in os.listdir(rhs_path) if os.path.isfile(os.path.join(rhs_path, f))]
        # todo add only csv files
        common_files = np.intersect1d(np.array(lhs_files), np.array(rhs_files))
        for common_file in common_files:
            # Main comparison function
            lhs_filepath = os.path.join(lhs_path, common_file)
            rhs_filepath = os.path.join(rhs_path, common_file)
            output = compare(lhs_filepath, rhs_filepath, settings['delimiter'])

            # Results are stored in quasimodo_YYYYMMDD.xlsx file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # common_file without extension in the filename
            filename = common_file + "_quasimodo_" + timestamp + ".xlsx"
            filepath = output_folder / filename
            output.to_excel(filepath, index=False)
            log_scr.insert(tk.END, "Created file:\n" + str(filepath) + "\n")

    # file + folder / folder + file
    if (os.path.isdir(lhs_path) and os.path.isfile(rhs_path)) or (os.path.isfile(lhs_path) and os.path.isdir(rhs_path)):
        msg.showwarning("Inconsistent sources", "Left and right must be either both files or folders.")

    # file + file
    if os.path.isfile(lhs_path) and os.path.isfile(rhs_path):
        # Main comparison function
        lhs_filepath = lhs_path
        rhs_filepath = rhs_path
        output = compare(lhs_filepath, rhs_filepath, settings['delimiter'])

        # Results are stored in quasimodo_YYYYMMDD.xlsx file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = "quasimodo_" + timestamp + ".xlsx"
        filepath = output_folder / filename
        output.to_excel(filepath, index=False)
        log_scr.insert(tk.END, "Created file:\n" + str(filepath) + "\n")

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
        result = utils.compare_cols(lhs[col], rhs[col])
        output[col] = list(result)

    # Add LHS only cols
    for col in lhs_only_cols:
        output[col] = "only_in_left"

    # Add RHS only cols
    for col in rhs_only_cols:
        output[col] = "only_in_right"

    return output


def sanitize_output(settings):
    # Output folder can't have space(s) at the end
    if settings['output'] != "":
        while settings['output'][-1] == " ":
            settings['output'] = settings['output'][:-1]
    output_folder = Path(settings['output'])
    return output_folder


def ensure_existence(lhs_path, rhs_path, output_folder, log_scr):
    paths_check = 0

    if not lhs_path.exists():
        msg.showwarning("File does not exist", "The left file does not exist. Please try again.")
        paths_check = paths_check + 1

    if not rhs_path.exists():
        msg.showwarning("File does not exist", "The right file does not exist. Please try again.")
        paths_check = paths_check + 1

    if not output_folder.exists():
        answer = msg.askyesno("Create output folder", "The output folder does not exist. Do you want to create it?")
        if answer is True:
            try:
                os.makedirs(output_folder)
                log_scr.insert(tk.END, "Created folder:\n" + str(output_folder) + "\n")
            except OSError:
                msg.showwarning("Creation of the directory %s failed" % str(output_folder))
                paths_check = paths_check + 1
        else:
            paths_check = paths_check + 1

    return paths_check