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
    return os.path.join(str(folder), "stil_files", "timing_block", file_name)


def test_syn_err_timing_block_1():
    stil_file = get_stil_file("syn_err_timing_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 23
    assert parser.err_col == 8

def test_syn_err_timing_block_2():
    stil_file = get_stil_file("syn_err_timing_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 23
    assert parser.err_col == 20

def test_syn_err_timing_block_3():
    stil_file = get_stil_file("syn_err_timing_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 23
    assert parser.err_col == 8

def test_syn_err_timing_block_4():
    stil_file = get_stil_file("syn_err_timing_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 24
    assert parser.err_col == 17

def test_syn_err_timing_block_5():
    stil_file = get_stil_file("syn_err_timing_block_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 24
    assert parser.err_col == 21

def test_syn_err_timing_block_6():
    stil_file = get_stil_file("syn_err_timing_block_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 26
    assert parser.err_col == 7

def test_syn_err_timing_block_7():
    stil_file = get_stil_file("syn_err_timing_block_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 12

def test_syn_err_timing_block_8():
    stil_file = get_stil_file("syn_err_timing_block_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 12

def test_syn_err_timing_block_9():
    stil_file = get_stil_file("syn_err_timing_block_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 12

def test_syn_err_timing_block_10():
    stil_file = get_stil_file("syn_err_timing_block_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 26
    assert parser.err_col == 5

def test_syn_err_timing_block_11():
    stil_file = get_stil_file("syn_err_timing_block_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 10

def test_syn_err_timing_block_12():
    stil_file = get_stil_file("syn_err_timing_block_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 15

def test_syn_err_timing_block_13():
    stil_file = get_stil_file("syn_err_timing_block_13.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 19

def test_syn_err_timing_block_14():
    stil_file = get_stil_file("syn_err_timing_block_14.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 24

def test_syn_err_timing_block_15():
    stil_file = get_stil_file("syn_err_timing_block_15.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 24

def test_syn_err_timing_block_16():
    stil_file = get_stil_file("syn_err_timing_block_16.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 31
    assert parser.err_col == 1

def test_syn_err_timing_block_17():
    stil_file = get_stil_file("syn_err_timing_block_17.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 17

def test_syn_err_timing_block_18():
    stil_file = get_stil_file("syn_err_timing_block_18.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 26

def test_syn_err_timing_block_19():
    stil_file = get_stil_file("syn_err_timing_block_19.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 24

def test_syn_err_timing_block_20():
    stil_file = get_stil_file("syn_err_timing_block_20.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 24
    assert parser.err_col == 16

def test_syn_err_timing_block_21():
    stil_file = get_stil_file("syn_err_timing_block_21.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 28
    assert parser.err_col == 14

def test_syn_ok_timing_block_1():
    stil_file = get_stil_file("syn_ok_timing_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_err_timing_block_1():
    stil_file = get_stil_file("sem_err_timing_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 34
    assert parser.err_col == 8

def test_sem_err_timing_block_2():
    stil_file = get_stil_file("sem_err_timing_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 34
    assert parser.err_col == 19

def test_sem_err_timing_block_3():
    stil_file = get_stil_file("sem_err_timing_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 33
    assert parser.err_col == 17

def test_sem_err_timing_block_4():
    stil_file = get_stil_file("sem_err_timing_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 24
    assert parser.err_col == 16

def test_sem_err_timing_block_5():
    stil_file = get_stil_file("sem_err_timing_block_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 22
    assert parser.err_col == 9

def test_sem_err_timing_block_6():
    stil_file = get_stil_file("sem_err_timing_block_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 22
    assert parser.err_col == 17

def test_sem_err_timing_block_7():
    stil_file = get_stil_file("sem_err_timing_block_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 22
    assert parser.err_col == 24

def test_sem_err_timing_block_8():
    stil_file = get_stil_file("sem_err_timing_block_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 23
    assert parser.err_col == 14

def test_sem_ok_timing_block_1():
    stil_file = get_stil_file("sem_ok_timing_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_ok_timing_block_2():
    stil_file = get_stil_file("sem_ok_timing_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    period = parser.wft2period['*global*::wft']
    assert period == '400000000fs'
    
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_ok_timing_block_3():
    stil_file = get_stil_file("sem_ok_timing_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    period = parser.wft2period['*global*::wft']
    # Period '(1.0 / PLL_Freq) * 2';
    assert period == '400000000fs'
    
    sti = parser.sig_wft2timing['*global*::wft::si1']
    wfcs = sti.get_wfcs()
    wfcs = sti.get_wfcs()
    for wfc in wfcs:
        timing = sti.get_timing_for_wfc(wfc)
        for wfe_time in timing:
            wfe = wfe_time[0]
            time = wfe_time[1]
            if wfc == '0' and wfe == 'D':
                # PLL_Freq = 5MHz
                # si {0 {'1 / PLL_Freq' D;}}
                assert time == '200000000fs'
                continue
            if wfc == '1' and wfe == 'U':
                # PLL_Freq = 5MHz
                # si {1 {'1 / PLL_Freq * 2' U;}}
                assert time == '400000000fs'
                continue
            if wfc == 'A' and wfe == 'D':
                # si {A {'10ns+20ns' D; '25ns' U; '50ns' D;}}
                assert time == '30000000fs'
                continue
            if wfc == 'B' and wfe == 'U':
                # si {B {'10ns' D; '5000ps + 0.02us' U; }}
                assert time == '25000000fs'
                continue
            if wfc == 'S' and wfe == 'D':
                # si {S {'20ns-10ns' D; '25ns' U; }}
                assert time == '10000000fs'
                continue
            if wfc == 'D' and wfe == 'D':
                # si {D {'10ns/2' D; '25ns' U; }}
                assert time == '5000000fs'
                continue
    
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_ok_timing_block_4():
    stil_file = get_stil_file("sem_ok_timing_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1

def test_issue_50():
    stil_file = get_stil_file("issue_50.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1
