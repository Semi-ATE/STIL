# -*- coding: utf-8 -*-


class PattVecCmd:
    
    '''
    Contains pattern statements information for one vector address.
    On one vector address is possible to have multiple pattern statements.
    Like Label + Vector or WaveformTable + Vector ...
    The order of commands is not perserved. 
    '''

    CMD_NONE = 0
    CMD_LABEL = 1
    CMD_WFT = 2
    CMD_LOAD_LOOP_COUNTER = 3
    CMD_LOAD_MATCHLOOP_COUNTER = 4
    CMD_START_LOOP = 5
    CMD_START_MATCHLOOP = 6
    CMD_VECTOR = 7
    CMD_GOTO = 8
    CMD_BREAKPOINT = 9
    CMD_IDDQTESTPOINT = 10
    CMD_STOP = 11
    CMD_START_SHIFT = 12
    CMD_STOP_SHIFT = 13
    CMD_STOP_LOOP = 14
    CMD_STOP_MATCHLOOP = 15
    CMD_MACRO = 16
    CMD_CALL = 17

    cmds = {
        0: "NO CMD",
        1: "LABEL",
        2: "WFT",
        3: "LOAD_LOOP_COUNTER",
        4: "LOAD_MATCHLOOP_COUNTER",
        5: "START_LOOP",
        6: "START_MATCHLOOP",
        7: "VECTOR",
        8: "GOTO",
        9: "BREAKPOINT",
        10: "IDDQTESTPOINT",
        11: "STOP",
        12: "START_SHIFT",
        13: "STOP_SHIFT",
        14: "STOP_LOOP",
        15: "STOP_MATCHLOOP",
        16: "MACRO",
        17: "CALL",
    }

    def __init__(self, debug=False):

        self.debug = debug
        self.cmd = 0
        # Key is the command number
        # Value is the command's value
        self.cmd_value = {}
        # Key is the command number
        # Value is dict with the command property's key and value
        self.cmd_prop = {}

    def add_cmd(self, cmd, value=None):
        self.cmd |= 1 << cmd
        if value is not None:
            self.set_value(cmd, value)

    def del_cmd(self, cmd):

        if cmd in self.cmd_value:
            self.cmd_value[cmd] = None
        self.cmd &= ~(1 << cmd)

    def get_cmd_name(cmd_id):
        return PattVecCmd.cmds[cmd_id]

    def have_cmd(self, cmd_id):
        found = False
        cmds = []
        for bit in range(len(PattVecCmd.cmds)):
            if ((self.cmd >> bit) & 0x1) == 0x1:
                if cmd_id == bit:
                    found = True
                    break
        return found

    def get_cmd_ids(self):
        cmds = []
        for bit in range(len(PattVecCmd.cmds)):
            if ((self.cmd >> bit) & 0x1) == 0x1:
                cmds.append(bit)
        return cmds

    def set_value(self, cmd, value):
        self.cmd_value[cmd] = value

    def get_value(self, cmd_id):
        if cmd_id in self.cmd_value:
            return self.cmd_value[cmd_id]

    def add_prop(self, cmd, prop_name, prop_value):
        #print(f"add prop for cmd {PattVecCmd.get_cmd_name(cmd)}")
        if cmd in self.cmd_prop:
            d = self.cmd_prop[cmd]
            d[prop_name] = prop_value
            #print(f"{d}")
        else:
            #print("add new cmd for prop")
            self.cmd_prop[cmd] = {}
            d = self.cmd_prop[cmd]
            d[prop_name] = prop_value
            #print(f"{d}")

    def get_props(self, cmd_id):
        #cmd_name = PattVecCmd.get_cmd_name(cmd_id)
        #print(f"get_props for cmd {cmd_name}")
        if cmd_id in self.cmd_prop:
            return self.cmd_prop[cmd_id]
        
    def __str__(self):
        msg = ""
        new_line = "\n"
        cmds = self.get_cmd_ids()
        for cmd in cmds:
            value = self.get_value(cmd)
            msg += f"cmd {PattVecCmd.get_cmd_name(cmd)} value {value} "
            msg += new_line
        return msg
