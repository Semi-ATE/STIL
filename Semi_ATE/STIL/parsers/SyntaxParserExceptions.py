# -*- coding: utf-8 -*-

#    Work in process ...


error_map = {
    "base__KEYWORD_ANN": "Ann",
    "b_stil__KEYWORD_STIL": "STIL",
    "b_stil__STIL_VERSION": "version of the STIL = 1.0",
    "b_stil__STIL_EXTENSION_NAME": "DCLevels or Design",
    "b_stil__STIL_EXTENSION_YEAR": "2002 or 2005",
    "b_header__KEYWORD_HEADER": "Header",
    "b_header__KEYWORD_TITLE": "Title",
    "b_header__KEYWORD_SOURCE": "Source",
    "b_header__KEYWORD_DATE": "Date",
    "b_header__KEYWORD_HISTORY": "History",
    "b_header__HEADER_DATE_STRING": "Data/Time information in double quoted string",
    "b_header__TITLE_STRING":  "Title information in double quoted string",
    "b_header__SOURCE_STRING": "Source information in double quoted string",
    "b_signals__SIGNAL_TYPE": "signal type : In, Out, InOut, Pseudo or Supply",
    "b_timing__WFT_NAME": "Name of the WaveformTable",
    "b_pattern_burst__PATTERN_BURST_BLOCK_NAME" : "Name of the PatternBurst block",
    "b_pattern_exec__PATTERN_EXEC_BLOCK_NAME" : "Name of the PatternExec block",
    "b_macrodefs__MACRO_NAME" : "Name of the MacroDefs block",
    "b_pattern__pattern_statements__USER_KEYWORD_VALUE" : "UserKeyword value",
    "b_procedures__pattern_statements__USER_KEYWORD_VALUE" : "UserKeyword value",
    "b_macrodefs__pattern_statements__USER_KEYWORD_VALUE" : "UserKeyword value",
    "b_pattern__pattern_statements__UK_BLOCK_VALUE" : "value in the UserKeyword block",
    "b_procedures__pattern_statements__UK_BLOCK_VALUE" : "value in the UserKeyword block",
    "b_macrodefs__pattern_statements__UK_BLOCK_VALUE" : "value in the UserKeyword block",
    "ESCAPED_STRING" : "String in double quotes"    
}


class SyntaxParserExceptions:
    """
    Class for transforming automatically generated
    Lark syntax errors in human readable text
    Work in process ...
    """

    def __init__(self, debug=False):
        self.debug = debug

    def transform(self, lark_error):

        if self.debug:
            print(f"Catched syntax error(s) from lark parser:\n{lark_error}")

        if len(lark_error) == 1:
            return_value = "Expected : "
        elif len(lark_error) > 1:
            return_value = "Expected one of : "
        else:
            print(lark_error)
