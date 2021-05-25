#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from lark import Lark
from lark import Transformer
from lark.exceptions import UnexpectedToken
from lark.exceptions import UnexpectedCharacters
from lark.exceptions import VisitError

from . import STILBlockParser
from . import HeaderBlockParser
from . import SignalsBlockParser
from . import SyntaxParserExceptions
from . import utils

# ToDo : add all semantic parsers here
class STIL(Transformer, STILBlockParser, HeaderBlockParser, SignalsBlockParser):
    def __init__(self, debug=False):
        self.debug = debug

        STILBlockParser.__init__(self, debug)
        HeaderBlockParser.__init__(self, debug)
        SignalsBlockParser.__init__(self, debug)

class STILParser:

    def __init__(self, propagate_positions=True, debug=False):
        
        self.err_line = -1
        self.err_col = -1
        self.err_msg = ''

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
    
    def parse_syntax(self, stil, debug=False):
        '''
        

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

        '''
        if debug:
            print("\n===========================")
            print(  "Start of syntax parsing :\n")
            

        try:
            if len(stil) < 1024 and os.path.exists(stil):
                with open(stil) as data:
                    tree = self.parser.parse(data.read())
                    if debug == True:
                        print(tree.pretty())
            else:
                tree = self.parser.parse(stil)
                if debug == True:
                    print(tree.pretty())
                
            if debug:
                print("\nEnd of syntax parsing")
                print(  "===========================\n")

            return tree

        except UnexpectedToken as e:
            
            if debug:
                print(f'UnexpectedToken Exception:\n {e}')

            line = e.line
            self.err_line = line

            col  = e.column
            self.err_col = col
            
            if str(e).startswith("Unexpected token Token('$END'"):
                print("\nEnd of the file reached, but expected one of the tokens:")
                s = str(e).split("\n")
                i = 0
                for s1 in s:
                    i += 1
                    if i == 3:
                        print(s1)
                return

            line_with_error = utils.get_line(stil, e.line)
            
            self.err_msg = f'\nERROR:\tIn the line number {line}, column {col}:\n'
            self.err_msg += f'\t{line_with_error}\n'
            self.err_msg += utils.get_col_error_pos(col) + '\n'
            self.err_msg += f'\tUnexpected token : {e.token}\n'
            self.err_msg += f'\t{SyntaxParserExceptions(debug).transform(e.expected)}\n'

            print(self.err_msg)
            
        except UnexpectedCharacters as e:

            if debug:
                print(f'UnexpectedCharacters Exception:\n {e}')

            line = e.line
            self.err_line = line

            col  = e.column
            self.err_col = col
            
            line_with_error = utils.get_line(stil, line)

            self.err_msg = f'\nERROR:\tIn the line number {line}, column {col}:\n'
            self.err_msg += f'\t{line_with_error}\n'
            self.err_msg += utils.get_col_error_pos(col) + '\n'
            self.err_msg += f'\tUnexpected character : {e.char}\n'
            self.err_msg += f'\t{SyntaxParserExceptions(debug).transform(e.allowed)}\n'

            print(self.err_msg)

        return None

    def parse_semantic(self, tree, stil, debug=False):

        # if tree is None, syntax parsing is already failed
        if tree != None:
            print(  "\nStart of semantic parsing :\n")
            if debug:
                print("\n===========================")
                print(  "Start of semantic parsing :\n")
    
            t = STIL(debug)
            try:
               
                print(  "before t.transform(tree)")
                t.transform(tree)
                print(  " after t.transform(tree)")

#                if debug:
#                    print("\nEnd of semantic parsing")
#                    print(  "===========================\n")

            except VisitError as e:
           
                line = e.obj.line
                self.err_line = line
                col  = e.obj.column
                self.err_col = col

                line_with_error = utils.get_line(stil, line)
                self.err_msg = f'\nERROR:\tIn the line number {line}, column {col} [{line},{col}]:\n'
                self.err_msg += f'\t{line_with_error}\n'
                self.err_msg += utils.get_col_error_pos(e.obj.column) + '\n'
                self.err_msg += f'\t{e.orig_exc}\n'

                print(self.err_msg)
