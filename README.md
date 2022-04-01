# STIL

Standard Tester Interface Language [IEEE1450]

[![CI](https://github.com/Semi-ATE/STIL/workflows/CI/badge.svg?branch=main)](https://github.com/Semi-ATE/STIL/actions?query=workflow%3ACI)
[![CD](https://github.com/Semi-ATE/STIL/workflows/CD/badge.svg)](https://github.com/Semi-ATE/STIL/actions?query=workflow%3ACD)

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Semi-ATE/STIL?color=blue&label=GitHub&sort=semver)](https://github.com/Semi-ATE/STIL/releases/latest)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/Semi-ATE/STIL/latest)](https://github.com/Semi-ATE/STIL)
[![PyPI](https://img.shields.io/pypi/v/Semi-ATE-STIL?color=blue&label=PyPI)](https://pypi.org/project/Semi-ATE-STIL/)

[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/Semi-ATE-STIL?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/semi-ate-stil)
[![conda-forge feedstock](https://img.shields.io/github/issues-pr/conda-forge/Semi-ATE-STIL-feedstock?label=feedstock)](https://github.com/conda-forge/Semi-ATE-STIL-feedstock)

[![GitHub issues](https://img.shields.io/github/issues/Semi-ATE/STIL)](https://github.com/Semi-ATE/STIL/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Semi-ATE/STIL)](https://github.com/Semi-ATE/STIL/pulls)

[![codecov](https://codecov.io/gh/Semi-ATE/STIL/branch/main/graph/badge.svg?token=BAP0H9OMED)](https://codecov.io/gh/Semi-ATE/STIL)
![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/semi-ate-stil.svg?color=brightgreen)

This repository contains STIL parser and dump compiler written in Python using Lark parser library and Language Server Protocol (LSP) for integration into IDE.
The work is in progress and the parser is not yet ready to be used in production environment.


# Usage examples


## Use syntax and semantic parsers to find out errors in the input STIL file:  

```python
from Semi_ATE.STIL.parsers.STILParser import STILParser

stil_file = "PATH_TO_STIL_FILE"
parser = STILParser(stil_file)
parser.parse_syntax()
parser.parse_semantic()
if parser.err_line == -1:
  print("No errors are found during STIL file parsing")
else:
  print("Found error during STIL file parsing")
```

## Use a dump compiler to understand how to make a own compiler.
The dump compiler will save content of the STIL file into one or more text files.
The files contain WFC data for signals, commands etc.
The compiler can expand the procedures and shift statements if needed.
For detail information, read the intro text of the Semi_ATE.STIL.parsers.STILDumpCompiler

```python
from Semi_ATE.STIL.parsers.STILDumpCompiler import STILDumpCompiler

stil_file = "PATH_TO_STIL_FILE"
out_folder = "PATH_TO_OUTPUT_FOLDER"

compiler = STILDumpCompiler(
    stil_file, expanding_procs=True, is_scan_mem_available=True, out_folder = out_folder
)
compiler.compile()

```
