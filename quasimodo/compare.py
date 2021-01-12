import numpy as np
import pandas as pd
import tkinter as tk
import os
from .utils import compare_cols, ensure_existence
from pandas.api.types import is_string_dtype
from datetime import datetime
from pathlib import Path
from tkinter import messagebox as msg


def run(settings, log_scr):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_scr.insert(tk.END, "Starting job: " + timestamp + "\n\n")

    lhs_path = Path(settings['lhs'])
    rhs_path = Path(settings['rhs'])

    # Prepare and check paths
    output_folder = sanitize_output(settings)
    paths_check = ensure_existence(lhs_path, rhs_path, output_folder, log_scr)  # paths must exist
    if paths_check > 0:
        return

    # Approach differs depending if user chooses files or folders
    comparison_sources = pd.DataFrame(columns=["lhs", "rhs"])

    # file + folder
    if (os.path.isdir(lhs_path) and os.path.isfile(rhs_path)) or (os.path.isfile(lhs_path) and os.path.isdir(rhs_path)):
        msg.showwarning("Inconsistent sources", "Left and right must be either both files or folders.")

    # folder + folder
    if os.path.isdir(lhs_path) and os.path.isdir(rhs_path):
        lhs_files = [f for f in os.listdir(lhs_path) if os.path.isfile(os.path.join(lhs_path, f))]
        rhs_files = [f for f in os.listdir(rhs_path) if os.path.isfile(os.path.join(rhs_path, f))]
        common_files = np.intersect1d(np.array(lhs_files), np.array(rhs_files))  # todo: add only csv files
        for common_file in common_files:
            comparison_sources = comparison_sources.append({"lhs": os.path.join(lhs_path, common_file),
                                                            "rhs": os.path.join(rhs_path, common_file)},
                                                           ignore_index=True)
    # file + file
    if os.path.isfile(lhs_path) and os.path.isfile(rhs_path):
        comparison_sources = comparison_sources.append({"lhs": lhs_path, "rhs": rhs_path}, ignore_index=True)

    # main comparison
    for index, row in comparison_sources.iterrows():
        # For folder comparison, show the file number
        if os.path.isdir(lhs_path) and os.path.isdir(rhs_path):
            log_scr.insert(tk.END, "[" + str(index+1) + "/" + str(len(comparison_sources)) + "]\n")
        log_scr.insert(tk.END, "LHS: " + str(row['lhs']) + "\nRHS: " + str(row['rhs']) + "\n")

        try:
            lhs = pd.read_csv(row['lhs'], sep=settings['delimiter'])
        except pd.errors.EmptyDataError:
            lhs = pd.DataFrame()
        try:
            rhs = pd.read_csv(row['rhs'], sep=settings['delimiter'])
        except pd.errors.EmptyDataError:
            rhs = pd.DataFrame()

        output = compare(lhs, rhs, settings['columns_subset'])
        lhs_filename = os.path.splitext(os.path.basename(row['lhs']))[0]
        rhs_filename = os.path.splitext(os.path.basename(row['rhs']))[0]
        if lhs_filename == rhs_filename:
            output_filename = lhs_filename + "_quasimodo_" + timestamp + ".xlsx"
        else:
            output_filename = lhs_filename + "_" + rhs_filename + "_quasimodo_" + timestamp + ".xlsx"
        filepath = output_folder / output_filename
        output.to_excel(filepath, index=False)
        log_scr.insert(tk.END, "Out: " + str(filepath) + "\n\n")

    # Save settings for future use
    file = open("settings.txt", "w")
    file.write(str(settings))
    file.close()


def compare(lhs, rhs, columns_subset):
    columns_subset_list = columns_subset.split(",")
    the_same_flag = True

    # There might be columns only in LHS or RHS
    common_cols = np.intersect1d(np.array(lhs.columns), np.array(rhs.columns))
    lhs_only_cols = np.setdiff1d(np.array(lhs.columns), common_cols)
    rhs_only_cols = np.setdiff1d(np.array(rhs.columns), common_cols)

    # User can choose to compare only a subset of columns
    if columns_subset != "":
        common_cols = np.intersect1d(common_cols, np.array(columns_subset_list))
        lhs_only_cols = np.intersect1d(lhs_only_cols, np.array(columns_subset_list))
        rhs_only_cols = np.intersect1d(rhs_only_cols, np.array(columns_subset_list))

    # Tables differ if they contain different columns
    if len(lhs_only_cols) > 0 or len(rhs_only_cols) > 0:
        the_same_flag = False

    # RHS has fewer rows
    if len(lhs) - len(rhs) > 0:
        zero_like_row = []
        for c in rhs.columns:
            if is_string_dtype(rhs[c]):
                zero_like_row.append("")
            else:
                zero_like_row.append(0)

        zeros = pd.DataFrame(data=[zero_like_row], columns=list(rhs.columns))
        frames = [rhs, zeros]
        rhs = pd.concat(frames)

    # LHS has fewer rows
    if len(rhs) - len(lhs) > 0:
        zero_like_row = []
        for c in lhs.columns:
            if is_string_dtype(lhs[c]):
                zero_like_row.append("")
            else:
                zero_like_row.append(0)

        zeros = pd.DataFrame(data=[zero_like_row], columns=list(lhs.columns))
        frames = [lhs, zeros]
        lhs = pd.concat(frames)

    output = pd.DataFrame(index=range(max(len(lhs), len(rhs))))

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


def sanitize_output(settings):
    # Output folder can't have space(s) at the end
    if settings['output'] != "":
        while settings['output'][-1] == " ":
            settings['output'] = settings['output'][:-1]
    output_folder = Path(settings['output'])
    return output_folder
