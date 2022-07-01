#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re

from lark import Lark
from lark.exceptions import UnexpectedToken
from lark.exceptions import UnexpectedCharacters
from lark.exceptions import VisitError

from .STILLark import STILLark

from . import SyntaxParserExceptions
from . import STILSemanticException
from . import utils

class STILParser(STILLark):
    def __init__(self, 
                 stil_file, 
                 propagate_positions=True, 
                 expanding_procs = False, 
                 stil_lark_file = None,
                 extra_grammars = [],
                 debug=False):

        STILLark.__init__(self, stil_file, debug)

        self.err_line = -1
        self.err_col = -1
        self.err_msg = ""

        self.tree = None

        self.is_parsing_done = False
        # Depends on ATE pattern engine capabilities, procedures can be expanded or not.
        # This choice impacts calculation of the total VA
        self.expanding_procs = expanding_procs

        grammar_base_file = os.path.dirname(__file__)
        # Adding main lark grammar file
        if stil_lark_file == None:
            grammar_file = os.path.join(str(grammar_base_file), "grammars", "stil.lark")
        else:
            grammar_file = stil_lark_file
                
        grammars_file = os.path.join(str(grammar_base_file), "grammars")
        # Adding all lark grammars files under grammars folder
        ip = list()
        ip.append(grammars_file)

        # Adding additional grammar files
        if extra_grammars:
            ip.extend(extra_grammars)
            
        with open(grammar_file) as grammar:
            self.parser = Lark(
                grammar.read(),
                start="start",
                parser="lalr",
                propagate_positions=propagate_positions,
                import_paths=ip,
            )


        self.is_compressed = utils.check_for_compression(stil_file)
    
    def preprocess_include(self, file):
        
        out_file = file + ".wo_include"

        f = open(out_file, 'wb')
        if f == None:
            print(f"ERROR: Can not create output file {out_file}.\n")
            return "ERROR"
        else:
            f.close()
            os.remove(out_file)
        
        with open(file) as data, open(out_file, "w") as out:
            inc_cnt = 0
            line_cnt = 0
            line = data.readline()
            out.write(line)
            err_inc_msg = "Not correct 'Include' syntax at line "
            err_file_not_found_msg = "Can not find include flie "
            while line:
                line = data.readline()
                line_cnt += 1
                strip_line = line.strip()
                if strip_line.startswith("Include"):
                    l = re.split(r'\s+', strip_line)
                    if len(l) > 1:
                        l = l[1].split('"')
                        inc_cnt += 1
                        if len(l) > 1:
                            inc_file = l[1]
                            folder = os.path.dirname(file)
                            f = os.path.join(folder, inc_file)
                            if os.path.exists(f):
                                with open(f) as inc_data:
                                    inc_line = inc_data.readline()
                                    sl = inc_line.strip()
                                    if sl.startswith("STIL") == False:
                                        out.write(inc_line)
                                    while inc_line:
                                        inc_line = inc_data.readline()
                                        sl = inc_line.strip()
                                        if sl.startswith("STIL") == False:
                                            out.write(inc_line)
                            else:
                                print(f"ERROR: {err_file_not_found_msg} '{inc_file}' at line {line_cnt}")
                                return "ERROR"
                        else:
                            print(f"ERROR: {err_inc_msg} {line_cnt}")
                            return "ERROR"
                    else:
                            print(f"ERROR: {err_inc_msg} {line_cnt}")
                            return "ERROR"
                else:
                    out.write(line)
        
        if inc_cnt > 0:
            return out_file
        else:
            os.remove(out_file)
            return None

    def parse_syntax(self, debug=False, preprocess_include = True):
        """
        Parameters
        ----------
        stil : str
            stil argument can be either location of STIL file or
            the STIL file content as string.
        debug : TYPE, optional
            Debug flag. The default is False.

        Returns
        -------
        tree : Lark tree object

        """
        if debug:
            print("\n===========================")
            print("Start of syntax parsing :\n")

        try:
            
            if os.path.exists(self.stil_file):
                if self.is_compressed:
                    data = utils.get_uncompressed_data(self.stil_file)
                    self.tree = self.parser.parse(data)
                    if debug == True:
                        print(self.tree.pretty())
                else:
                    
                    file = self.stil_file
                    
                    if preprocess_include:
                        # Initial support for 'Include'.
                        # Does not support syntax error highlighting yet.
                        full_file = self.preprocess_include(self.stil_file)
                        
                        if full_file != None:
                            if full_file == "ERROR":
                                return
                            else:
                                file = full_file
                        else:
                            file = self.stil_file

                    with open(file) as data:
                        self.tree = self.parser.parse(data.read())
                        if debug == True:
                            print(self.tree.pretty())
            else:
                msg = "ERROR : input STIL file does not exists '{self.stil_file}' b"
                raise Exception(msg)

            if debug:
                print("\nEnd of syntax parsing")
                print("===========================\n")

            return self.tree

        except UnexpectedToken as e:

