import numpy as np 
import pandas as pd 

## IsCharNumber ##
# Checks if my_char could be a number


def is_char_number(my_char):
    assert(my_char.dtype == 'object'), 'my_char must be an object dtype'
    # trim trailing and leading whitespace
    my_char = my_char.str.strip()
    # define what is not a number
    not_number = my_char.str.contains('[^-01234567889\\.]', regex=True, na=True) 
    is_number = ~not_number
    return is_number


def not_char_number(my_char):
    assert(my_char.dtype == 'object'), 'my_char must be an object dtype'
    return ~is_char_number(my_char)


def failed_numeric_conversions(my_df, colname):
    failed_rows = np.where(not_char_number(my_df[colname]))[0]
    failed_vals = my_df[colname].iloc[failed_rows]
    failed_vars = np.repeat(colname, failed_rows.size)

    failed_meta = pd.DataFrame({
        'failed_vars' : failed_vars,
        'failed_rows' : failed_rows,
        'failed_vals' : failed_vals
    })

    failed_meta.index = np.arange(1, failed_rows.size + 1)

    return failed_meta
