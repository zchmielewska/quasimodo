import os
import tkinter as tk
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from tkinter import messagebox as msg


def ensure_existence(lhs_path, rhs_path, output_folder, log_scr):
    paths_check = 0

    if not lhs_path.exists():
        msg.showwarning("Path does not exist", "The left path does not exist. Please try again.")
        paths_check = paths_check + 1

    if not rhs_path.exists():
        msg.showwarning("Path does not exist", "The right path does not exist. Please try again.")
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


def compare_cols(left_col, right_col):
    if is_string_dtype(left_col) and is_string_dtype(right_col):
        result = map(compare_char_char, left_col, right_col)
    elif is_string_dtype(left_col) and is_numeric_dtype(right_col):
        result = map(compare_char_num, left_col, right_col)
    elif is_numeric_dtype(left_col) and is_string_dtype(right_col):
        result = map(compare_num_char, left_col, right_col)
    elif is_numeric_dtype(left_col) and is_numeric_dtype(right_col):
        result = map(compare_num_num, left_col, right_col)
    return result


def compare_char_char(x, y):
    return x == y


def compare_char_num(x, y):
    return x == str(y)


def compare_num_char(x, y):
    return str(x) == y


def compare_num_num(x, y):
    return x - y
