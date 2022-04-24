# -*- coding: utf-8 -*-
import os
import gzip

def check_for_compression(file):

    if os.path.exists(file):
        #Check for gz compression
        with open(file, 'rb') as zf:
            if zf.read(2) == b'\x1f\x8b':
                return True
        #Check for zip compression
        with open(file, 'rb') as zf:
            if zf.read(4) == b'\x50\x4B\x03\x04':
                return True
    return False

def get_uncompressed_data(file):

    if os.path.exists(file):
        is_gz = False
        is_zip = False
        
        #Check for gz compression
        with open(file, 'rb') as zf:
            if zf.read(2) == b'\x1f\x8b':
                is_gz = True
                
        if is_gz == False:
            #Check for zip compression
            with open(file, 'rb') as zf:
                if zf.read(4) == b'\x50\x4B\x03\x04':
                    is_zip = True
    
        if is_gz:
            with gzip.open(file, 'rt') as zf:
                return zf.read()
        elif is_zip:
            #Not supported yet
            return None
    return None

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
    is_compressed = check_for_compression(file)
    if os.path.exists(file):

        line_count = 1
        
        if is_compressed:
            data = get_uncompressed_data(file)
            for line in data:
                if line_count == line_number:
                    return line[:-1]
                    break
                line_count += 1
        else:
            with open(file) as f:
                line = f.readline()
                while line:
                    if line_count == line_number:
                        return line[:-1]
                        break
                    line = f.readline()
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
