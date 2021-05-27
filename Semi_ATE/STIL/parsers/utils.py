# -*- coding: utf-8 -*-
import os


def get_line(file, line_number):
    """
    Return line content for the given line number

    Parameters
    ----------
    file : str
        The input file location or file content.
    line : int
        The line number.

    Returns
    -------
    line
        The line content for the given line number.

    """
    line_count = 0
    if len(file) < 255 and os.path.exists(file):
        with open(file) as f:
            line_count = 1
            line = f.readline()
            while line:
                if line_count == line_number:
                    return line[:-1]
                    break
                line = f.readline()
                line_count += 1
    else:
        text = str(file).split("\n")
        for line in text:
            if line_count == line_number:
                return line[:-1]
                break
            line_count += 1

    return None


def get_col_error_pos(col):
    """
    Return string which points the error in a line

    Parameters
    ----------
    col : int
        Column number where the error is located.

    Returns
    -------
    line : str
        Line with arrow up point to the error location.

    """
    line = "\t"
    i = 1
    while i < col:
        line += " "
        i += 1
    line += "↑"
    return line
