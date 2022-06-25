# -*- coding: utf-8 -*-
import inspect

from lark import Transformer

from . import STILBlockParser
from . import HeaderBlockParser
from . import SignalsBlockParser
from . import SignalGroupsBlockParser
from . import TimingBlockParser
from . import ScanStructBlockParser
from . import SelectorBlockParser
from . import SpecBlockParser
from . import MacroDefsBlockParser
from . import ProceduresBlockParser
from . import PatternBurstBlockParser
from . import PatternBlockParser
from . import PatternExecBlockParser


class STILLark(
    Transformer,
    STILBlockParser,
    HeaderBlockParser,
    SignalsBlockParser,
    SignalGroupsBlockParser,
    TimingBlockParser,
    ScanStructBlockParser,
    SpecBlockParser,
    SelectorBlockParser,
    MacroDefsBlockParser,
    ProceduresBlockParser,
    PatternBurstBlockParser,
    PatternExecBlockParser,
    PatternBlockParser,
):
    def __init__(self, stil_file, debug=False):

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
        Nothing

        """
        self.debug = debug
        self.stil_file = stil_file
        self.total_va = 0
        self.user_defined_keywords = set()

        STILBlockParser.__init__(self, debug)
        HeaderBlockParser.__init__(self, debug)
        SignalsBlockParser.__init__(self, debug)
        SignalGroupsBlockParser.__init__(self, debug)
        TimingBlockParser.__init__(self, debug)
        ScanStructBlockParser.__init__(self, debug)
        SelectorBlockParser.__init__(self, debug)
        SpecBlockParser.__init__(self, debug)
        MacroDefsBlockParser.__init__(self, debug)
        ProceduresBlockParser.__init__(self, debug)
        PatternBurstBlockParser.__init__(self, debug)
        PatternExecBlockParser.__init__(self, debug)
        PatternBlockParser.__init__(self, debug)

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def USER_KEYWORDS(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.user_defined_keywords.add(t.value)
            
    def eof(self):
        # end of the file
        PatternBlockParser.eof(self)
