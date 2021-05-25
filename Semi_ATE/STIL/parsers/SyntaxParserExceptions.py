# -*- coding: utf-8 -*-

# 

error_map = {
    'SEMICOLON'                     :';',
    'base__KEYWORD_ANN'             :'Ann',

    'b_stil__KEYWORD_STIL'          :'STIL',
    'b_stil__STIL_VERSION'          :'version of the STIL = 1.0',
    'b_stil__OPEN_STIL_EXTENSION'   :'{',
    'b_stil__CLOSE_STIL_EXTENSION'  :'}',
    'b_stil__STIL_EXTENSION_NAME'   :'DCLevels or Design',
    'b_stil__STIL_EXTENSION_YEAR'   :'2002 or 2005',


    'b_header__KEYWORD_HEADER'      :'Header',
    'b_header__OPEN_HEADER_BLOCK'   :'{',
    'b_header__CLOSE_HEADER_BLOCK'  :'}',
    'b_header__KEYWORD_TITLE'       :'Title',
    'b_header__KEYWORD_SOURCE'      :'Source',
    'b_header__KEYWORD_DATE'        :'Date',
    'b_header__KEYWORD_HISTORY'     :'History',
    'b_header__OPEN_BLOCK_HISTORY'  :'{',
    'b_header__base__KEYWORD_ANN'  :'Ann',    
    'b_header__CLOSE_BLOCK_HISTORY' :'}'
    }

class SyntaxParserExceptions:
    '''
    Class for transforming automatically generated 
    Lark syntax errors in human readable text
    '''
    def __init__(self, debug=False):
        self.debug = debug
            
    def transform(self, lark_error):
        
        if self.debug:
            print(f'Catched syntax error(s) from lark parser:\n{lark_error}')

        if len(lark_error) == 1:
            return_value = "Expected : "
        elif len(lark_error) > 1:
            return_value = "Expected one of : "
        else:
            print(lark_error)
            return 'Lark parser does not provide expected value, but should!'

        for err in lark_error:
            v = error_map.get(err)
            if v == None:
                return_value += err
            else:
                return_value += v
                if len(lark_error) > 1:
                    return_value += " or "

        if len(lark_error) > 1:
            return_value = return_value[:-4]

        return return_value