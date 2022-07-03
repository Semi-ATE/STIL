# -*- coding: utf-8 -*-
from .STILParser import STILParser

from .WFCUtils import WFCUtils
from .DomainUtils import DomainUtils
from .PattVecCmd import PattVecCmd
from .HashInfo import HashInfo
from .STILDumpCompilerExceptions import STILDumpCompilerException

import os

'''
This is an example class which can be used as a base for a real STIL compiler.
The main compile method will make a syntax and semantic analisys of the file
and will dump the content of the STIL file in several text files:
    
pattern_blocks.flow :   this is the main entry point which define the order of 
                        pattern blocks execution (in *.pattern_blocks files), 
                        depends on information found in PatternExec/PatternBurst 
                        blocks.

*.pattern_blocks    :   one or more files with "compiled" information from the 
                        pattern blocks. The information includes : one or more 
                        lines for every vector statement as vector address with 
                        information for WaveformCharacter for every used signal 
                        and pattern statement as separate command.
                        The format is the following:
                        #                                               -> start of comment
                        SIGNALS_ORDER|sig1+...+sigN                     -> order of the signal used to decode WFC to signal information
                        VA|VAP|VAMP|WFCS|CMD|CMD_ARG| ... |CMD|CMD_ARG  -> one vector address
                        Where:
                            |    is a data separator.
                            VA   is the absolute vector address for the particular 
                                 pattern block.
                            VAP  is the absolute vector address for every pattern 
                                 statement in the pattern block if there is no 
                                 Macro or expanding Procedure invocation in this 
                                 pattern block. 
                                 Value '-' indicates that there is WFC/CMD data 
                                 from Macro/Procdure at this VA
                            VAMP is absolute vector address of the Macro or expanded Procedure block.
                                 Value '-' indicates that there is no WFC/CMD 
                                 data from Macro/Procdure at this VA
                            WFCS is a ordered WaveformCharacter for every used 
                                 signal in the pattern block. The order of signals is defined in SIGNALS_ORDER line
                            CMD  Short name of the command. The command is based 
                                 on found pattern statement in the pattern block. 
                                 One pattern statement can generate one or more commands.
                                 For example : 
                                     "Loop X { ... }" statement will generate three commands:
                                         "LLC" (Load Loop Counter) with value X 
                                                 which indicates how many times 
                                                 the block will repeat.
                                         "SP" (Start Loop) on the first "Vector" 
                                                 statement after the "Loop" statement. 
                                                 This command defines the address where 
                                                 the EL must jump if the X counter 
                                                 value not reached.
                                         "EL" (End Loop) which will be placed on 
                                                 the last vector of the Loop block 
                                                 and will jump to SP address
                                     "Stop" statement will generate just one command - "E" (stands for End)
                            CMD_ARG : value of the CMD if applicable. For example the counter for the "LLC" command (Load Loop Counter)
                            Note : for one vector address, multiple commands can exists. 
                            They will be separated with "|".
                            The full description of the commands is available in every generated pattern_blocks file.
                            
*.procedure_block   :   one or more files with "compiled" information from the 
                        procedures blocks if the option "expanding_procs" is 
                        set to False.
                        The format is the same as in the *.pattern_blocks
                        
pattern_name.sm     :   Scan memory file which contains WFC sequence for every 
                        signal used in Procedure or Macro invocation. Depends on
                        locations and number of # in the procedure or macro bodies,
                        not all WFC in the procdure/macro call will be available
                        in the .sm file due WFC substition and normalization
                        according the STIL standard.

timing.txt          :   Text file with timing information 
                        
Class's arguments (passed as class constructor arguments):
    
    stil_file               : location of the input stil file. Mandatory
    
    expanding_procs         : Expanding or not the vectors from procedures into
                              the pattern block where the procedure is called.
                              Expanding is useful if the ATE pattern engine 
                              lack of capabilities to execute real procedures. 
                              This option impacts calculation of the vector addreses.
                              
    is_scan_mem_available   : depends on ATE pattern engine capabilities,
                              WFC used as arguments in the Macro/Proc invocation
                              can be stored into a dedicated scan memory or to 
                              be expanded in the general available memory.
                              If the option is False, all WFC will be expanded
                              into vector statements in the pattern block where
                              procedures or macros with "Shift" statements are
                              invoked.
                              This option impacts calculation of the vector addreses.
    
    out_folder              : output folder where files will be generated. If
                              not provided, they will be generated in the current
                              working folder
    
    signals_order_file      : file with custom order of the signals. One line - one signal name
    
Restrictions:
    Because ATE pattern engine can have many restrictions (in the HW or in the FW),
    our dump compiler is based on imaginary HW/FW with the following capabilities 
    and restrictoins:
        1. One vector address can hold unlimited commands.
        2. Unlimited number of:
            - Signals
            - Named Signals groups
            - Named Timing blocks
            - Waveform tables in one Timing block
            - Waveform characters (WFC) per signals 
            - Waveform events (WFE) per WFC at any place within one period.
              All defined in IEEE 1450.0 WFE are supported.
            - Vector addresses
            - Procedures calls
            - Named PatternExec/PatternBurts blocks
            - Named Pattern blocks
        3. No restrictions for the period value in any Waveform table.
        4. Call to a procedure command is always placed in the vector preceded
           the "Call" statement. This means "Call" statement, before any "Vector" 
           statement will throw a compilation error. This restriction is not
           valid if option "expanding_procs" is set to value "True".
           The reason behind this restriction is to use the prevoiuos vector 
           statement as place to put the FW command for preparation the jump to
           the procedure's first address.
        5. Call to a procedure statement is not allowed immediately after end of 
           Loop/MatchLoop statement block. The reason is again the need for a 
           vector to place the "jump to procedure" command. If such command is 
           placed in the last vector of the Loop/MatchLoop command, it will 
           always jump to the procedure at the last vector of the Loop/MatchLoop 
           block instead the first vector after the Loop/MatchLoop block.
        6. Nested Loop/MatchLoop blocks are not allowed. Compilation error will be thrown.
        7. Loop/MatchLoop statements need a command to set the number of loops.
           This must be done before the first vector where the Loop/MatchLoop 
           block statements start. Because of this, the following cases, will 
           thrown compilation errors:
               - There is no Vector statement before end of one Loop/MatchLoop 
                 block and the next one.
               - When the start of the Loop/MatchLoop block is the first statement
                 before any "Vector" statement.
        8. Backward GoTo statements (go to the label, prevoiusly defined) will 
           trown a compilation error. This is to prevent an endless cycle.
        9. In the case when "#" (incremental data substitution) is before or 
           after the Shift block and the option "expanding_procs" is False, the 
           compiler will thrown an error, because we assume that scan memory can
           be used only in the shift block. Otherwise every call to a not expanded 
           procedure have to set WFC values in the pre- and post- shift occurance 
           of the "#".

'''

class STILDumpCompiler(STILParser):
    def __init__(
        self,
        stil_file,
        out_folder,
        signals_order_file = None,
        propagate_positions = True,
        expanding_procs = False,
        is_scan_mem_available = False,
        dump_data = True,
        enable_trace = True,
        stil_lark_file = None,
        extra_grammars = [],
        debug = False,
    ):

        STILParser.__init__(self, stil_file, propagate_positions, expanding_procs, stil_lark_file, extra_grammars, debug)
        # Depends on ATE pattern engine capabilities, WFC used as arguments in the Macro/Proc invocation
        # can be stored into a dedicated scan memory or to be expanded in the general available memory
        # This choice impacts calculation of the total VA
        self.is_scan_mem_available = is_scan_mem_available
        
        # In the case when the STILDumpCompiler is used as base for a real compiler
        # this option will supprass the creation of the text files by STILDumpCompiler
        self.dump_data = dump_data
        
        self.enable_trace = enable_trace
        
        out_folder = os.path.join(os.getcwd(), out_folder)
        try: 
            os.mkdir(out_folder)
        except OSError: 
            pass

        self.out_folder = out_folder
        
        self.signals_order = []
        
        if signals_order_file != None:
            if os.path.exists(signals_order_file):
                with open(signals_order_file) as f:
                    self.signals_order.append(f.readline())
            else:
                raise Exception("File with signal order does not exists")
        # Key is in format SignalsGroupDomain::Pattern
        # Value is a dict with :
        #    key - signal name
        #    value is a list with WFC for this signal
        self.sgd_patt2sig2WFCs = {}

        # Number of wfc for the first vector address for each pattern block
        #    key - pattern block name
        #    value - number of wfcs
        self.patt2wfcs_number = {}

        # Key is in format MacroDefsDomain::Macro
        # Value is a list with all SignalsGroup domains used by macro
        self.macro2signal_group_domains = {}
        # Key is in format SignalsGroupDomain::MacroDefsDomain::Macro
        # Value is a dict with :
        #    key - signal name
        #    value is a list with WFC for this signal
        self.sgd_macro2sig2WFCs = {}
        # Number of wfc for the first vector address for each MacroDefs::Macro block
        #    key - MacroDefs block domain :: Macro block name
        #    value - number of wfcs
        self.macro2wfcs_number = {}

        # Key is in format ProceduresDomain::Procedure
        # Value is a list with all SignalsGroup domains used by procedure
        self.proc2signal_group_domains = {}
        # Key is in format SignalsGroupDomain::ProceduresDomain::Procedure
        # Value is a dict with :
        #    key - signal name
        #    value is a list with WFC for this signal
        self.sgd_proc2sig2WFCs = {}
        # Number of wfc for the first vector address for each Procedures::Procedure block
        #    key - Procedures block domain :: Procedure block name
        #    value - number of wfcs
        self.proc2wfcs_number = {}


        # dict key   is the pattern name
        # dict value is a list of command lists like:
        # pattern_name : [[VECTOR_0, LABEL, WFT], [VECTOR_1], ..., [CALL]]
        # In one vector address we can have multiple commands
        self.patt2cmd = {}

        # dict key   is the macro name in full domain format -> domain::macro_name
        # dict value is a list of command lists like:
        # pattern_name : [[VECTOR_0, LABEL, WFT], [VECTOR_1], ..., [CALL]]
        # In one vector address we can have multiple commands.
        self.macro2cmd = {}

        # dict key   is the procedure name in full domain format -> domain::procedure_name
        # dict value is a list of command lists like:
        # pattern_name : [[VECTOR_0, LABEL, WFT], [VECTOR_1], ..., [CALL]]
        # In one vector address we can have multiple commands and 
        # in the case of not expanded Procedures we do not have 
        # vector address at all, because the ATE engine must invoke 
        # the procedure code from separate addresss space
        self.proc2cmd = {}

        # Key is in format SignalsGroupDomain::ProceduresDomain::Procedure
        # Value is a dict with :
        #    key - signal name in the condition statamenet
        #    value is a list with WFC for this signal
        #self.sgd_proc2cond_sig2WFCs = {}

        # Current pattern command : PattVecCmd object
        self.curr_cmd = None
        
