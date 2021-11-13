#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from lark import Lark
from lark.exceptions import UnexpectedToken
from lark.exceptions import UnexpectedCharacters
from lark.exceptions import VisitError

from .STILLark import STILLark

from . import SyntaxParserExceptions
from . import STILSemanticException
from . import utils

class STILParser(STILLark):
    def __init__(self, stil_file, propagate_positions=True, expanding_procs = False, debug=False):

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
        grammar_file = os.path.join(str(grammar_base_file), "grammars", "stil.lark")
        grammars_file = os.path.join(str(grammar_base_file), "grammars")
        # Adding all lark grammars files under grammars folder
        ip = list()
        ip.append(grammars_file)
        with open(grammar_file) as grammar:
            self.parser = Lark(
                grammar.read(),
                start="start",
                parser="lalr",
                propagate_positions=propagate_positions,
                import_paths=ip,
            )
        
        self.is_compressed = utils.check_for_compression(stil_file)
    
    def parse_syntax(self, debug=False):
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
                    with open(self.stil_file) as data:
                        self.tree = self.parser.parse(data.read())
                        if debug == True:
                            print(self.tree.pretty())

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
                print("Start of semantic parsing :\n")
            try:
                self.transform(self.tree)
                self.eof()
                self.is_parsing_done = True

                if debug:
                    print("\nEnd of semantic parsing")
                    print("===========================\n")
                                    
            except VisitError as e:

                #raise Exception()
                #if debug:
                #    raise Exception()
                
                line = e.obj.line
                self.err_line = line
                col = e.obj.column
                self.err_col = col
                err_msg = e.orig_exc
                
                if isinstance(e.orig_exc, STILSemanticException):
                    line = e.orig_exc.line
                    self.err_line = line
                    col = e.orig_exc.col
                    self.err_col = col
                    err_msg = e.orig_exc.msg

                line_with_error = utils.get_line(self.stil_file, line)
                self.err_msg = f"\nERROR:\tIn the line number {line}, column {col} [{line},{col}]:\n"
                self.err_msg += f"\t{line_with_error}\n"
                self.err_msg += utils.get_col_error_pos(col) + "\n"
                self.err_msg += f"\t{err_msg}\n"

                print(self.err_msg)

        else:
            print("ERROR : syntax parse must be performed before semantic parsing b")