#            raise Exception()
#            print(f"UnexpectedToken Exception:\n {e.token.type}")

            if debug:
                print(f"UnexpectedToken Exception:\n {e}")

            line = e.line
            self.err_line = line

            col = e.column
            self.err_col = col
            
            line_with_error = utils.get_line(self.stil_file, e.line)

            self.err_msg = f"\nERROR:\tIn the line number {line}, column {col}:\n"
            self.err_msg += f"\t{line_with_error}\n"
            self.err_msg += utils.get_col_error_pos(col) + "\n"

            if str(e).startswith("Unexpected token Token('$END'"):
                s = str(e).split("\n")
                i = 0
                for s1 in s:
                    i += 1
                    if i == 3:
                        strim = s1.strip()
                        if strim == "*":
                            lines = line_with_error.strip()
                            exp_token = "';' or '}'"
                            if (lines.endswith(";")):
                                exp_token = "'}'"
                            self.err_msg += f"\tEnd of the file reached, but expected {exp_token}"
                        else:
                            if strim.startswith("* "):
                                self.err_msg += "\tUnexpected end of the file or block is not closed (including nested ones) \n"
#                                expected = strim[2:]
#                                self.err_msg += f"\t{SyntaxParserExceptions(debug).transform([expected])}\n"
                            else:
                                self.err_msg += s1 + "\n"
            else:
                self.err_msg += f"\tUnexpected token : {e.token}\n"
                token = e.token.type
                if token == "b_pattern_burst__CLOSE_PATT_OR_BURST":
                    self.err_msg += "\tDid you miss to write the mandatory PatList block ? \n"
                else:
                    self.err_msg += f"\t{SyntaxParserExceptions(debug).transform(e.expected)}\n"

            print(self.err_msg)

        except UnexpectedCharacters as e:

            if debug:
                print(f"UnexpectedCharacters Exception:\n {e}")

            line = e.line
            self.err_line = line

            col = e.column
            self.err_col = col

            line_with_error = utils.get_line(self.stil_file, line)

            self.err_msg = f"\nERROR:\tIn the line number {line}, column {col}:\n"
            self.err_msg += f"\t{line_with_error}\n"
            self.err_msg += utils.get_col_error_pos(col) + "\n"
            self.err_msg += f"\tUnexpected character : {e.char}\n"
            self.err_msg += f"\t{SyntaxParserExceptions(debug).transform(e.allowed)}\n"

            print(self.err_msg)

        return None

    def parse_semantic(
        self,
        # stil,
        debug=False,
    ):

        # if tree is None, syntax parsing is already failed
        if self.tree != None:
            if debug:
                print("\n===========================")
                print("Start of semantic analisys :\n")
            try:
                self.transform(self.tree)
                self.eof()
                self.is_parsing_done = True

                if debug:
                    print("\nEnd of semantic analisys")
                    print("===========================\n")
                                    
            except VisitError as e:

                #raise Exception()
                #if debug:
                #    raise Exception()
                                
                if isinstance(e.orig_exc, STILSemanticException):
                    line = e.orig_exc.line
                    col = e.orig_exc.col
                    err_msg = e.orig_exc.msg
                else:

                    err_msg = e.orig_exc
                    try:
                        #Lark version < 1.0.0 
                        line = e.obj.line
                        col = e.obj.column
                    except:
                        #Lark version >= 1.0.0 
                        line = e.obj.meta.line
                        col = e.obj.meta.column
                
                self.err_line = line
                self.err_col = col

                line_with_error = utils.get_line(self.stil_file, line)
                self.err_msg = f"\nERROR:\tIn the line number {line}, column {col} [{line},{col}]:\n"
                self.err_msg += f"\t{line_with_error}\n"
                self.err_msg += utils.get_col_error_pos(col) + "\n"
                self.err_msg += f"\t{err_msg}\n"

                print(self.err_msg)

        else:
            msg = "ERROR : syntax parsing must be performed before semantic analisys b"
            raise Exception(msg)
