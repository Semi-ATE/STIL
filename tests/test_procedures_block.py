# -*- coding: utf-8 -*-

import os
import sys

try:
    from Semi_ATE.STIL.parsers.STILParser import STILParser
except:
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, cwd)
    from Semi_ATE.STIL.parsers.STILParser import STILParser


def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", "procedures_block", file_name)

def test_syn_ok_procedures_block_1():
    stil_file = get_stil_file("syn_ok_procedures_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_syn_err_procedures_block_1():
    stil_file = get_stil_file("syn_err_procedures_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 44
    assert parser.err_col == 11

def test_syn_err_procedures_block_2():
    stil_file = get_stil_file("syn_err_procedures_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 44
    assert parser.err_col == 18

def test_syn_err_procedures_block_3():
    stil_file = get_stil_file("syn_err_procedures_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 45
    assert parser.err_col == 9

def test_syn_err_procedures_block_4():
    stil_file = get_stil_file("syn_err_procedures_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 47
    assert parser.err_col == 10

def test_syn_err_procedures_block_5():
    stil_file = get_stil_file("syn_err_procedures_block_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 47
    assert parser.err_col == 10

def test_syn_err_label_1():
    stil_file = get_stil_file("syn_err_label_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 17

def test_syn_err_label_2():
    stil_file = get_stil_file("syn_err_label_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 17

def test_syn_err_label_3():
    stil_file = get_stil_file("syn_err_label_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 32

def test_syn_err_vector_1():
    stil_file = get_stil_file("syn_err_vector_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_vector_2():
    stil_file = get_stil_file("syn_err_vector_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 23

def test_syn_err_vector_3():
    stil_file = get_stil_file("syn_err_vector_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 26

def test_syn_err_vector_4():
    stil_file = get_stil_file("syn_err_vector_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_vector_5():
    stil_file = get_stil_file("syn_err_vector_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 32

def test_syn_err_vector_6():
    stil_file = get_stil_file("syn_err_vector_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_vector_7():
    stil_file = get_stil_file("syn_err_vector_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 34

def test_syn_err_waveformtable_1():
    stil_file = get_stil_file("syn_err_waveformtable_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_waveformtable_2():
    stil_file = get_stil_file("syn_err_waveformtable_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 12

def test_syn_err_waveformtable_3():
    stil_file = get_stil_file("syn_err_waveformtable_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 12

def test_syn_err_waveformtable_4():
    stil_file = get_stil_file("syn_err_waveformtable_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_condition_1():
    stil_file = get_stil_file("syn_err_condition_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_condition_2():
    stil_file = get_stil_file("syn_err_condition_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 26

def test_syn_err_condition_3():
    stil_file = get_stil_file("syn_err_condition_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 29

def test_syn_err_condition_4():
    stil_file = get_stil_file("syn_err_condition_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_condition_5():
    stil_file = get_stil_file("syn_err_condition_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 35

def test_syn_err_condition_6():
    stil_file = get_stil_file("syn_err_condition_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_condition_7():
    stil_file = get_stil_file("syn_err_condition_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 37

def test_syn_err_fixed_1():
    stil_file = get_stil_file("syn_err_fixed_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_fixed_2():
    stil_file = get_stil_file("syn_err_fixed_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 22

def test_syn_err_fixed_3():
    stil_file = get_stil_file("syn_err_fixed_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 25

def test_syn_err_fixed_4():
    stil_file = get_stil_file("syn_err_fixed_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_fixed_5():
    stil_file = get_stil_file("syn_err_fixed_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 31

def test_syn_err_fixed_6():
    stil_file = get_stil_file("syn_err_fixed_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_fixed_7():
    stil_file = get_stil_file("syn_err_fixed_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 33

def test_syn_err_call_1():
    stil_file = get_stil_file("syn_err_call_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_call_2():
    stil_file = get_stil_file("syn_err_call_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_call_3():
    stil_file = get_stil_file("syn_err_call_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_call_4():
    stil_file = get_stil_file("syn_err_call_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_call_5():
    stil_file = get_stil_file("syn_err_call_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_call_6():
    stil_file = get_stil_file("syn_err_call_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 21

def test_syn_err_call_7():
    stil_file = get_stil_file("syn_err_call_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_call_8():
    stil_file = get_stil_file("syn_err_call_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_call_9():
    stil_file = get_stil_file("syn_err_call_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_call_10():
    stil_file = get_stil_file("syn_err_call_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_call_11():
    stil_file = get_stil_file("syn_err_call_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 33

def test_syn_err_call_12():
    stil_file = get_stil_file("syn_err_call_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 36

def test_syn_err_macro_1():
    stil_file = get_stil_file("syn_err_macro_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_macro_2():
    stil_file = get_stil_file("syn_err_macro_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15

def test_syn_err_macro_3():
    stil_file = get_stil_file("syn_err_macro_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15

def test_syn_err_macro_4():
    stil_file = get_stil_file("syn_err_macro_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_macro_5():
    stil_file = get_stil_file("syn_err_macro_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_macro_6():
    stil_file = get_stil_file("syn_err_macro_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 24

def test_syn_err_macro_7():
    stil_file = get_stil_file("syn_err_macro_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_macro_8():
    stil_file = get_stil_file("syn_err_macro_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_macro_9():
    stil_file = get_stil_file("syn_err_macro_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_macro_10():
    stil_file = get_stil_file("syn_err_macro_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_macro_11():
    stil_file = get_stil_file("syn_err_macro_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 36

def test_syn_err_macro_12():
    stil_file = get_stil_file("syn_err_macro_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 39

def test_syn_err_loop_1():
    stil_file = get_stil_file("syn_err_loop_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_loop_2():
    stil_file = get_stil_file("syn_err_loop_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_loop_3():
    stil_file = get_stil_file("syn_err_loop_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_loop_4():
    stil_file = get_stil_file("syn_err_loop_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_syn_err_loop_6():
    stil_file = get_stil_file("syn_err_loop_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15
    
def test_syn_err_loop_7():
    stil_file = get_stil_file("syn_err_loop_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15

def test_syn_err_loop_8():
    stil_file = get_stil_file("syn_err_loop_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_loop_9():
    stil_file = get_stil_file("syn_err_loop_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_loop_10():
    stil_file = get_stil_file("syn_err_loop_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_loop_11():
    stil_file = get_stil_file("syn_err_loop_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_loop_12():
    stil_file = get_stil_file("syn_err_loop_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_loop_13():
    stil_file = get_stil_file("syn_err_loop_13.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_loop_14():
    stil_file = get_stil_file("syn_err_loop_14.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_loop_15():
    stil_file = get_stil_file("syn_err_loop_15.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1


def test_syn_err_matchloop_1():
    stil_file = get_stil_file("syn_err_matchloop_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_matchloop_2():
    stil_file = get_stil_file("syn_err_matchloop_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 19

def test_syn_err_matchloop_3():
    stil_file = get_stil_file("syn_err_matchloop_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 19

def test_syn_err_matchloop_4():
    stil_file = get_stil_file("syn_err_matchloop_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 19

def test_syn_err_matchloop_6():
    stil_file = get_stil_file("syn_err_matchloop_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 20
    
def test_syn_err_matchloop_7():
    stil_file = get_stil_file("syn_err_matchloop_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 20

def test_syn_err_matchloop_8():
    stil_file = get_stil_file("syn_err_matchloop_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_9():
    stil_file = get_stil_file("syn_err_matchloop_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_10():
    stil_file = get_stil_file("syn_err_matchloop_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_11():
    stil_file = get_stil_file("syn_err_matchloop_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_12():
    stil_file = get_stil_file("syn_err_matchloop_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_13():
    stil_file = get_stil_file("syn_err_matchloop_13.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_14():
    stil_file = get_stil_file("syn_err_matchloop_14.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_15():
    stil_file = get_stil_file("syn_err_matchloop_15.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_matchloop_16():
    stil_file = get_stil_file("syn_err_matchloop_16.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5
    
def test_syn_err_goto_1():
    stil_file = get_stil_file("syn_err_goto_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5
    
def test_syn_err_goto_2():
    stil_file = get_stil_file("syn_err_goto_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 14
    
def test_syn_err_goto_3():
    stil_file = get_stil_file("syn_err_goto_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_goto_4():
    stil_file = get_stil_file("syn_err_goto_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 17

def test_syn_err_goto_5():
    stil_file = get_stil_file("syn_err_goto_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_breakpoint_1():
    stil_file = get_stil_file("syn_err_breakpoint_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_breakpoint_2():
    stil_file = get_stil_file("syn_err_breakpoint_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_3():
    stil_file = get_stil_file("syn_err_breakpoint_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_4():
    stil_file = get_stil_file("syn_err_breakpoint_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_5():
    stil_file = get_stil_file("syn_err_breakpoint_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_6():
    stil_file = get_stil_file("syn_err_breakpoint_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_7():
    stil_file = get_stil_file("syn_err_breakpoint_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_8():
    stil_file = get_stil_file("syn_err_breakpoint_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_9():
    stil_file = get_stil_file("syn_err_breakpoint_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_10():
    stil_file = get_stil_file("syn_err_breakpoint_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_breakpoint_11():
    stil_file = get_stil_file("syn_err_breakpoint_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 20

def test_syn_err_breakpoint_12():
    stil_file = get_stil_file("syn_err_breakpoint_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 20

def test_syn_err_iddqtestpoint_1():
    stil_file = get_stil_file("syn_err_iddqtestpoint_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_iddqtestpoint_2():
    stil_file = get_stil_file("syn_err_iddqtestpoint_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 24

def test_syn_err_iddqtestpoint_3():
    stil_file = get_stil_file("syn_err_iddqtestpoint_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 24

def test_syn_err_stop_1():
    stil_file = get_stil_file("syn_err_stop_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_stop_2():
    stil_file = get_stil_file("syn_err_stop_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15

def test_syn_err_stop_3():
    stil_file = get_stil_file("syn_err_stop_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15

def test_syn_err_scanchain_1():
    stil_file = get_stil_file("syn_err_scanchain_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_scanchain_2():
    stil_file = get_stil_file("syn_err_scanchain_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 20

def test_syn_err_scanchain_3():
    stil_file = get_stil_file("syn_err_scanchain_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_scanchain_4():
    stil_file = get_stil_file("syn_err_scanchain_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 23

def test_syn_err_shift_1():
    stil_file = get_stil_file("syn_err_shift_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 52
    assert parser.err_col == 5

def test_syn_err_shift_2():
    stil_file = get_stil_file("syn_err_shift_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_3():
    stil_file = get_stil_file("syn_err_shift_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_4():
    stil_file = get_stil_file("syn_err_shift_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_5():
    stil_file = get_stil_file("syn_err_shift_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_6():
    stil_file = get_stil_file("syn_err_shift_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_7():
    stil_file = get_stil_file("syn_err_shift_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_8():
    stil_file = get_stil_file("syn_err_shift_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_9():
    stil_file = get_stil_file("syn_err_shift_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_10():
    stil_file = get_stil_file("syn_err_shift_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 53
    assert parser.err_col == 1

def test_syn_err_shift_11():
    stil_file = get_stil_file("syn_err_shift_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15

def test_syn_err_shift_12():
    stil_file = get_stil_file("syn_err_shift_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 51
    assert parser.err_col == 15
    
def test_sem_err_procedures_block_1():
    stil_file = get_stil_file("sem_err_procedures_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 53
    assert parser.err_col == 5

def test_sem_err_loop():
    stil_file = get_stil_file("sem_err_loop.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 51
    assert parser.err_col == 14

def test_sem_err_matchloop():
    stil_file = get_stil_file("sem_err_matchloop.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 51
    assert parser.err_col == 19

def test_sem_err_wft():
    stil_file = get_stil_file("sem_err_wft.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 51
    assert parser.err_col == 11
    
def test_sem_err_wft_1():
    stil_file = get_stil_file("sem_err_wft_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 51
    assert parser.err_col == 32

def test_sem_ok_wft():
    stil_file = get_stil_file("sem_ok_wft.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == -1
    assert parser.err_col == -1
    
def test_sem_err_wfc_1():
    stil_file = get_stil_file("sem_err_wfc_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 52
    assert parser.err_col == 24

def test_sem_err_wfc_2():
    stil_file = get_stil_file("sem_err_wfc_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 53
    assert parser.err_col == 25

def test_sem_err_wfc_3():
    stil_file = get_stil_file("sem_err_wfc_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 70
    assert parser.err_col == 24

def test_sem_err_wfc_4():
    stil_file = get_stil_file("sem_err_wfc_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 53
    assert parser.err_col == 25

def test_sem_err_wfc_5():
    stil_file = get_stil_file("sem_err_wfc_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 54
    assert parser.err_col == 25

def test_sem_err_wfc_6():
    stil_file = get_stil_file("sem_err_wfc_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 53
    assert parser.err_col == 24

def test_sem_err_label_1():
    stil_file = get_stil_file("sem_err_label_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 54
    assert parser.err_col == 21

def test_sem_err_label_2():
    stil_file = get_stil_file("sem_err_label_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 53
    assert parser.err_col == 9

def test_sem_err_signal():
    stil_file = get_stil_file("sem_err_signal.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 52
    assert parser.err_col == 18

def test_sem_err_sig_wfc():
    stil_file = get_stil_file("sem_err_sig_wfc.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 52
    assert parser.err_col == 24

def test_sem_err_goto_label_1():
    stil_file = get_stil_file("sem_err_goto_label_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 53
    assert parser.err_col == 14

def test_sem_err_goto_label_2():
    stil_file = get_stil_file("sem_err_goto_label_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 55
    assert parser.err_col == 1

def test_sem_ok_goto():
    stil_file = get_stil_file("sem_ok_goto.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == -1
    assert parser.err_col == -1
