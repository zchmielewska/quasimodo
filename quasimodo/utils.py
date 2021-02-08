import tkinter as tk
import pandas as pd
from pathlib import Path


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
    if pd.isna(x) and pd.isna(y):
        return True
    elif (not pd.isna(x) and pd.isna(y)) or (pd.isna(x) and not pd.isna(y)):
        return False
    else:
        return x == y


def compare_char_num(x, y):
    if pd.isna(x) and pd.isna(y):
        return True
    elif (not pd.isna(x) and pd.isna(y)) or (pd.isna(x) and not pd.isna(y)):
        return False
    else:
        return x == str(y)


def compare_num_char(x, y):
    if pd.isna(x) and pd.isna(y):
        return True
    elif (not pd.isna(x) and pd.isna(y)) or (pd.isna(x) and not pd.isna(y)):
        return False
    else:
        return str(x) == y


def compare_num_num(x, y):
    if pd.isna(x) and pd.isna(y):
        return True
    elif (not pd.isna(x) and pd.isna(y)) or (pd.isna(x) and not pd.isna(y)):
        return False
    else:
        return x - y


def add_log(st, text):
    st.configure(state='normal')
    st.insert(tk.END, str(text) + "\n")
    st.see(tk.END)
    st.configure(state='disabled')


def sanitize_output(settings):
    # Output folder can't have space(s) at the end
    if settings['output'] != "":
        while settings['output'][-1] == " ":
            settings['output'] = settings['output'][:-1]
    output_folder = Path(settings['output'])
    return output_folder