#        self.is_shift = False
#        self.is_condition_stmt = False
        self.is_fixed_stmt = False

        # Temp dict with :
        # Key is in format SignalsGroupDomain::PatternName
        # Value is a list with all signals for this pair of key
        self.sgd_patt2signals = {}
        # Key is in format SignalsGroupDomain::PatternName::SignalName
        # Value is the default WFC for this signal, taken either from Condition 
        # statment or from the first Vector statement
        self.sgd_patt_sig2defWFC = {}
        
        # Last signal to WFC info, common for pattern/macro/proc
        # key is signals group domain 
        # value is a dict with key signal name and value WFC 
        self.sgd2last_sig2wfc = {}

        # WFC before the first # or % per signals, common for pattern/macro/proc
        # Used when WFC of a signal is not defined after # or %. 
        # key is signals group domain 
        # value is a dict with key signal name and value WFC 
        self.sgd2before_subs_sig2wfc = {}

        # dict key   is the procedure name in full domain format -> domain::procedure_name
        # dict value is the number of vector addresses used by the procedure
        self.proc2vas = {}

        # scan data is a list with maps which contains :
        # key - timing_domain::wft_name::signal name
        # value - WFC list 
        self.scan_data = []

        # data contains list of lists with :
        # [0]     VA - list with vector addresses
        # [1]     | separator 
        # [2]     VAP - list with pattern only vector addresses
        # [3]     | separator 
        # [4]     VAMP -list with macro/proc only vector addresses
        # [5]     | separator 
        # [6+X-1]   For every used signal (total X signals), separate list with own WFCs
        # [6+X]   | separator 
        # [6+X+1] one or more commands for every vector address, separated with |. Temporary, it will be replaced by next record:
        # [6+X+2] PattVecCmd for every vector. Late
        self.data = []
        
        self.is_matchloop_inf = False

    def compile(self):

        if self.enable_trace:
            print("\nSyntax parsing is in progress...")
        self.parse_syntax()
        if self.enable_trace:
            print("Semantic analisys is in progress...")
        self.parse_semantic()
        # The real compilation will happen once the semantic
        # parsing is finished in self.eof() method bellow

    def eof(self):
        # at the end of the file:
        if self.enable_trace:
            print("Dump compilation is in progress...")
        try:
            self.dump_timing_data()
            self.dump_pattern_flow()
            if self.expanding_procs == False:
                 self.dump_procedures()
            patt_va, proc_va = self.dump_pattern_blocks()
            self.assamble_all()

            if self.enable_trace:
                print(f"Vector statements in pattern blocks : {patt_va}")
                if self.expanding_procs:
                    print(f"Vector statements in procedures blocks : {proc_va} (Procedure memory option is disabled) ")
                else:
                    print(f"Vector statements in procedures blocks : {proc_va}")
                print("Compiled with the following options:")
                if self.is_scan_mem_available:
                    print(" => Scan memory option is enabled [is_scan_mem_available=True] ")
                else:
                    print(" => Scan memory option is disabled (shift operator is expanded) [is_scan_mem_available=False] ")
                if self.expanding_procs:
                    print(" => Procedure memory option is not available [expanding_procs=True]")
                else:
                    print(" => Procedure memory option is available [expanding_procs=False]")
    
                print("Compilation is finished.")

        except STILDumpCompilerException as e:
            print(e.msg)
            os._exit(1)
            
    def add_cmd_patt(self, cmd, value=None):

        if self.curr_cmd == None:
            self.curr_cmd = PattVecCmd()
        self.curr_cmd.add_cmd(cmd, value)

    def add_prop_cmd_patt(self, cmd, prop, value):
        if self.curr_cmd == None:
            self.curr_cmd = PattVecCmd()
        self.curr_cmd.add_prop(cmd, prop, value)

    def save_cmd_patt(self):
        patt_cmd = self.patt2cmd[self.curr_pattern]
        patt_cmd.append(self.curr_cmd)
        self.curr_cmd = None

    def save_in_prev_cmd_patt(self, cmd, value = None):
        patt_cmd = self.patt2cmd[self.curr_pattern]
        vec_cmd = patt_cmd[-1]
        vec_cmd.add_cmd(cmd, value)

    def add_cmd_macro(self, cmd, value=None):
        if self.curr_cmd == None:
            self.curr_cmd = PattVecCmd()
        self.curr_cmd.add_cmd(cmd, value)        

    def save_cmd_macro(self):
        patt_cmd = self.macro2cmd[self.curr_macro_name]
        patt_cmd.append(self.curr_cmd)
        self.curr_cmd = None

    def save_in_prev_cmd_macro(self, cmd, value = None):
        patt_cmd = self.macro2cmd[self.curr_macro_name]
        vec_cmd = patt_cmd[-1]
        vec_cmd.add_cmd(cmd, value)

    def add_cmd_proc(self, cmd, value=None):
        if self.curr_cmd == None:
            self.curr_cmd = PattVecCmd()
        self.curr_cmd.add_cmd(cmd, value)
        
    def save_cmd_proc(self):
        patt_cmd = self.proc2cmd[self.curr_proc_name]
        patt_cmd.append(self.curr_cmd)
        self.curr_cmd = None

    def save_in_prev_cmd_proc(self, cmd, value = None):
        patt_cmd = self.proc2cmd[self.curr_proc_name]
        vec_cmd = patt_cmd[-1]
        vec_cmd.add_cmd(cmd, value)

    def b_signals__close_signal_block(self, t):
        if len(self.signals_order) > 0:
            for existing_signal in self.sig2type:
                if existing_signal not in self.signals_order:
                    raise Exception(f"Can not follow the signal order in {self.signals_order_file} due missing signal in signal block")
    
    def b_pattern__pattern_statements__WAVEFORM_TABLE_NAME(self, t):
        super().b_pattern__pattern_statements__WAVEFORM_TABLE_NAME(t)
        self.add_cmd_patt(PattVecCmd.CMD_WFT, self.curr_wft)

    def b_macrodefs__pattern_statements__WAVEFORM_TABLE_NAME(self, t):
        super().b_macrodefs__pattern_statements__WAVEFORM_TABLE_NAME(t)
        self.add_cmd_macro(PattVecCmd.CMD_WFT, self.curr_wft)

    def b_procedures__pattern_statements__WAVEFORM_TABLE_NAME(self, t):
        super().b_procedures__pattern_statements__WAVEFORM_TABLE_NAME(t)
        self.add_cmd_proc(PattVecCmd.CMD_WFT, self.curr_wft)

    def b_pattern__pattern_statements__CALL_VEC_DATA_STRING(self, t):
        ewfc = WFCUtils.expand_wfcs(t.value)
        self.add_prop_cmd_patt(PattVecCmd.CMD_CALL, self.curr_sig_ref, ewfc)
        super().b_pattern__pattern_statements__CALL_VEC_DATA_STRING(t)

    def b_pattern__pattern_statements__MACRO_VEC_DATA_STRING(self, t):
        ewfc = WFCUtils.expand_wfcs(t.value)
        self.add_prop_cmd_patt(PattVecCmd.CMD_MACRO, self.curr_sig_ref, ewfc)
        super().b_pattern__pattern_statements__MACRO_VEC_DATA_STRING(t)

    def b_pattern__pattern_statements__KEYWORD_C(self, t):
        self.is_condition_stmt = True

    def b_pattern__pattern_statements__KEYWORD_CONDITION(self, t):
        self.is_condition_stmt = True

    def b_pattern__pattern_statements__KEYWORD_F(self, t):
        self.is_fixed_stmt = True

    def b_pattern__pattern_statements__KEYWORD_FIXED(self, t):
        self.is_fixed_stmt = True

    def b_pattern__pattern_statements__KEYWORD_V(self, t):
        super().b_pattern__pattern_statements__KEYWORD_V(t)
        self.add_cmd_patt(PattVecCmd.CMD_VECTOR)
        self.is_vector_stmt = True

    def b_macrodefs__pattern_statements__KEYWORD_V(self, t):
        super().b_macrodefs__pattern_statements__KEYWORD_V(t)
        self.add_cmd_macro(PattVecCmd.CMD_VECTOR)

    def b_procedures__pattern_statements__KEYWORD_V(self, t):
        super().b_procedures__pattern_statements__KEYWORD_V(t)
        self.add_cmd_proc(PattVecCmd.CMD_VECTOR)

    def b_pattern__pattern_statements__KEYWORD_VECTOR(self, t):
        super().b_pattern__pattern_statements__KEYWORD_VECTOR(t)
        self.add_cmd_patt(PattVecCmd.CMD_VECTOR)
        self.is_vector_stmt = True

    def b_macrodefs__pattern_statements__KEYWORD_VECTOR(self, t):
        super().b_macrodefs__pattern_statements__KEYWORD_VECTOR(t)
        self.add_cmd_macro(PattVecCmd.CMD_VECTOR)

    def b_procedures__pattern_statements__KEYWORD_VECTOR(self, t):
        super().b_procedures__pattern_statements__KEYWORD_VECTOR(t)
        self.add_cmd_proc(PattVecCmd.CMD_VECTOR)

    def b_pattern__pattern_statements__LABEL(self, t):
        label = super().b_pattern__pattern_statements__LABEL(t)
        self.add_cmd_patt(PattVecCmd.CMD_LABEL, label)

    def b_macrodefs__pattern_statements__LABEL(self, t):
        label = super().b_macrodefs__pattern_statements__LABEL(t)
        self.add_cmd_macro(PattVecCmd.CMD_LABEL, label)
        
    def b_procedures__pattern_statements__LABEL(self, t):
        label = super().b_procedures__pattern_statements__LABEL(t)
        self.add_cmd_proc(PattVecCmd.CMD_LABEL, label)

    def b_pattern__pattern_statements__GOTO_LABEL(self, t):
        super().b_pattern__pattern_statements__GOTO_LABEL(t)
        self.save_in_prev_cmd_patt(PattVecCmd.CMD_GOTO, t.value)

    def b_macrodefs__pattern_statements__GOTO_LABEL(self, t):
        super().b_macrodefs__pattern_statements__GOTO_LABEL(t)
        self.save_in_prev_cmd_macro(PattVecCmd.CMD_GOTO, t.value)

    def b_procedures__pattern_statements__GOTO_LABEL(self, t):
        super().b_procedures__pattern_statements__GOTO_LABEL(t)
        self.save_in_prev_cmd_proc(PattVecCmd.CMD_GOTO, t.value)

    def b_macrodefs__pattern_statements__VEC_DATA_STRING(self, t):
        super().b_macrodefs__pattern_statements__VEC_DATA_STRING(t)

    def b_procedures__pattern_statements__VEC_DATA_STRING(self, t):
        super().b_procedures__pattern_statements__VEC_DATA_STRING(t)
        
    # to be moved to WFC decoding where # is !!!
    def b_macrodefs__pattern_statements__KEYWORD_SHIFT(self, t):
        super().b_macrodefs__pattern_statements__KEYWORD_SHIFT(t)
        self.add_cmd_macro(PattVecCmd.CMD_START_SHIFT)

    def b_procedures__pattern_statements__KEYWORD_SHIFT(self, t):
        super().b_procedures__pattern_statements__KEYWORD_SHIFT(t)
        self.add_cmd_proc(PattVecCmd.CMD_START_SHIFT)

    def b_macrodefs__pattern_statements__close_shift_block(self, t):
        super().b_macrodefs__pattern_statements__close_shift_block(t)
        self.save_in_prev_cmd_macro(PattVecCmd.CMD_STOP_SHIFT)

    def b_procedures__pattern_statements__close_shift_block(self, t):
        super().b_procedures__pattern_statements__close_shift_block(t)
        self.save_in_prev_cmd_proc(PattVecCmd.CMD_STOP_SHIFT)

    def b_pattern__pattern_statements__CALL_PROC_NAME(self, t):
        super().b_pattern__pattern_statements__CALL_PROC_NAME(t)
        patt_cmd = self.patt2cmd[self.curr_pattern]
        #is_empty = (len(patt_cmd) == 0)
        is_not_vec = (patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False)
        is_not_macro = (patt_cmd[-1].have_cmd(PattVecCmd.CMD_MACRO) == False)
        if self.expanding_procs == False and is_not_vec and is_not_macro:
            err_msg = "COMPILER ERROR: At least one Vector statement is required before Call statement!"
            raise Exception(err_msg)
        else:
            self.add_cmd_patt(PattVecCmd.CMD_CALL, self.curr_proc_name_call)

    def b_macrodefs__pattern_statements__CALL_PROC_NAME(self, t):
        super().b_macrodefs__pattern_statements__CALL_PROC_NAME(t)
        patt_cmd = self.macro2cmd[self.curr_macro_name]
        is_empty = (len(patt_cmd) == 0)
        is_not_vec = (patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False)
        if self.expanding_procs == False and (is_empty or is_not_vec):
            err_msg = "COMPILER ERROR: At least one Vector statement is required before Call statement!"
            raise Exception(err_msg)
        else:
            self.add_cmd_macro(PattVecCmd.CMD_CALL, self.curr_proc_name_call)

    def b_proc__pattern_statements__CALL_PROC_NAME(self, t):
        super().b_proc__pattern_statements__CALL_PROC_NAME(t)
        patt_cmd = self.proc2cmd[self.curr_proc_name]
        is_empty = (len(patt_cmd) == 0)
        is_not_vec = (patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False)
        if self.expanding_procs == False and (is_empty or is_not_vec):
            err_msg = "COMPILER ERROR: At least one Vector statement is required before Call statement!"
            raise STILDumpCompilerException(-1, -1, err_msg)
        else:
            self.add_cmd_proc(PattVecCmd.CMD_CALL, self.curr_proc_name_call)

    def b_pattern__pattern_statements__CALL_MACRO_NAME(self, t):
        super().b_pattern__pattern_statements__CALL_MACRO_NAME(t)
        self.add_cmd_patt(PattVecCmd.CMD_MACRO, self.curr_macro_name_call)

    def b_macro__pattern_statements__CALL_MACRO_NAME(self, t):
        super().b_macro__pattern_statements__CALL_MACRO_NAME(t)
        self.add_cmd_macro(PattVecCmd.CMD_MACRO, self.curr_macro_name_call)

    def b_proc__pattern_statements__CALL_MACRO_NAME(self, t):
        super().b_proc__pattern_statements__CALL_MACRO_NAME(t)
        self.add_cmd_proc(PattVecCmd.CMD_MACRO, self.curr_macro_name_call)

    def b_pattern__pattern_statements__LOOP_COUNT(self, t, suppress_by_subclass = False):
        super().b_pattern__pattern_statements__LOOP_COUNT(t)
        
        if suppress_by_subclass == False:
            patt_cmd = self.patt2cmd[self.curr_pattern]
            if len(patt_cmd) == 0 or patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False:
                err_msg = "COMPILER ERROR: At least one Vector statement is required before Loop block!"
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                self.save_in_prev_cmd_patt(PattVecCmd.CMD_LOAD_LOOP_COUNTER, t.value)
                self.add_cmd_patt(PattVecCmd.CMD_START_LOOP)

    def b_macrodefs__pattern_statements__LOOP_COUNT(self, t, suppress_by_subclass = False):
        super().b_macrodefs__pattern_statements__LOOP_COUNT(t)

        if suppress_by_subclass == False:
            patt_cmd = self.macro2cmd[self.curr_macro_name]
            if len(patt_cmd) == 0 or patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False:
                err_msg = "COMPILER ERROR: At least one Vector statement is required before Loop block!"
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                self.save_in_prev_cmd_macro(PattVecCmd.CMD_LOAD_LOOP_COUNTER, t.value)
                self.add_cmd_macro(PattVecCmd.CMD_START_LOOP, t.value)

    def b_procedures__pattern_statements__LOOP_COUNT(self, t, suppress_by_subclass = False):
        super().b_procedures__pattern_statements__LOOP_COUNT(t)

        if suppress_by_subclass == False:
            patt_cmd = self.proc2cmd[self.curr_proc_name]
            if len(patt_cmd) == 0 or patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False:
                err_msg = "COMPILER ERROR: At least one Vector statement is required before Loop block!"
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                self.save_in_prev_cmd_proc(PattVecCmd.CMD_LOAD_LOOP_COUNTER, t.value)
                self.add_cmd_proc(PattVecCmd.CMD_START_LOOP, t.value)

    def b_pattern__pattern_statements__close_loop_block(self, t):
        super().b_pattern__pattern_statements__close_loop_block(t)
        self.save_in_prev_cmd_patt(PattVecCmd.CMD_STOP_LOOP)

    def b_macrodefs__pattern_statements__close_loop_block(self, t):
        super().b_macrodefs__pattern_statements__close_loop_block(t)
        self.save_in_prev_cmd_macro(PattVecCmd.CMD_STOP_LOOP)

    def b_procedures__pattern_statements__close_loop_block(self, t):
        super().b_procedures__pattern_statements__close_loop_block(t)
        self.save_in_prev_cmd_proc(PattVecCmd.CMD_STOP_LOOP)

    def b_pattern__pattern_statements__MATCHLOOP_COUNT(self, t, suppress_by_subclass = False):
        super().b_pattern__pattern_statements__MATCHLOOP_COUNT(t)

        if suppress_by_subclass == False:
            patt_cmd = self.patt2cmd[self.curr_pattern]
            if len(patt_cmd) == 0 or patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False:
                err_msg = "COMPILER ERROR: At least one Vector statement is required before Loop block!"
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                self.save_in_prev_cmd_patt(PattVecCmd.CMD_LOAD_MATCHLOOP_COUNTER, t.value)
                self.add_cmd_patt(PattVecCmd.CMD_START_MATCHLOOP)

    def b_macrodefs__pattern_statements__MATCHLOOP_COUNT(self, t, suppress_by_subclass = False):
        super().b_macrodefs__pattern_statements__MATCHLOOP_COUNT(t)
        
        if suppress_by_subclass == False:
            patt_cmd = self.macro2cmd[self.curr_macro_name]
            if len(patt_cmd) == 0 or patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False:
                err_msg = "COMPILER ERROR: At least one Vector statement is required before Loop block!"
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                self.save_in_prev_cmd_macro(PattVecCmd.CMD_LOAD_MATCHLOOP_COUNTER, t.value)
                self.add_cmd_macro(PattVecCmd.CMD_STRAT_MATCHLOOP, t.value)


    def b_procedures__pattern_statements__MATCHLOOP_COUNT(self, t, suppress_by_subclass = False):
        super().b_procedures__pattern_statements__MATCHLOOP_COUNT(t)

        if suppress_by_subclass == False:
            patt_cmd = self.proc2cmd[self.curr_proc_name]
            if len(patt_cmd) == 0 or patt_cmd[-1].have_cmd(PattVecCmd.CMD_VECTOR) == False:
                err_msg = "COMPILER ERROR: At least one Vector statement is required before Loop block!"
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                self.save_in_prev_cmd_proc(PattVecCmd.CMD_LOAD_MATCHLOOP_COUNTER, t.value)
                self.add_cmd_proc(PattVecCmd.CMD_START_MATCHLOOP, t.value)

    def b_pattern__pattern_statements__MATCHLOOP_INF(self, t):
        super().b_pattern__pattern_statements__MATCHLOOP_INF(t)
        self.add_cmd_patt(PattVecCmd.CMD_START_MATCHLOOP, t.value)
        self.is_matchloop_inf = True

    def b_macrodefs__pattern_statements__MATCHLOOP_INF(self, t):
        super().b_macrodefs__pattern_statements__MATCHLOOP_INF(t)
        self.add_cmd_macro(PattVecCmd.CMD_START_MATCHLOOP, t.value)
        self.is_matchloop_inf = True

    def b_procedures__pattern_statements__MATCHLOOP_INF(self, t):
        super().b_procedures__pattern_statements__MATCHLOOP_INF(t)
        self.add_cmd_proc(PattVecCmd.CMD_START_MATCHLOOP, t.value)
        self.is_matchloop_inf = True

    def b_pattern__pattern_statements__close_matchloop_block(self, t):
        super().b_pattern__pattern_statements__close_matchloop_block(t)
        if self.is_matchloop_inf:
            self.save_in_prev_cmd_patt(PattVecCmd.CMD_STOP_INF_MATCHLOOP)
            self.is_matchloop_inf = False
        else:
            self.save_in_prev_cmd_patt(PattVecCmd.CMD_STOP_COUNT_MATCHLOOP)

    def b_macrodefs__pattern_statements__close_matchloop_block(self, t):
        super().b_macrodefs__pattern_statements__close_matchloop_block(t)
        if self.is_matchloop_inf:
            self.save_in_prev_cmd_macro(PattVecCmd.CMD_STOP_INF_MATCHLOOP)
            self.is_matchloop_inf = False
        else:
            self.save_in_prev_cmd_macro(PattVecCmd.CMD_STOP_COUNT_MATCHLOOP)

    def b_procedures__pattern_statements__close_matchloop_block(self, t):
        super().b_procedures__pattern_statements__close_matchloop_block(t)
        if self.is_matchloop_inf:
            self.save_in_prev_cmd_proc(PattVecCmd.CMD_STOP_INF_MATCHLOOP)
            self.is_matchloop_inf = False
        else:
            self.save_in_prev_cmd_proc(PattVecCmd.CMD_STOP_COUNT_MATCHLOOP)

    def b_pattern__pattern_statements__close_call_vector_block(self, t):
        self.save_cmd_patt()

    def b_pattern__pattern_statements__PROC_CALL_END_STMT(self, t):
        self.save_cmd_patt()

    def b_pattern__pattern_statements__close_macro_vector_block(self, t):
        self.save_cmd_patt()

    def b_pattern__pattern_statements__MACRO_CALL_END_STMT(self, t):
        self.save_cmd_patt()

    def b_pattern__pattern_statements__KEYWORD_IDDQ_TEST_POINT(self, t):
        self.add_cmd_patt(PattVecCmd.CMD_IDDQTESTPOINT, None)
        
    def b_macrodefs__pattern_statements__KEYWORD_IDDQ_TEST_POINT(self, t):
        self.add_cmd_macro(PattVecCmd.CMD_IDDQTESTPOINT, None)
        
    def b_procedures__pattern_statements__KEYWORD_IDDQ_TEST_POINT(self, t):
        self.add_cmd_proc(PattVecCmd.CMD_IDDQTESTPOINT, None)
        
    def b_pattern__pattern_statements__KEYWORD_STOP(self, t):
        self.save_in_prev_cmd_patt(PattVecCmd.CMD_STOP, None)

    def b_pattern__pattern_statements__KEYWORD_STOP_SC(self, t):
        self.save_in_prev_cmd_patt(PattVecCmd.CMD_STOP, None)

    def b_macrodefs__pattern_statements__KEYWORD_STOP(self, t):
        self.save_in_prev_cmd_macro(PattVecCmd.CMD_STOP, None)

    def b_macrodefs__pattern_statements__KEYWORD_STOP_SC(self, t):
        self.save_in_prev_cmd_macro(PattVecCmd.CMD_STOP, None)

    def b_procedures__pattern_statements__KEYWORD_STOP(self, t):
        self.save_in_prev_cmd_proc(PattVecCmd.CMD_STOP, None)
        
    def b_procedures__pattern_statements__KEYWORD_STOP_SC(self, t):
        self.save_in_prev_cmd_proc(PattVecCmd.CMD_STOP, None)


    def b_macrodefs__open_macro_defs_block(self, t):

        if self.is_signal_block_defined == False:
            err_msg = "Expected Signal block before any MacroDefs block"
            raise Exception(err_msg)
        if self.is_signalgroups_block_defined == False:
            err_msg = "Expected SignalGroups block before any MacroDefs block"
            raise Exception(err_msg)
        if self.is_timing_block_defined == False:
            err_msg = "Expected Timing block before any MacroDefs block"
            raise Exception(err_msg)
        if self.is_patternburst_block_defined == False:
            err_msg = "Expected PatternBurst block before any MacroDefs block"
            raise Exception(err_msg)
        if self.is_patternexec_block_defined == False:
            err_msg = "Expected PatternExec block before any MacroDefs block"
            raise Exception(err_msg)

        super().b_macrodefs__open_macro_defs_block(t)

    def b_procedures__open_procedure_block(self, t):

        if self.is_signal_block_defined == False:
            err_msg = "Expected Signal block before any Procedures block"
            raise Exception(err_msg)
        if self.is_signalgroups_block_defined == False:
            err_msg = "Expected SignalGroups block before any Procedures block"
            raise Exception(err_msg)
        if self.is_timing_block_defined == False:
            err_msg = "Expected Timing block before any Procedures block"
            raise Exception(err_msg)
        if self.is_patternburst_block_defined == False:
            err_msg = "Expected PatternBurst block before any Procedures block"
            raise Exception(err_msg)
        if self.is_patternexec_block_defined == False:
            err_msg = "Expected PatternExec block before any Procedures block"
            raise Exception(err_msg)


        super().b_procedures__open_procedure_block(t)

    def b_macrodefs__MACRO_NAME(self, t):

        super().b_macrodefs__MACRO_NAME(t)
        
        self.sgd2last_sig2wfc = {}
        self.sgd2before_subs_sig2wfc = {}
        
        self.macro2cmd[self.curr_macro_name] = []
        self.macro2signal_group_domains = {}

        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:
    
                macro_domain = self.patt_burst2macro_domain[patt_burst]
                sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]
                
                if macro_domain in self.macro_domain2macro_names:
                    
                    macros = self.macro_domain2macro_names[macro_domain]
                
                    for macro in macros:
                        mdn = self.curr_macro_name
                        if mdn in self.macro2signal_group_domains:
                            signal_group_domains = self.macro2signal_group_domains[mdn]
                            if sig_group_domain not in signal_group_domains:
                                signal_group_domains.append(sig_group_domain)
                        else:
                            self.macro2signal_group_domains[mdn] = [sig_group_domain]
            
    def b_procedures__PROCEDURE_NAME(self, t):

        super().b_procedures__PROCEDURE_NAME(t)

        self.sgd2last_sig2wfc = {}
        self.sgd2before_subs_sig2wfc = {}
        
        self.proc2cmd[self.curr_proc_name] = []

        self.proc2signal_group_domains = {}

        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:
    
                proc_domain = self.patt_burst2proc_domain[patt_burst]
                sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]
                
                if proc_domain in self.proc_domain2proc_names:
                    
                    procs = self.proc_domain2proc_names[proc_domain]
                
                    for proc in procs:
                        pdn = self.curr_proc_name
                        if pdn in self.proc2signal_group_domains:
                            signal_group_domains = self.proc2signal_group_domains[pdn]
                            if sig_group_domain not in signal_group_domains:
                                signal_group_domains.append(sig_group_domain)
                        else:
                            self.proc2signal_group_domains[pdn] = [sig_group_domain]

    def b_pattern__PATTERN_NAME(self, t):
        super().b_pattern__PATTERN_NAME(t)

        self.patt2cmd[self.curr_pattern] = []

    def dump_procedures(self):
        
        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():

            time_domain = self.patt_exec_block2time_domain[pattern_exec_block]
            # time_domain = self.patt_exec_block2time_domain[pattern_exec_block]
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:

                proc_domain = self.patt_burst2proc_domain[patt_burst]
                macro_domain = self.patt_burst2macro_domain[patt_burst]
                sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]

                if proc_domain in self.proc_domain2proc_names:
                    procs = self.proc_domain2proc_names[proc_domain]
                    for proc in procs:
                        va = self.dump_procedure(
                            proc, sig_group_domain, proc_domain, macro_domain, time_domain
                        )
                        fpn = DomainUtils.get_full_name(proc_domain, proc)
                        self.proc2vas[fpn] = va

    def dump_procedure(self, proc, sgdomain, pdomain, mdomain, time_domain):

        #print("dump_procedure")
        
        fpn = DomainUtils.get_full_name(pdomain, proc)

        pd = DomainUtils.get_domain(pdomain, True)
        md = DomainUtils.get_domain(mdomain, True)
        sgd = DomainUtils.get_domain(sgdomain, True)

        fn = proc + "_" + pd + "_" + md + "_" + sgd + ".procedure_block"
        fn = fn.replace('"', "_")
         
        file = os.path.join(self.out_folder, fn)
        
        va = self.dump_patt_stmt_block(self.sgd_proc2sig2WFCs, self.proc2cmd , fpn, file, time_domain, sgdomain, pdomain, mdomain, False)
        return va 
    
    def dump_pattern_flow(self):
        
        if self.dump_data:
            # Processing pattern flow before the first pattern block
            file = os.path.join(self.out_folder, "pattern_blocks.flow")
    
            f = open(file, "w")
            f.write(
                "#FORMAT : pattern dump file name | pattern block name | td = Timing domain| sg = SignalsGroup domain | md = MacroDefs domain | pd = Procedures domain\n"
            )
    
            for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
    
                time_domain = self.patt_exec_block2time_domain[pattern_exec_block]
                patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
                # For every pattern burst block in the pattern exec block
                for patt_burst in patt_bursts:
    
                    pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]
                    proc_domain = self.patt_burst2proc_domain[patt_burst]
                    macro_domain = self.patt_burst2macro_domain[patt_burst]
                    sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]
    
                    # For every pattern block in the pattern burst block
                    for patt in pattern_list:
                        td = DomainUtils.get_domain(time_domain, True)
                        sgd = DomainUtils.get_domain(sig_group_domain, True)
                        md = DomainUtils.get_domain(macro_domain, True)
                        pd = DomainUtils.get_domain(proc_domain, True)
                        ext = ".pattern_block"
    
                        fn = patt + "-" + td + "-" + sgd + "-" + md + "-" + pd + ext
    
                        rec = (
                            fn
                            + " | "
                            + patt
                            + " | td="
                            + td
                            + " | sgd="
                            + sgd
                            + " | md="
                            + md
                            + " | pd="
                            + pd
                            + "\n"
                        )
                        f.write(rec)
            f.close()

    def b_pattern__pattern_statements__close_vector_block(self, t):
        
        #print("b_pattern__pattern_statements__close_vector_block")

        # Current pattern block is not used in pattern burst
        if self.curr_pattern not in self.patt2sig_group_domain:
            super().b_pattern__pattern_statements__close_vector_block(t)
            return

        #Ignore so far the Fixed and Condition statements
        if self.is_vector_stmt:
            self.save_cmd_patt()

            sig_groups = self.patt2sig_group_domain[self.curr_pattern]
            #print(f"sig_groups {sig_groups}")
            
            """
            Collecting WFC for all signals in the pattern's Vector statetment
            """
            for sgd in sig_groups:
                #print(f"sgd = {sgd} sig_groups = {sig_groups}")
                sgd_patt = DomainUtils.get_full_name(sgd, self.curr_pattern)
                if sgd_patt not in self.sgd_patt2sig2WFCs:
                    self.sgd_patt2sig2WFCs[sgd_patt] = {}
    
                si = 0
                total_wfc = 0
                for sigs in self.curr_sig_order:
                    sig2wfc = self.sgd_patt2sig2WFCs[sgd_patt]
                    if sigs in self.sig2type:
                        if sigs not in self.sgd_patt2sig2WFCs[sgd_patt]:
                            sig2wfc[sigs] = [self.curr_wfc_order[si]]
                        else:
                            sig2wfc[sigs].append(self.curr_wfc_order[si])
                        #print(f"signal {sigs} sig2wfc {sig2wfc}")
                        total_wfc += 1
                    else:
                        sig = DomainUtils.get_full_name(sgd, sigs)
                        if sig in self.signal_groups2signals:
                            wfci = 0
                            for s in self.signal_groups2signals[sig]:
                                # print(f"signal {s}")
                                if s not in self.sgd_patt2sig2WFCs[sgd_patt]:
                                    sig2wfc[s] = [self.curr_wfc_order[si][wfci]]
                                else:
                                    sig2wfc[s].append(self.curr_wfc_order[si][wfci])
                                #print(f"signal {s} sig2wfc {sig2wfc}")
                                wfci += 1
                            total_wfc += wfci
                        else:
                            sig = DomainUtils.get_name(sig)
                            err_msg = f"Can not find a signal/signal group '{sig}' in the pattern {self.curr_pattern}!"
                            raise Exception(err_msg)
                    si += 1
    
            if self.is_first_vector:
                self.patt2wfcs_number[self.curr_pattern] = total_wfc
            else:
                expected_wfc_number = self.patt2wfcs_number[self.curr_pattern]
                if total_wfc < expected_wfc_number:
                    #print(f"Delta vector expected_wfc_number {expected_wfc_number} != {total_wfc}")
                    """
                    Delta vector, not all WFC are defined
                    """
                    for sgd in sig_groups:
                        sgd_patt = DomainUtils.get_full_name(sgd, self.curr_pattern)
                        sigs2wfc = self.sgd_patt2sig2WFCs[sgd_patt]
                        max_wfc = 0
                        for sig in sigs2wfc.keys(): 
                            ml = len(sigs2wfc[sig])
                            if ml > max_wfc:
                                max_wfc = ml
                        for sig in sigs2wfc.keys():
                            if len(sigs2wfc[sig]) != max_wfc:
                                last_wfc = sigs2wfc[sig][-1]
                                if last_wfc == "#" or last_wfc == "%":
                                    before_subs_sig2wfc = self.sgd2before_subs_sig2wfc[sgd]
                                    if sig in before_subs_sig2wfc:
                                        wfc = before_subs_sig2wfc[sig]
                                        sigs2wfc[sig].append(wfc)
                                    else:
                                        err_msg = f"Missing WFC for a signal {sig} after a vector with '#' or '%'!"
                                        raise Exception(err_msg)
                                        
                                else:
                                    sigs2wfc[sig].append(last_wfc)
        
        if self.is_first_vector and (self.is_condition_stmt or self.is_vector_stmt):
            sig_groups = self.patt2sig_group_domain[self.curr_pattern]

            """
            Collecting all WFC per signals in the first Condition or Vector statetment
            """
    
            for sgd in sig_groups:
                sgd_patt = DomainUtils.get_full_name(sgd, self.curr_pattern)
                if sgd_patt not in self.sgd_patt2signals:
                    self.sgd_patt2signals[sgd_patt] = []
    
                sig_idx = 0
                for sigs in self.curr_sig_order:
                    all_found_sigs = self.sgd_patt2signals[sgd_patt]
                    if sigs in self.sig2type:
                        if sigs not in all_found_sigs:
                            all_found_sigs.append(sigs)
                        sgd_p_s = sgd_patt + "::" + sigs
                        self.sgd_patt_sig2defWFC[sgd_p_s] = self.curr_wfc_order[sig_idx]
                        
                    else:
                        sig = DomainUtils.get_full_name(sgd, sigs)
                        if sig in self.signal_groups2signals:
                            wfc_idx = 0
                            for s in self.signal_groups2signals[sig]:
                                if s not in all_found_sigs:
                                    all_found_sigs.append(s)
                                sgd_p_s = sgd_patt + "::" + s
                                self.sgd_patt_sig2defWFC[sgd_p_s] = self.curr_wfc_order[sig_idx][wfc_idx]
                            wfc_idx += 1
                        else:
                            sig = DomainUtils.get_name(sig)
                            err_msg = f"Can not find a signal/signal group '{sig}' in the pattern {self.curr_pattern}!"
                            raise Exception(err_msg)
                    sig_idx += 1
            for sgd_patt in self.sgd_patt2signals.keys():
                sigs = self.sgd_patt2signals[sgd_patt]
                for sig in sigs:
                    sgd_p_s = sgd_patt + "::" + sig
                    wfc = self.sgd_patt_sig2defWFC[sgd_p_s]
                    if sig not in self.signals_order:
                        self.signals_order.append(sig)
        
        super().b_pattern__pattern_statements__close_vector_block(t)
        self.is_fixed_stmt = False
        self.is_condition_stmt = False
        self.is_vector_stmt = False

    def dump_pattern_blocks(self):
        
        pattern_blocks_va = 0
        proc_blocks_va = 0

        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            #print(f"pattern_exec_block {pattern_exec_block}")
            time_domain = self.patt_exec_block2time_domain[pattern_exec_block]
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:
                #print(f"patt_burst {patt_burst}")

                pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]
                proc_domain = self.patt_burst2proc_domain[patt_burst]
                macro_domain = self.patt_burst2macro_domain[patt_burst]
                sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]

                #print(f"pattern_list {pattern_list}")

                # For every pattern block in the pattern burst block
                for pattern in pattern_list:
                    td = DomainUtils.get_domain(time_domain, True)
                    sgd = DomainUtils.get_domain(sig_group_domain, True)
                    md = DomainUtils.get_domain(macro_domain, True)
                    pd = DomainUtils.get_domain(proc_domain, True)
                    ext = ".pattern_block"
                    fn = pattern + "-" + td + "-" + sgd + "-" + md + "-" + pd + ext
                    fn = fn.replace('"', "_")
                    patt_va, proc_va = self.dump_patt_stmt_block(self.sgd_patt2sig2WFCs, self.patt2cmd,  pattern, fn, time_domain, sig_group_domain, macro_domain, proc_domain, True)
                    pattern_blocks_va += patt_va
                    proc_blocks_va += proc_va
                    
        return pattern_blocks_va, proc_blocks_va
    
    def initial_fill_data(self, data, va_length):
        sep= ['|']*(va_length)
        empty_va = ['-']*(va_length)
        # [0]     VA - vector addresses
        data.append(range(va_length))
        # [1]     | separator 
        data.append(sep)
        # [2]     VAP - pattern only vector addresses
        data.append(empty_va)
        # [3]     | separator 
        data.append(sep)
        # [4]     VAMP - macro/proc only vector addresses
        data.append(empty_va)
        # [5]     | separator 
        data.append(sep)
        return data

    def wfc_substitution(self, hash_info, arg_sig2wfc, sig2wfcs, signals, sig_group_domain, cond_sig2wfc):
        """
        Replacing # and % with WFC from Macro/Procedure invocation according 
        the STIL standard.
        """
        # Key   - the signal name
        # value - wfc length of signals which are called in the Macro/Proc
        arg_wfcs_length = {}
        # Key - the signal name, value - number of pre-shift # per this signal
        pre_shift = {}
        # Key - the signal name, value - number of post-shift # per this signal
        post_shift = {}
        # List with signals which have # in any vector address
        signals_with_hash = []
        # List with signals which have # in a shift block
        signals_with_shift_hash = []
        # Key   - the signal name
        # value - shift cycles = arg_wfcs_length - (pre_shift + post_shift)
        shift_cycles = {}
        # Maximum value in shift_cycles
        max_scan_shift = 0        
        # Key   - the signal name
        # value - padding WFC count = max_scan_shift - shift_cycles
        padding_len = {}
        # List with input type signals which have to be pre padded
        prepad_sig = []
        # List with output type signals which have to be post padded
        postpad_sig = []
           
        for sig in signals:
            if sig in arg_sig2wfc:
                wfcs = arg_sig2wfc[sig]
                arg_wfcs_length[sig] = len(wfcs)
                #print(f"sig {sig} len {len(wfcs)}")
                
        # in the case of signals group part of argument WFC
        new_sig2wfc = {}
        for sg in arg_sig2wfc:
            fsg = DomainUtils.get_full_name(sig_group_domain, sg)
            if fsg in self.signal_groups2signals:
                signals_group = self.signal_groups2signals[fsg]
                si = 0
                for signal in signals_group:
                    wfcs = arg_sig2wfc[sg][si]
                    arg_wfcs_length[signal] = len(wfcs)
                    new_sig2wfc[signal] = [wfcs]
                    si += 1
        for sig in new_sig2wfc:
            arg_sig2wfc[sig] = new_sig2wfc[sig]
        
        for hi in hash_info:

            if hi.pos_rel_shift == HashInfo.POS_BEFORE_SHIFT:
                
                if self.expanding_procs == False:
                    err_msg = "When option expanding_procs is False, '#' before Shift block is not allowed!"
                    raise STILDumpCompilerException(-1, -1, err_msg)
                
                if hi.sig_ref in self.sig2type:
                    if hi.sig_ref in pre_shift:
                        pre_shift[hi.sig_ref] += 1
                    else:
                        pre_shift[hi.sig_ref] = 1
                    if hi.sig_ref not in signals_with_hash:
                        signals_with_hash.append(hi.sig_ref)
                else:
                    sg = DomainUtils.get_full_name(sig_group_domain, hi.sig_ref)
                    sig_group = self.signal_groups2signals[sg]
                    for pos in hi.pos:
                        sig = sig_group[pos]
                        if sig in pre_shift:
                            pre_shift[sig] += 1
                        else:
                            pre_shift[sig] = 1
                        if sig not in signals_with_hash:
                            signals_with_hash.append(sig)
                            
            elif hi.pos_rel_shift == HashInfo.POS_AFTER_SHIFT:
                
                if self.expanding_procs == False:
                    err_msg = "When option expanding_procs is False, '#' after Shift block is not allowed!"
                    raise STILDumpCompilerException(-1, -1, err_msg)

                if hi.sig_ref in self.sig2type:
                    if hi.sig_ref in post_shift:
                        post_shift[hi.sig_ref] += 1
                    else:
                        post_shift[hi.sig_ref] = 1
                    if hi.sig_ref not in signals_with_hash:
                        signals_with_hash.append(hi.sig_ref)
                else:
                    sg = DomainUtils.get_full_name(sig_group_domain, hi.sig_ref)
                    sig_group = self.signal_groups2signals[sg]
                    for pos in hi.pos:
                        sig = sig_group[pos]
                        if sig in post_shift:
                            post_shift[sig] += 1
                        else:
                            post_shift[sig] = 1
                        if sig not in signals_with_hash:
                            signals_with_hash.append(sig)
                            
            elif hi.pos_rel_shift == HashInfo.POS_SHIFT:
                
                if hi.sig_ref in self.sig2type:
                    if hi.sig_ref not in signals_with_hash:
                        signals_with_hash.append(hi.sig_ref)
                    if hi.sig_ref not in signals_with_shift_hash:
                        signals_with_shift_hash.append(hi.sig_ref)
                        
                else:
                    sg = DomainUtils.get_full_name(sig_group_domain, hi.sig_ref)
                    sig_group = self.signal_groups2signals[sg]
                    for pos in hi.pos:
                        sig = sig_group[pos]
                        if sig not in signals_with_hash:
                            signals_with_hash.append(sig)
                        if sig not in signals_with_shift_hash:
                            signals_with_shift_hash.append(sig)
        
        for sig in signals_with_hash:
            if sig not in arg_sig2wfc:
                arg_sig2wfc[sig] = ""
        
        for sig in signals:
            
            l = 0
            if sig in arg_wfcs_length:
                l = arg_wfcs_length[sig]
                
            pre_shift_count = 0
            if sig in pre_shift:
                pre_shift_count = pre_shift[sig]
                
            post_shift_count = 0
            if sig in post_shift:
                post_shift_count = post_shift[sig]

            if sig in signals_with_shift_hash:
               
                shift_cycles[sig] = l - (pre_shift_count + post_shift_count)
                if shift_cycles[sig] > max_scan_shift:
                    max_scan_shift = shift_cycles[sig]
            
        # Padding WFC count = max_scan_shift - shift_cycles
        for sig in signals:
            if sig in shift_cycles:
                pad = max_scan_shift - shift_cycles[sig]
                if pad > 0:
                    padding_len[sig] = pad
                    if self.sig2type[sig] == "In":
                        prepad_sig.append(sig)
                        #print(f"pre padding for signal {sig} : {pad}")
                    elif self.sig2type[sig] == "Out":
                        postpad_sig.append(sig)
                        #print(f"post padding for signal {sig} : {pad}")
                    elif sig in self.scanin_sigs:
                        postpad_sig.append(sig)
                    elif sig in self.scanout_sigs:
                        postpad_sig.append(sig)
                    else:
                        err_msg = "COMPILER ERROR: padding is unknown for none unidirectional signal"
                        raise STILDumpCompilerException(-1, -1, err_msg)
                        
        # Pre-padding
        for sig in prepad_sig:
            
            if sig not in sig2wfcs:
                continue
            
            wfcs = sig2wfcs[sig]
            # Get the last defined WFC before the #
            indx = -1;
            prepad_value = None
            for wfc in wfcs:
                if wfc == "#":
                    if indx > -1:
                        prepad_value = wfcs[indx]
                    break
                else:
                    indx += 1
                    
            if prepad_value == None:
                if cond_sig2wfc != None:
                    if sig in cond_sig2wfc:
                        prepad_value = cond_sig2wfc[sig][0]
                    
            if prepad_value == None:
                err_msg = "COMPILER ERROR: Can not find pre-padding value in the vector before the first #"          
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                pad_count = padding_len[sig]
                padding_data = pad_count*prepad_value
                arg_sig2wfc[sig] = padding_data + arg_sig2wfc[sig]

        # Post-padding
        for sig in postpad_sig:
            
            if sig not in sig2wfcs:
                continue
            
            wfcs = sig2wfcs[sig]
            # Get the last defined WFC before the #
            indx = -1;
            postpad_value = None
            for wfc in wfcs:
                if wfc == "#":
                    if indx > -1:
                        postpad_value = wfcs[indx]
                    break
                else:
                    indx += 1

            if postpad_value == None:
                if sig in cond_sig2wfc:
                    postpad_value = cond_sig2wfc[sig][0]

            if postpad_value == None:
                err_msg = "COMPILER ERROR: Can not find post-padding value in the vector before the first #"        
                raise STILDumpCompilerException(-1, -1, err_msg)
            else:
                pad_count = padding_len[sig]
                padding_data = pad_count*postpad_value
                arg_sig2wfc[sig] = arg_sig2wfc[sig] + padding_data
                #print(f"post padding arg_sig2wfc[{sig}] {arg_sig2wfc[sig]}")

    
        # Key is the signal name
        # Value is a list with the WFC of this signal per each VA
        new_sig2wfcs = {}
        # Key is the signal name
        # Value is a list with scan chain memory filled with WFC
        scan_mem = {}
        
        shift_pos = -1

        # Processing signals which have # in shift block        
        for sig in signals:
            
            if sig not in sig2wfcs:
                continue
            
            wfcs = sig2wfcs[sig]
            
            new_vectors = 0
            
            if sig in arg_sig2wfc and sig in signals_with_shift_hash:
                #print(f" signals_with_shift_hash {sig}")
                new_sig2wfcs[sig] = []
                pre = 0
                if sig in pre_shift:
                    pre = pre_shift[sig]
                post = 0
                if sig in post_shift:
                    post = post_shift[sig]
                is_shift_done = False
                arg_indx = 0
                for i in range(len(wfcs)):
                    if wfcs[i] == '#':
                        if pre > 0:
                            new_sig2wfcs[sig].append(arg_sig2wfc[sig][arg_indx])
                            arg_indx += 1
                            pre -= 1
                        elif is_shift_done == False:
                            shift_pos = i
                            is_hash_added = False
                            for ii in range(max_scan_shift):
                                wfc = arg_sig2wfc[sig][arg_indx]
                                if self.is_scan_mem_available:
                                    if is_hash_added == False:
                                        is_hash_added = True
                                        new_sig2wfcs[sig].append("#")
                                    if sig not in scan_mem:
                                        scan_mem[sig] = []
                                    scan_mem[sig].append(wfc)
                                else:
                                    new_sig2wfcs[sig].append(wfc)
                                    new_vectors += 1
                                arg_indx += 1
                            is_shift_done = True
                        elif post > 0:
                            new_sig2wfcs[sig].append(arg_sig2wfc[sig][arg_indx])
                            arg_indx += 1
                            post -= 1
                    else:
                        new_sig2wfcs[sig].append(wfcs[i])

        # Processing signals which have #, but not in the shift block        
        for sig in signals:
            
            if sig not in sig2wfcs:
                continue
            
            wfcs = sig2wfcs[sig]
            
            if sig in arg_sig2wfc and \
                sig not in signals_with_shift_hash and \
                sig in signals_with_hash:
                    
                new_sig2wfcs[sig] = []
                pre = 0
                if sig in pre_shift:
                    pre = pre_shift[sig]
                post = 0
                if sig in post_shift:
                    post = post_shift[sig]
                arg_indx = 0
                
                for i in range(len(wfcs)):
                    if wfcs[i] == '#':
                        if pre > 0:
                            new_sig2wfcs[sig].append(arg_sig2wfc[sig][arg_indx])
                            arg_indx += 1
                            pre -= 1
                        elif post > 0:
                            new_sig2wfcs[sig].append(arg_sig2wfc[sig][arg_indx])
                            arg_indx += 1
                            post -= 1
                    elif i == shift_pos:
                        for ii in range(max_scan_shift):
                            new_sig2wfcs[sig].append(wfcs[i])
                    else:
                        if wfcs[i] == '?':
                            if self.expanding_procs == False:
                                # Issue #13
                                err_msg = "COMPILER ERROR: Delta vector after # is not supported in none expanding procedure mode"
                                raise STILDumpCompilerException(-1, -1, err_msg)
                            else:
                                w = new_sig2wfcs[sig]
                                new_sig2wfcs[sig].append(w[-1])
                        else:
                            new_sig2wfcs[sig].append(wfcs[i])
                        
        max_wfc_len = 0
                        
        # Processing signal without #
        for sig in signals:
            
            if sig not in sig2wfcs:
                continue
            
            wfcs = sig2wfcs[sig]
            
            if sig not in signals_with_hash:

                if len(wfcs) > max_wfc_len:
                    max_wfc_len = len(wfcs)

                new_sig2wfcs[sig] = []
                for i in range(len(wfcs)):
                    if i == shift_pos:
                        r = wfcs[i]
                        if self.is_scan_mem_available:
                            new_sig2wfcs[sig].append(r)
                        else:
                            for ii in range(max_scan_shift):
                                new_sig2wfcs[sig].append(r)
                    else:
                        new_sig2wfcs[sig].append(wfcs[i])

        # Processing signals which have % 
        for sig in signals:
            
            if sig not in sig2wfcs:
                continue
            
            wfcs = new_sig2wfcs[sig]
            if "%" in wfcs:
                subs_wfc = arg_sig2wfc[sig]
                if len(subs_wfc) == 1:
                    wfcs = [wfc.replace('%', subs_wfc) for wfc in wfcs]
                    new_sig2wfcs[sig] = wfcs
                else:
                    err_msg = "COMPILER ERROR: Only 1 WFC expected for % substitution of the signal {sig} "
                    raise STILDumpCompilerException(-1, -1, err_msg)
        
        return new_sig2wfcs, scan_mem, new_vectors

    def dump_patt_stmt_block(
        self, sgd_patt2sig2WFCs, block2cmd, block_name, file_name, timing, sig_group_domain, macro_domain, proc_domain, is_pattern_block
    ):
        
        '''
        This function will "compile" the input block2cmd (which can be Pattern or Procedure block)
        into text file
        '''
        
        self.data = []

        self.scan_data = []
        
        # Collect WFC data from sgd_patt2sig2WFCs
        # sgd_patt2sig2WFCs can be either pattern or procedure block
        signals = []
        sep = []
        sgd_patt = DomainUtils.get_full_name(sig_group_domain, block_name)
        
        sig2patt_wfcs = {}
        
        if len(self.signals_order) > 0:
            signals = self.signals_order
            

        # It is posible to have pattern block without any vector,
        # for example : only calls to macros and procedures
        if len(sgd_patt2sig2WFCs) > 0:
            sig2patt_wfcs = sgd_patt2sig2WFCs[sgd_patt]
            
            # ToDo: add signals which are in the Condition stmt, but not in the
            # vectors
            # from sgd_patt2signals and sgd_patt_sig2defWFC
                    
            va_count = 0
            for sig in sig2patt_wfcs:
                if sig not in signals:
                    signals.append(sig)
                wfcs = sig2patt_wfcs[sig]
                va_count = len(wfcs)
                #print(f"sig {sig} {wfcs} va_count {va_count}\n")
                if len(self.data) == 0:
                    self.data = self.initial_fill_data(self.data, va_count)
                # Adding WFCs data for the current signal
                self.data.append(wfcs)
            self.data.append(sep)
        
        # Vector address in the case of expanding Macro or Procedure blocks
        exp_va = 0
        vamp = []
        vap = []
        vap_c = 0
        cmds = block2cmd[block_name]
        # Key is the signal name
        # Value is a list with scan chain memory filled with WFC
        block_scan_mem = {}
        
        proc_va = 0
        
        va_cmd = []
        
        last_start_loop_va = -1
        
        for vec_cmds in cmds:
            #print("\tNEW COMMAND\n")
            
            va_cmd.append(vec_cmds)
                                    
            for cmd in vec_cmds.get_cmd_ids():
                cmd_name = PattVecCmd.get_cmd_name(cmd)
                #print(f"\t\tCMD {cmd_name} | VALUE {vec_cmds.get_value(cmd)}\n")
                
                if cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_VECTOR]:
                    #print("vector cmd")
                    vamp.append("-")
                    vap.append(vap_c)
                    vap_c += 1
                    exp_va += 1 
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_WFT]:
                    pass
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_LABEL]:
                    va_cmd[-1].set_value(PattVecCmd.CMD_LABEL, vec_cmds.get_value(cmd))
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_LOAD_LOOP_COUNTER]:
                    pass
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_LOAD_MATCHLOOP_COUNTER]:
                    pass
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_LOOP]:
                    if last_start_loop_va != -1:
                        int_err_msg = "COMPILER ERROR : nested loop block detected"
                        raise STILDumpCompilerException(-1, -1, int_err_msg)
                    else:
                        last_start_loop_va = exp_va
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_LOOP]:
                    jmp = exp_va - last_start_loop_va - 1
                    va_cmd[-1].set_value(PattVecCmd.CMD_STOP_LOOP, jmp)
                    last_start_loop_va = -1
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_MATCHLOOP]:
                    value = vec_cmds.get_value(cmd)

                    if last_start_loop_va != -1:
                        int_err_msg = "COMPILER ERROR : nested loop block detected"
                        raise STILDumpCompilerException(-1, -1, int_err_msg)
                    else:
                        last_start_loop_va = exp_va

                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_COUNT_MATCHLOOP]:
                    jmp = exp_va - last_start_loop_va - 1
                    va_cmd[-1].set_value(PattVecCmd.CMD_STOP_COUNT_MATCHLOOP, jmp)
                    last_start_loop_va = -1
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_INF_MATCHLOOP]:
                    jmp = exp_va - last_start_loop_va - 1
                    va_cmd[-1].set_value(PattVecCmd.CMD_STOP_INF_MATCHLOOP, jmp)
                    last_start_loop_va = -1
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_IDDQTESTPOINT]:
                    pass
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_BREAKPOINT]:
                    pass
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_GOTO]:
                    pass
                    va_cmd[-1].set_value(PattVecCmd.CMD_GOTO, vec_cmds.get_value(cmd))
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP]:
                    pass
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_SHIFT]:
                    pass
                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_SHIFT]:
                    pass
                elif cmd_name ==  PattVecCmd.cmds[PattVecCmd.CMD_MACRO]:
                    # Macro blocks are always expanding into the pattern block

                    macro_va_length = 0

                    fmn = DomainUtils.get_full_name(macro_domain, vec_cmds.get_value(cmd))

                    sgd_macro = sig_group_domain + "::" + fmn
                    sig2macro_wfcs = self.sgd_macro2sig2WFCs[sgd_macro]

                    if len(signals) == 0:
                        for sig in sig2macro_wfcs:
                            if sig in self.sig2type:
                                signals.append(sig)

                    is_new_data_created = False
                    if len(sig2patt_wfcs) == 0:
                        for sig in signals:
                            if sig in sig2macro_wfcs:
                                wfcs = sig2macro_wfcs[sig]
                                va_count = len(wfcs)
                            else:
                                wfcs = list(sig2macro_wfcs.keys())[0]
                                va_count = len(wfcs)
                            if len(self.data) == 0:
                                self.data = self.initial_fill_data(self.data, va_count)
                                is_new_data_created = True
                            if is_new_data_created:
                                wfc = [] 
                                self.data.append(wfc)
                        if is_new_data_created:
                            self.data.append(sep)
                    
                    # WFC data substitution
                    if fmn in self.macro_for_subs:
                        arg_sig2wfc = vec_cmds.get_props(PattVecCmd.CMD_MACRO)
                        # TODO : to check STIL standard what should be done
                        if arg_sig2wfc != None:
                            hash_info = self.hashinfo[fmn]
                            cond_sig2wfc = None
                            if fmn in self.macro2first_cond:
                                cond_sig2wfc = self.macro2first_cond[fmn]
                            exp_sig2wfc, scan_mem, new_vectors = self.wfc_substitution(
                                                    hash_info, 
                                                    arg_sig2wfc, 
                                                    sig2macro_wfcs, 
                                                    signals, 
                                                    sig_group_domain,
                                                    cond_sig2wfc)

                            if self.is_scan_mem_available:
                                sd = {}
                                for sig in scan_mem:
                                    if sig not in block_scan_mem:
                                        block_scan_mem[sig] = []
                                    block_scan_mem[sig].extend(scan_mem[sig])
                                    scan_chain = ''
                                    for wfc in scan_mem[sig]:
                                        scan_chain += wfc
                                    if len(scan_chain) > 0:
                                        sd[sig] = scan_chain
                                if len(sd) > 0:
                                    self.scan_data.append(sd)
                            else:
                                pass
                            
                            is_first = True
                            sig_index = 6
                            exp = 0
                            for sig in signals:
                                if sig in sig2macro_wfcs:
                                    wfcs = sig2macro_wfcs[sig]
                                if sig in exp_sig2wfc:
                                    wfcs = exp_sig2wfc[sig]
                                    macro_va_length = len(wfcs)
                                    # adding WFC for the next signal
                                    self.data[sig_index][exp_va:exp_va] = wfcs
        
                                    if is_first:
                                        exp += macro_va_length
                                        is_first = False
                                else:
                                    # For signal not in the expansion, takes the latest WFC (issue #13)
                                    last_wfc = self.data[sig_index][-1]
                                    self.data[sig_index][exp_va:exp_va] = last_wfc
                                sig_index += 1
                                
                            shift_sig_wo_data = []
                            if len(scan_mem) == 0:
                                for sig in exp_sig2wfc:
                                    wfcs = exp_sig2wfc[sig]
                                    if len(wfcs) == 0:
                                        shift_sig_wo_data.append(sig)

                            if len(shift_sig_wo_data) > 0:
                                print("WARNING: The following signals in Shift block do not have data in the call of the macro:")
                                for s in shift_sig_wo_data:
                                    print(f"         {s}")
                                macro_va_length = 1

                                sig_index = 6
                                for sig in signals:
                                    if sig in shift_sig_wo_data:
                                        wfcs = self.data[sig_index]
                                        last_wfc = self.data[sig_index][-1]
                                        self.data[sig_index][exp_va:exp_va] = last_wfc
                                    sig_index += 1

                            exp_va += exp
                        else:
                            # Macro call without data, but with shift inside the macro
                            exp_va += 1
                            macro_va_length = 1

                            sig_index = 6
                            for sig in signals:
                                last_wfc = self.data[sig_index][-1]
                                self.data[sig_index][exp_va:exp_va] = last_wfc
                                sig_index += 1

                    else:
                        is_first = True
                        sig_index = 6
                        exp = 0
                        for sig in signals:
                            if sig in sig2macro_wfcs:
                                wfcs = sig2macro_wfcs[sig]
                                macro_va_length = len(wfcs)
                                # adding WFC for the next signal
                                self.data[sig_index][exp_va:exp_va] = wfcs
    
                                if is_first:
                                    exp += macro_va_length
                                    is_first = False
                            sig_index += 1
                        exp_va += exp
                            
                    # In the case when the last command does not have Vector statement
                    # like macro or procedure invocation we have to "transfer" the new command to the old command
                    add_to_last_cmd = False
                    last_cmd = va_cmd[-1]
                    if last_cmd.have_cmd(PattVecCmd.CMD_VECTOR) == False:
                        add_to_last_cmd = True
                        
                    macro_commands = self.macro2cmd[fmn]
                    last_start_loop_va = -1
                    m_va = 0
                    for macro_command in macro_commands:
                        if add_to_last_cmd:
                            cids = macro_command.get_cmd_ids()
                            for cid in cids: 
                                value = macro_command.get_value(cid)
                                last_cmd.add_cmd(cid, value)
                            add_to_last_cmd = False
                        else:
                            va_cmd.append(macro_command)
                            for cmd in macro_command.get_cmd_ids():
                                cmd_name = PattVecCmd.get_cmd_name(cmd)
                                if cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_WFT]:
                                    pass
                                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_LOOP]:
                                    last_start_loop_va = m_va
                                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_LOOP]:
                                    jmp = m_va - last_start_loop_va - 1
                                    va_cmd[-1].set_value(PattVecCmd.CMD_STOP_LOOP, jmp)
                                    last_start_loop_va = -1
                                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_MATCHLOOP]:
                                    last_start_loop_va = m_va
                                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_COUNT_MATCHLOOP]:
                                    jmp = m_va - last_start_loop_va - 1
                                    va_cmd[-1].set_value(PattVecCmd.CMD_STOP_COUNT_MATCHLOOP, jmp)
                                    last_start_loop_va = -1
                                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_INF_MATCHLOOP]:
                                    jmp = m_va - last_start_loop_va - 1
                                    va_cmd[-1].set_value(PattVecCmd.CMD_STOP_INF_MATCHLOOP, jmp)
                                    last_start_loop_va = -1
                                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_GOTO]:
                                    va_cmd[-1].set_value(PattVecCmd.CMD_GOTO, macro_command.get_value(cmd))
                                elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_LABEL]:
                                    va_cmd[-1].set_value(PattVecCmd.CMD_LABEL, macro_command.get_value(cmd))
                            m_va += 1
                            
                    for i in range(macro_va_length):
                        vap.append("-")
                        vamp.append(i)

                elif cmd_name ==  PattVecCmd.cmds[PattVecCmd.CMD_CALL]:

                    proc_va_length = 0

                    fpn = DomainUtils.get_full_name(proc_domain, vec_cmds.get_value(cmd))

                    if self.expanding_procs:
                        
                        sgd_proc = sig_group_domain + "::" + fpn
                        sig2proc_wfcs = self.sgd_proc2sig2WFCs[sgd_proc]

                        if len(signals) == 0:
                            for sig in sig2proc_wfcs:
                                if sig in self.sig2type:
                                    signals.append(sig)

                        is_new_data_created = False
                        if len(sig2patt_wfcs) == 0:
                            for sig in signals:
                                if sig in sig2proc_wfcs:
                                    wfcs = sig2proc_wfcs[sig]
                                    va_count = len(wfcs)
                                else:
                                    wfcs = list(sig2proc_wfcs.keys())[0]
                                    va_count = len(wfcs)
                                if len(self.data) == 0:
                                    self.data = self.initial_fill_data(self.data, va_count)
                                    is_new_data_created = True
                                if is_new_data_created:
                                    wfc = [] 
                                    self.data.append(wfc)
                            if is_new_data_created:
                                self.data.append(sep)
                        
                        # WFC data substitution
                        is_wfc_subs = False
                        scan_len = 0
                        if fpn in self.proc_for_subs:
                            arg_sig2wfc = vec_cmds.get_props(PattVecCmd.CMD_CALL)
                            # TODO : to check STIL standard what should be done
                            if arg_sig2wfc != None:
                                hash_info = self.hashinfo[fpn]
                                cond_sig2wfc = None
                                if fpn in self.proc2first_cond:
                                    cond_sig2wfc = self.proc2first_cond[fpn]
                                exp_sig2wfc, scan_mem, new_vectors = self.wfc_substitution(
                                                        hash_info, 
                                                        arg_sig2wfc, 
                                                        sig2proc_wfcs, 
                                                        signals, 
                                                        sig_group_domain,
                                                        cond_sig2wfc)

                                if self.is_scan_mem_available:
                                    sd = {}
                                    for sig in scan_mem:
                                        if sig not in block_scan_mem:
                                            block_scan_mem[sig] = []
                                        block_scan_mem[sig].extend(scan_mem[sig])
                                        scan_chain = ''
                                        for wfc in scan_mem[sig]:
                                            scan_chain += wfc
                                        if len(scan_chain) > 0:
                                            sd[sig] = scan_chain
                                    if len(sd) > 0:
                                        self.scan_data.append(sd)
                                else:
                                    is_wfc_subs = True
                                
                                is_first = True
                                sig_index = 6
                                exp = 0
                                for sig in signals:
                                    if sig in sig2proc_wfcs:
                                        wfcs = sig2proc_wfcs[sig]
                                    if sig in exp_sig2wfc:
                                        wfcs = exp_sig2wfc[sig]
                                        proc_va_length = len(wfcs)
                                        # adding WFC for the next signal
                                        self.data[sig_index][exp_va:exp_va] = wfcs
            
                                        if is_first:
                                            exp += proc_va_length
                                            scan_len = len(wfcs)
                                            is_first = False
                                    else:
                                        # For signal not in the expansion, takes the latest WFC (issue #13)
                                        last_wfc = self.data[sig_index][-1]
                                        self.data[sig_index][exp_va:exp_va] = last_wfc
                                    sig_index += 1

                                shift_sig_wo_data = []
                                if len(scan_mem) == 0:
                                    for sig in exp_sig2wfc:
                                        wfcs = exp_sig2wfc[sig]
                                        if len(wfcs) == 0:
                                            shift_sig_wo_data.append(sig)
    
                                if len(shift_sig_wo_data) > 0:
                                    print("WARNING: The following signals in Shift block do not have data in the call of the procedure:")
                                    for s in shift_sig_wo_data:
                                        print(f"         {s}")
                                    proc_va_length = 1

                                    sig_index = 6
                                    for sig in signals:
                                        if sig in shift_sig_wo_data:
                                            wfcs = self.data[sig_index]
                                            last_wfc = self.data[sig_index][-1]
                                            self.data[sig_index][exp_va:exp_va] = last_wfc
                                        sig_index += 1

                                exp_va += exp
                            else:
                                # Procedure call without data, but with shift inside the procedure
                                exp_va += 1
                                proc_va_length = 1

                                sig_index = 6
                                for sig in signals:
                                    last_wfc = self.data[sig_index][-1]
                                    self.data[sig_index][exp_va:exp_va] = last_wfc
                                    sig_index += 1
                                                                
                        else:
                            is_first = True
                            sig_index = 6
                            exp = 0
                            for sig in signals:
                                if sig in sig2proc_wfcs:
                                    wfcs = sig2proc_wfcs[sig]
                                    proc_va_length = len(wfcs)
                                    # adding WFC for the next signal
                                    self.data[sig_index][exp_va:exp_va] = wfcs
        
                                    if is_first:
                                        exp += proc_va_length
                                        is_first = False
                                sig_index += 1
                            exp_va += exp


                        # In the case when the last command does not have Vector statement
                        # like macro or procedure invocation we have to "transfer" the new command to the old command
                        add_to_last_cmd = False
                        last_cmd = va_cmd[-1]
                        if last_cmd.have_cmd(PattVecCmd.CMD_VECTOR) == False:
                            add_to_last_cmd = True
                                
                        proc_commands = self.proc2cmd[fpn]
                        last_start_loop_va = -1
                        m_va = 0
                        for proc_command in proc_commands:
                            if add_to_last_cmd:
                                cids = proc_command.get_cmd_ids()
                                for cid in cids: 
                                    value = proc_command.get_value(cid)
                                    last_cmd.add_cmd(cid, value)
                                add_to_last_cmd = False
                            else:
                                va_cmd.append(proc_command)

                                is_shift_start = False
                                is_shift_stop = False

                                for cmd in proc_command.get_cmd_ids():
                                    cmd_name = PattVecCmd.get_cmd_name(cmd)
                                    if cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_LOOP]:
                                        last_start_loop_va = m_va
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_SHIFT]:
                                        is_shift_start = True
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_SHIFT]:
                                        is_shift_stop = True
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_LOOP]:
                                        jmp = m_va - last_start_loop_va - 1
                                        va_cmd[-1].set_value(PattVecCmd.CMD_STOP_LOOP, jmp)
                                        last_start_loop_va = -1
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_START_MATCHLOOP]:
                                        last_start_loop_va = m_va
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_COUNT_MATCHLOOP]:
                                        jmp = m_va - last_start_loop_va - 1
                                        va_cmd[-1].set_value(PattVecCmd.CMD_STOP_COUNT_MATCHLOOP, jmp)
                                        last_start_loop_va = -1
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_STOP_INF_MATCHLOOP]:
                                        jmp = m_va - last_start_loop_va - 1
                                        va_cmd[-1].set_value(PattVecCmd.CMD_STOP_INF_MATCHLOOP, jmp)
                                        last_start_loop_va = -1
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_GOTO]:
                                        va_cmd[-1].set_value(PattVecCmd.CMD_GOTO, proc_command.get_value(cmd))
                                    elif cmd_name == PattVecCmd.cmds[PattVecCmd.CMD_LABEL]:
                                        va_cmd[-1].set_value(PattVecCmd.CMD_LABEL, proc_command.get_value(cmd))

                                if is_shift_start and is_shift_stop:
                                    if is_wfc_subs:
                                        for i in range(new_vectors-1):
                                            cmd = PattVecCmd()
                                            cmd.add_cmd(PattVecCmd.CMD_VECTOR)
                                            va_cmd.append(cmd)
                                elif is_shift_start or is_shift_stop:
                                    int_err_msg = "INTERNAL COMPILER ERROR : Shift block with more of one vector is not yet supported!"
                                    raise STILDumpCompilerException(-1, -1, int_err_msg)


                                m_va += 1

                        for i in range(proc_va_length):
                            vap.append("-")
                            vamp.append(i)
                            
        
        self.data.append(va_cmd)
        
        if len(va_cmd) != exp_va:
            int_err_msg = f"INTERNAL COMPILER ERROR : total vector addresses ({exp_va}) does not match with number of commands ({len(va_cmd)})"
            raise STILDumpCompilerException(-1, -1, int_err_msg)
        if len(vap) != exp_va:
            int_err_msg = f"INTERNAL COMPILER ERROR : total vector addresses ({exp_va}) does not match pattern VA ({len(vap)})"
            raise STILDumpCompilerException(-1, -1, int_err_msg)
        if len(vamp) != exp_va:
            int_err_msg = f"INTERNAL COMPILER ERROR : total vector addresses ({exp_va}) does not match proc/macro VA ({len(vamp)})"
            raise STILDumpCompilerException(-1, -1, int_err_msg)
        
            
        # If there are commands which expands VA like Macro,
        # we have to update the vector address columns as well
        if exp_va > 0:
                        
            #print(f"data {data}")
            self.data[0] = []
            self.data[0] = range(exp_va)
    
            new_sep = ['|']*(exp_va)
            self.data[1] = []
            self.data[1] = new_sep
    
            self.data[2] = []
            self.data[2] = vap
    
            self.data[3] = []
            self.data[3] = new_sep
    
            self.data[4] = []
            self.data[4] = vamp
    
            self.data[5] = []
            self.data[5] = new_sep
    
            self.data[6+len(signals)] = []
            self.data[6+len(signals)] = new_sep
            
        if self.dump_data:
            self.dump_pattern_data(file_name, 
                                   signals, 
                                   block_name, 
                                   timing, 
                                   sig_group_domain, 
                                   macro_domain, 
                                   proc_domain, 
                                   exp_va, 
                                   block_scan_mem)
        elif is_pattern_block:
            # "compile mode", implement your code to compile self.data into 
            # specific FW/FPGA commands and data
            self.compile_data(  signals, 
                                timing, 
                                block_scan_mem)

        va_size = len(list(self.data[0]))

        if is_pattern_block:
            return va_size, proc_va
        else:
            return va_size

    def compile_data(self, signals, timing, block_scan_mem):
        '''
        Empty function for compilation self.data into your specific FW/FPGA commands and data

        Parameters
        ----------
        signals : list
            List of signal names.
        timing : string
            Time domain name.
        block_scan_mem : map
            Key is the signal name
            Value is a list with scan chain memory filled with WFC.

        Returns
        -------
        None.

        
        self.data contains list of lists with :
        [0]     VA - list with vector addresses
        [1]     | separator 
        [2]     VAP - list with pattern only vector addresses
        [3]     | separator 
        [4]     VAMP -list with macro/proc only vector addresses
        [5]     | separator 
        [6+X-1]   For every used signal (total X signals), separate list with own WFCs
        [6+X]   | separator 
        [6+X+1] PattVecCmd for every vector.
        '''
        pass

    def dump_pattern_data(self, file_name, signals, block_name, timing, sig_group_domain, macro_domain, proc_domain, exp_va, block_scan_mem):
        
        file = os.path.join(self.out_folder, file_name)
        f = open(file, "w")

        # start the dump:
        # Write first description:
        f.write(f"# Block name  : {block_name}\n\n")
        f.write( "# Domain info:\n")
        f.write(f"# - Timing domain       : {timing}\n")
        f.write(f"# - SignalsGroup domain : {sig_group_domain}\n")
        f.write(f"# - MacroDefs domain    : {macro_domain}\n")
        f.write(f"# - Procedures domain   : {proc_domain}\n\n")

        f.write("# Format of compiled data :\n")
        f.write("# VA|VAP|VAMP|WFC|CMD|CMD arg| .... |CMD|CMD arg \n\n")

        
        f.write( "# Vector data information :\n")
        f.write( "# VA   - absolute vector address for this particular pattern block. \n\
        This address can be used also as relative vector address when all \n\
        pattern blocks are assembled into the memory.\n")
        f.write( "# VAP  - absolute vector address in the pattern block if there is no \n\
        Macro or expanding Procedure invocation in this pattern block.\n\
        Value '-' indicates that there is WFC/CMD data from Macro/Procdure at this VA\n")
        f.write( "# VAMP - absolute vector address of the Macro or expanded Procedure block.\n\
        Value '-' indicates that there is no WFC/CMD data from Macro/Procdure at this VA\n\n")

        f.write( "# Commands syntax:\n")
        f.write( "# COMMAND_NAME=value_if_applicable\n")
        f.write( "# If more than one command exists on the same vector address, they are separated with | \n\n")

        f.write("# SIGNALS_ORDER|")
        s = ""
        si = 0
        err_msg = ""
        raise_int_err = False
        for signal in signals:
            s += signal + "+"
            wfc_len = len(self.data[si+6])
            if wfc_len != exp_va:
                err_msg += f"INTERNAL COMPILER ERROR : total vector addresses ({exp_va}) does not match WFC length ({wfc_len}) of the signal {signal}\n"
                raise_int_err = True
            si += 1
        f.write(f"{s[:-1]}")
        f.write("|\n\n")
        
        if raise_int_err:
            raise STILDumpCompilerException(-1, -1, err_msg)

        """
         Finally dump all data like in text version of "memory map"
         Transponse VA, WFC and commands data from columns (lists) to rows: 
         VA ->         [  0,     1,     2  ...,  N]
         WFC -> sig1 = [ "L",   "H",   "H" ..., "X"]
         WFC -> sig2 = [ "0",   "1",   "1" ..., "Z"]
         CMD -> cmd  = [ "W" , "SL|5",  "" ..., "L|label1" ]
         after transponse:
         
         0|L0|W
         1|H1|SL|5
         2|H1|
         .....
         N|XZ|L|label1
         
         For large STIL file, avoid using numpy.transpose() method. 
         It use a huge amount of RAM and in result is very slow:
         mem_map = list(map(list, np.transpose(data)))
         for va in mem_map:
             for mem_data in va:
                 f.write(f"{mem_data}")
             f.write("\n")         
        """        
        f.write("# VA| VAP|VAMP|  WFCs  |CMD ... \n")
        va_size = len(list(self.data[0]))
        for va in range(va_size):
            s =""
            c = 0
            for column in self.data:
                if len(column) > 0:
                    if c == 0 or c == 2 or c == 4:
                        s += str(column[va]).rjust(4)
                    elif c == 6:
                        s += str(column[va]).rjust(6)
                    else:
                        s += str(column[va])
                c += 1
                if c > (6+si+1):
                    break
            s += "\n"
            f.write(s)
        f.close()

        if self.is_scan_mem_available:
            scan_mem_file = file_name + ".sm"
            file = os.path.join(self.out_folder, scan_mem_file)
            f = open(file, "w")

            # write header before the data
            f.write("# SIGNAL_NAME | WFC sequence for the scan memory\n")

            for sig in block_scan_mem:
                f.write(sig)
                f.write("|")
                wfcs = block_scan_mem[sig]
                for wfc in wfcs:
                    f.write(wfc)
                f.write("\n")
                    
            f.close()
    
    def collect_wfc_for_signals(self, s2w, sgds, block_name, sig_order, wfc_order):

        # For each signal group domain used by macro/proc/pattern block
        for sgd in sgds:

            last_sig2wfc = None
            if sgd in self.sgd2last_sig2wfc:
                last_sig2wfc = self.sgd2last_sig2wfc[sgd]

            sig2wfc_before_subs = None
            if sgd not in self.sgd2before_subs_sig2wfc:
                self.sgd2before_subs_sig2wfc[sgd] = {}
            sig2wfc_before_subs = self.sgd2before_subs_sig2wfc[sgd]

            sig2wfc = WFCUtils.collect_sig2wfc(self.sig2type.keys(),
                                               sgd,
                                               self.signal_groups2signals,
                                               sig_order,
                                               wfc_order,
                                               last_sig2wfc,
                                               sig2wfc_before_subs)

            self.sgd2last_sig2wfc[sgd] = sig2wfc

            sgd_block = sgd + "::" + block_name
            if sgd_block not in s2w:
                s2w[sgd_block] = {}
            
            if self.is_first_vector and self.is_vector_stmt:
                s2w[sgd_block] = sig2wfc
            else:
                old_sig2wfc = s2w[sgd_block]
                for sig in sig2wfc:
                    wfc = sig2wfc[sig]
                    if sig not in old_sig2wfc:
                        old_sig2wfc[sig] = wfc
                    else:
                        old_sig2wfc[sig] += wfc

    
    def b_macrodefs__pattern_statements__close_vector_block(self, t):

        if self.is_vector_stmt:
            self.save_cmd_macro()

        sgds = self.macro2signal_group_domains[self.curr_macro_name]
        
        self.collect_wfc_for_signals(self.sgd_macro2sig2WFCs,
                                     sgds,
                                     self.curr_macro_name,
                                     self.curr_macro_sig_order,
                                     self.curr_macro_wfc_order
                                     )

        super().b_macrodefs__pattern_statements__close_vector_block(t)

    def b_procedures__pattern_statements__close_vector_block(self, t):

        if self.is_vector_stmt:
            self.save_cmd_proc()

        sgds = self.proc2signal_group_domains[self.curr_proc_name]

        self.collect_wfc_for_signals(self.sgd_proc2sig2WFCs,
                                     sgds,
                                     self.curr_proc_name,
                                     self.curr_proc_sig_order,
                                     self.curr_proc_wfc_order
                                     )

        
        super().b_procedures__pattern_statements__close_vector_block(t)

    def dump_timing_data(self):
        
        if self.dump_data:
            timing_file = os.path.join(self.out_folder, "timing.txt")
            with open(timing_file, "w") as f:
                f.write("# Format of timing data :\n")
                f.write("# Timing domain name | WFT name | Signal name | WFC | WFE : Time .... \n")
                for sig_wft in self.sig_wft2timing:
                    data = sig_wft.split("::")
                    t_domain = DomainUtils.get_domain(data[0], True)

                    sti = self.sig_wft2timing[sig_wft]
                    wfcs = sti.get_wfcs()
                    for wfc in wfcs:
                        timing = sti.get_timing_for_wfc(wfc)
                        f.write(f"{t_domain} | {data[1]} | {data[2]} | {wfc} | ")
                        for wfe_time in timing:
                            wfe = wfe_time[0]
                            time = wfe_time[1]
                            f.write(f"{wfe}:{time} | ")
                        f.write("\n")

    def assamble_all(self):
        # not implemented yet
        pass

    def calculate_test_cycles(self):

        if self.is_parsing_done == False:
            return

        # Number of test cycles
        # test cycles != vector addresses!!!
        tc = 0

        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():

            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:

                pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]
                proc_domain = self.patt_burst2proc_domain[patt_burst]
                macro_domain = self.patt_burst2macro_domain[patt_burst]
                sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]

                # For every pattern block in the pattern burst block
                for patt in pattern_list:

                    start_loop_va = 0
                    loop_count = 0

                    cmds_list = self.patt2cmd[patt]

                    for vec_cmds in cmds_list:
                        for cmd in vec_cmds.get_cmd_ids():
                            pm_name = ""
                            if (cmd == PattVecCmd.CMD_CALL) or (cmd == PattVecCmd.CMD_MACRO):
                                pm_name = vec_cmds.get_value(cmd)
                            props = vec_cmds.get_props(cmd)
                            sig2wfc_count = {}
                            if props is not None:
                                for key, value in props.items():
                                    if (
                                        cmd == PattVecCmd.CMD_CALL
                                        or cmd == PattVecCmd.CMD_MACRO
                                    ):
                                        sig2wfc_count[key] = len(value)
                            if cmd == PattVecCmd.CMD_VECTOR:
                                tc += 1
                            elif (
                                cmd == PattVecCmd.CMD_START_LOOP
                                or cmd == PattVecCmd.CMD_START_MATCHLOOP
                            ):
                                start_loop_va = tc
                                if vec_cmds.get_value(cmd) == "Infinite":
                                    loop_count = -1
                            elif (
                                cmd == PattVecCmd.CMD_LOAD_LOOP_COUNTER
                                or cmd == PattVecCmd.CMD_LOAD_MATCHLOOP_COUNTER
                            ):
                                loop_count = int(vec_cmds.get_value(cmd))
                            elif (
                                cmd == PattVecCmd.CMD_STOP_LOOP
                                or cmd == PattVecCmd.CMD_STOP_COUNT_MATCHLOOP
                            ):
                                if loop_count > 0:
                                    tc += (tc - start_loop_va + 1) * (loop_count - 1)
                                start_loop_va = 0

                            elif cmd == PattVecCmd.CMD_CALL:

                                proc_name = pm_name

                                pfn = DomainUtils.get_full_name(proc_domain, proc_name)

                                tc += self.proc2tc[pfn]

                                if pfn in self.proc_with_shift:

                                    max_va = 0

                                    for sig in sig2wfc_count:

                                        wfc_c = sig2wfc_count[sig]
                                        his = self.hashinfo[pfn]
                                        hash_not_in_shift = 0

                                        for hi in his:
                                            if hi.sig_ref in self.sig2type:
                                                if hi.pos_rel_shift != 1:
                                                    hash_not_in_shift += 1
                                            else:
                                                sg = (
                                                    sig_group_domain + "::" + hi.sig_ref
                                                )
                                                sig_gr = self.signal_groups2signals[sg]
                                                if sig in sig_gr:
                                                    if hi.pos_rel_shift != 1:
                                                        hash_not_in_shift += 1
                                        # number of WFC argument - # not in shift - shift Vector
                                        va_shift = wfc_c - hash_not_in_shift - 1
                                        if max_va == 0:
                                            max_va = va_shift
                                        elif va_shift > max_va:
                                            max_va = va_shift
                                    tc += max_va

                            elif cmd == PattVecCmd.CMD_MACRO:

                                macro_name = pm_name
                                mfn = DomainUtils.get_full_name(
                                    macro_domain, macro_name
                                )
                                tc += self.macro2tc[mfn]
                                if mfn in self.macro_with_shift:
                                    max_va = 0
                                    for sig in sig2wfc_count:

                                        wfc_c = sig2wfc_count[sig]
                                        his = self.hashinfo[mfn]
                                        hash_not_in_shift = 0

                                        for hi in his:
                                            if hi.sig_ref in self.sig2type:
                                                pass
                                            else:
                                                sg = (
                                                    sig_group_domain + "::" + hi.sig_ref
                                                )
                                                sig_gr = self.signal_groups2signals[sg]
                                                if sig in sig_gr:
                                                    if hi.pos_rel_shift != 1:
                                                        hash_not_in_shift += 1
                                        # number of WFC argument - # not in shift - shift Vector
                                        va_shift = wfc_c - hash_not_in_shift - 1
                                        if max_va == 0:
                                            max_va = va_shift
                                        elif va_shift > max_va:
                                            max_va = va_shift
                                    tc += max_va

        print(f"\nTest cycles = {tc}\n")
