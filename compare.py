import numpy as np
import pandas as pd
from tkinter import messagebox as msg
from datetime import datetime
from utils import *


def run_comparison(lhs_filepath, rhs_filepath):
    # Filepath can't be empty
    if lhs_filepath == "":
        msg.showwarning("Empty filepath", "Path to the first file is empty. Please fill in the filepath.")
        return

    if rhs_filepath == "":
        msg.showwarning("Empty filepath", "Path to the second file is empty. Please fill in the filepath.")
        return

    # todo What if files don't exist

    output = compare(lhs_filepath, rhs_filepath)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "quasimodo_" + timestamp + ".xlsx"
    output.to_excel(filename, index = False)


def compare(lhs_filepath, rhs_filepath):
    lhs = pd.read_csv(lhs_filepath, sep=";")
    rhs = pd.read_csv(rhs_filepath, sep=";")

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
