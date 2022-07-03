# -*- coding: utf-8 -*-
import inspect


class STILBlockParser:
    def __init__(self, debug=False):
        self.debug = debug
        self.extensions = {}
        self.last_extension = ""

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_stil__STIL_VERSION(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if t != "1.0":
            err_msg = "Not supported STIL file format : "
            err_msg += "expected 1.0, but the value is " + t
            raise Exception(err_msg)

    def b_stil__open_stil_extension(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_stil__STIL_EXTENSION_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.last_extension = t

    def b_stil__STIL_EXTENSION_YEAR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if self.last_extension == "Design" and t != "2005":
            err_msg = "Not supported STIL extension year : "
            err_msg += "expected 2005, but the value is " + t
            raise Exception(err_msg)
        elif self.last_extension == "DCLevels" and t != "2002":
            err_msg = "Not supported STIL extension year : "
            err_msg += "expected 2002, but the value is " + t
            raise Exception(err_msg)
        else:
            self.extensions[self.last_extension] = t

    def b_stil__CLOSE_STIL_EXTENSION(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