#            raise Exception()
            return "Lark parser does not provide expected value, but should!"

        is_open_block_used = False
        for err in lark_error:
            if self.debug:
                print(f"Error {err}")
            v = error_map.get(err)
            # If the error can not be found in the error map:
            if v == None:
                if err.endswith("USER_DEFINED_NAME"):
                    return_value += "User defined name"
                elif err.endswith("TIME_EXPR"):
                    return_value += "Time expression in format 'NUMBER UNIT' without whitespace between them or 'NUMBER MATH_OPERATOR NUMBER UNIT' or 'NUMBER' or 'VARIABLE' \n\t\t   Where:\n\t\t   - Mandatory single quotes 'xxx' for the value\n\t\t   - NUMBER can be integer, real or exponential number\n\t\t   - UNIT SI Time/Frequency unit with engineering prefixes (ns, us, ms, s, Hz, MHz ...)\n\t\t   - VARIABLE defined in the Spec block\n\t\t   - MATH_OPERATOR can be *,/,+.- \n\t\t   Examples: '5ns' '1.234ms' '10E-3s' '1MHz' '2/1MHz+PLL_Freq' "
                elif err.endswith("SEMICOLON"):
                    return_value += ";"
                elif err.find("QUOTE") > -1:
                    return_value += "'"
                elif err.find("EQUAL") > -1:
                    return_value += "="
                elif err.find("COLON") > -1:
                    return_value += ":"
                elif err.find("SLASH") > -1:
                    return_value += "/"
                elif err.find("TIMEUNIT") > -1:
                    return_value += "TimeUnit"
                elif err.endswith("_ADD"):
                    return_value += "+"
                elif err.endswith("_SUB"):
                    return_value += "-"
                elif err.find("__OPEN_") > -1:
                    if is_open_block_used == False:
                        return_value += "{"
                        is_open_block_used = True
                    else:
                        continue
                elif err.find("__CLOSE_") > -1:
                    return_value += "}"
                elif err.find("__KEYWORD_ANN") > -1:
                    return_value += "Ann"
                elif err.endswith("__INT"):
                    return_value += "integer value"
                elif err.endswith("_DOMAIN_NAME"):
                    return_value += "domain name"
                elif err.endswith("_END_STMT"):
                    return_value += ";"
                elif err.endswith("SIGREF_NAME"):
                    return_value += "signal name"
                elif err.endswith("KEYWORD_BLOCK_SIGNAL_GROUPS"):
                    return_value += "SignalGroups"
                elif err.endswith("SIGNAL_GROUPS_DOMAIN"):
                    return_value += "Name of the SignalGroups domain"                  
                elif err.endswith("KEYWORD_BASE"):
                    return_value += "Base"
                elif err.endswith("KEYWORD_DATABITCOUNT"):
                    return_value += "DataBitCount"
                elif err.endswith("KEYWORD_SCANOUT"):
                    return_value += "ScanOut"
                elif err.endswith("KEYWORD_SCANIN"):
                    return_value += "ScanIn"
                elif err.endswith("KEYWORD_TERMINATION"):
                    return_value += "Termination"
                elif err.endswith("KEYWORD_DEFAULT_STATE"):
                    return_value += "DefaultState"
                elif err.endswith("KEYWORD_ALIGNMENT"):
                    return_value += "Alignment"
                elif err.endswith("KEYWORD_START"):
                    return_value += "Start"
                elif err.endswith("KEYWORD_STOP"):
                    return_value += "Stop"
                elif err.endswith("KEYWORD_PROCEDURES"):
                    return_value += "Procedures"
                elif err.endswith("PROCEDURES_DOMAIN"):
                    return_value += "Name of the Procedures domain"
                elif err.endswith("KEYWORD_MACRO_DEFS"):
                    return_value += "MacroDefs"
                elif err.endswith("MACROS_DOMAIN"):
                    return_value += "Name of the MacroDefs domain"
                elif err.endswith("KEYWORD_SIGNAL_GROUPS"):
                    return_value += "SignalGroups"
                elif err.endswith("KEYWORD_IFNEEDED"):
                    return_value += "IfNeed"
                elif err.endswith("KEYWORD_BLOCK_SCAN_STRUCTURES"):
                    return_value += "ScanStructures"
                elif err.endswith("KEYWORD_BLOCK_ANN"):
                    return_value += "Ann"
                elif err.endswith("KEYWORD_BLOCK_USER_KEYWORDS"):
                    return_value += "UserKeywords"
                elif err.endswith("KEYWORD_BLOCK_USER_FUNCTIONS"):
                    return_value += "UserFunctions"
                elif err.endswith("KEYWORD_BLOCK_PATTERN"):
                    return_value += "Pattern"
                elif err.endswith("KEYWORD_BLOCK_SELECTOR"):
                    return_value += "Selector"
                elif err.endswith("KEYWORD_BLOCK_PATERN_EXEC"):
                    return_value += "PatternExec"
                elif err.endswith("KEYWORD_BLOCK_SPEC"):
                    return_value += "Spec"
                elif err.endswith("KEYWORD_BLOCK_SIGNALS"):
                    return_value += "Signals"
                elif err.endswith("KEYWORD_BLOCK_HEADER"):
                    return_value += "Header"
                elif err.endswith("KEYWORD_BLOCK_PROCEDURES"):
                    return_value += "Procedures"
                elif err.endswith("KEYWORD_BLOCK_TIMING"):
                    return_value += "Timing"
                elif err.endswith("KEYWORD_BLOCK_PATTERN_BURST"):
                    return_value += "PatternBurst"
                elif err.endswith("KEYWORD_BLOCK_MACRO_DEFS"):
                    return_value += "MacroDefs"
                elif err.endswith("KEYWORD_PAT_LIST"):
                    return_value += "PatList"
                elif err.endswith("KEYWORD_CALL"):
                    return_value += "Call"
                elif err.endswith("KEYWORD_BREAKPOINT"):
                    return_value += "BreakPoint"
                elif err.endswith("KEYWORD_CONDITION"):
                    return_value += "Condition"
                elif err.endswith("KEYWORD_C"):
                    return_value += "C"
                elif err.endswith("USER_KEYWORD"):
                    return_value += "UserKeyword"
                elif err.endswith("KEYWORD_IDDQ_TEST_POINT"):
                    return_value += "IddqTestPoint"
                elif err.endswith("KEYWORD_MATCH_LOOP"):
                    return_value += "MatchLoop"
                elif err.endswith("KEYWORD_LOOP"):
                    return_value += "Loop"
                elif err.endswith("KEYWORD_W"):
                    return_value += "W"
                elif err.endswith("KEYWORD_WAVEFORM_TABLE"):
                    return_value += "WaveformTable"
                elif err.endswith("KEYWORD_MACRO"):
                    return_value += "Macro"
                elif err.endswith("LABEL"):
                    return_value += "label name"
                elif err.endswith("KEYWORD_GOTO"):
                    return_value += "Goto"
                elif err.endswith("KEYWORD_FIXED"):
                    return_value += "Fixed"
                elif err.endswith("KEYWORD_F"):
                    return_value += "F"
                elif err.endswith("KEYWORD_VECTOR"):
                    return_value += "Vector"
                elif err.endswith("KEYWORD_V"):
                    return_value += "V"
                elif err.endswith("KEYWORD_SHIFT"):
                    return_value += "Shift"
                elif err.endswith("KEYWORD_SCAN_CHAIN"):
                    return_value += "ScanChain"
                elif err.endswith("KEYWORD_SCAN_CHAIN"):
                    return_value += "ScanChain"
                elif err.endswith("KEYWORD_SCAN_STRUCTURES"):
                    return_value += "ScanStructures"
                elif err.endswith("ACTIVESCANCHAINS"):
                    return_value += "ActiveScanChains"
                elif err.endswith("SCAN_STRUCTURES_DOMAIN"):
                    return_value += "Name of the ScanStructures domain"
                elif err.endswith("TERMINATEHIGH"):
                    return_value += "TerminateHigh"
                elif err.endswith("TERMINATELOW"):
                    return_value += "TerminateLow"
                elif err.endswith("TERMINATEOFF"):
                    return_value += "TerminateOff"
                elif err.endswith("TERMINATEUNKNOWN"):
                    return_value += "TerminateUnknown"
                elif err.endswith("SIG_DEF_STATE_UP"):
                    return_value += "U or ForceUp"
                elif err.endswith("SIG_DEF_STATE_OFF"):
                    return_value += "Z or ForceOff"
                elif err.endswith("SIG_DEF_STATE_DOWN"):
                    return_value += "D or ForceDown"
                elif err.endswith("HEX"):
                    return_value += "Hex"
                elif err.endswith("DEC"):
                    return_value += "Dec"
                elif err.endswith("WFC_LIST"):
                    return_value += "List of WFC"
                elif err.endswith("KEYWORD_PERIOD"):
                    return_value += "Period"
                elif err.endswith("SIGREF_EXPR"):
                    return_value += "Signal"
                elif err.endswith("EVENT"):
                    return_value += "one or more (separated by '/') Waveform events :\n\t\t   D,U,Z,P for drive \n\t\t   L,H,X,T,V,l,h,x,t,v for compare"
                elif err.endswith("LABEL_NAME"):
                    return_value += "Name of label"
                elif err.endswith("VEC_DATA_STRING"):
                    return_value += "List of WFC"
                elif err.endswith("WAVEFORM_TABLE_NAME"):
                    return_value += "Name of the WaveformTable"
                elif err.endswith("CALL_PROC_NAME"):
                    return_value += "Name of the Procedure"
                elif err.endswith("CALL_MACRO_NAME"):
                    return_value += "Name of the Macro"
                elif err.endswith("MATCHLOOP_INF"):
                    return_value += "Infinite"
                elif err.endswith("SCANCHAIN_NAME"):
                    return_value += "Name of the ScanChain"
                elif err.endswith("PATTERN_NAME"):
                    return_value += "Name of the Pattern block"
                elif err.endswith("LOOP_COUNT"):
                    return_value += "Loop count value"
                else:
                    return_value += err
            else:
                return_value += v
            return_value += " or "

        return_value = return_value[:-4]

        return return_value
