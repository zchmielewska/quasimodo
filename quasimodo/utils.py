import os
import tkinter as tk
import pandas as pd
from tkinter import messagebox as msg


def compare_cols(left_col, right_col):
    if pd.api.types.is_string_dtype(left_col) and pd.api.types.is_string_dtype(right_col):
        result = map(compare_char_char, left_col, right_col)
    elif pd.api.types.is_string_dtype(left_col) and pd.api.types.is_numeric_dtype(right_col):
        result = map(compare_char_num, left_col, right_col)
    elif pd.api.types.is_numeric_dtype(left_col) and pd.api.types.is_string_dtype(right_col):
        result = map(compare_num_char, left_col, right_col)
    elif pd.api.types.is_numeric_dtype(left_col) and pd.api.types.is_numeric_dtype(right_col):
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
