from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

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


