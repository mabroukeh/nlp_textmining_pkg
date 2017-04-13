"""
Common utility library

Author: Nizar Mabroukeh
"""

import bz2
import cPickle
import functools
import os
import sys
import warnings
from datetime import datetime
from itertools import chain


import pandas as pd

def get_user_confirmation():
    """
    Interactive dialogue to gets user confirmation
    Returns:
        bool
    """
    ready_to_go = ('yes', 'y')
    valid_ans = ready_to_go + ('no', 'n')
    ans = raw_input('Do you wish to proceed? (y/n): ')
    while True:
        ans = ans.lower()
        if ans in ready_to_go:
            print
            return True
        elif ans in valid_ans:
            print
            return False
        ans = raw_input('Please enter y|yes or n|no: ')



def save_pickle(object_to_pickle, filename):
    """
    Save an object to a compressed disk file.
    Works well with huge objects.
    Args:
        object_to_pickle (object):
        filename (str):
    """
    try:
        file_handle = bz2.BZ2File(filename, 'wb')
        cPickle.dump(object_to_pickle, file_handle)
        file_handle.close()
    except Exception as err:
        raise Exception("Could not store pickle.\n{}".format(err))


def load_pickle(filename):
    """
    Loads a compressed object from disk
    Args:
        filename (str):

    Returns:
        object
    """
    try:
        file_handle = bz2.BZ2File(filename, 'rb')
        unpickled_object = cPickle.load(file_handle)
        file_handle.close()
    except Exception as err:
        raise IOError("Could not load pickle.\n{}".format(err))
    return unpickled_object


def read_sql_dataframe(log, db_conn, input_sql, show_sql=False, *args):
    """
    run input_sql on database and output a DataFrame of the results
    Args:
        log:
        db_conn: database connection
        input_sql (str): sql (optionally including {} or {#} for .format() with *args)
        show_sql (bool):
        *args (list[str]): arguments to use to format input_sql; currently unused

    Returns:
        pd.DataFrame
    """
    sql_command = input_sql.format(*args)
    if show_sql:
        log.info(sql_command)
        dataframe = pd.read_sql(sql_command, db_conn)
    return dataframe


def deprecated(func):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    ref: https://wiki.python.org/moin/PythonDecoratorLibrary#Generating_Deprecation_Warnings
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1
        )
        return func(*args, **kwargs)

    return new_func


def c_lst(list_in):
    """
    Takes a list of anything and returns a string; a comma-and-space-separated version of the string representation of each element
    Args:
        list_in (list): can be list[int], list[str]

    Returns:
        str: comma-and-space-separated string of each element in list_in
    """
    return ", ".join(map(str, list_in))


def valid_date(string_date):
    """
    converts string to datetime
    Args:
        string_date (str): a date in string format (YYYY-MM-DD)

    Returns:
        datetime: the date corresponding to the string input
    """
    try:
        return datetime.strptime(string_date, "%Y-%m-%d").date()
    except ValueError:
        raise TypeError("Not a valid date: '{0}'.".format(string_date))


def transform_float_to_exact_int(float_val):
    """
    Converts a floating point value of 4 decimal point precision into an integer with exact value. For example 0.0031 becomes 31

    Args:
        float_val (float): any floating point number (preferred to be in 4 decimal points precision)

    Returns:
        int
    """
    return int(float_val * 10000)


def is_sorted(x, key=lambda x: x):
    """
    Checks if a list is sorted in ascending order
    Args:
        x (list):
        key:

    Returns:
        bool
    """
    return all([key(x[i]) <= key(x[i + 1]) for i in xrange(len(x) - 1)])

def flatmap(l):
    return list(chain.from_iterable(l))

