# STIL

Standard Tester Interface Language [IEEE1450]

[![CI](https://github.com/Semi-ATE/STIL/workflows/CI/badge.svg?branch=main)](https://github.com/Semi-ATE/STIL/actions?query=workflow%3ACI)
[![CD](https://github.com/Semi-ATE/STIL/workflows/CD/badge.svg)](https://github.com/Semi-ATE/STIL/actions?query=workflow%3ACD)

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Semi-ATE/STIL?color=blue&label=GitHub&sort=semver)](https://github.com/Semi-ATE/STIL/releases/latest)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/Semi-ATE/STIL/latest)](https://github.com/Semi-ATE/STIL)
[![PyPI](https://img.shields.io/pypi/v/Semi-ATE-STIL?color=blue&label=PyPI)](https://pypi.org/project/Semi-ATE-STIL/)


[![GitHub issues](https://img.shields.io/github/issues/Semi-ATE/STIL)](https://github.com/Semi-ATE/STIL/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Semi-ATE/STIL)](https://github.com/Semi-ATE/STIL/pulls)

This repository contains STIL parser written in Python using Lark parser library and Language Server Protocol (LSP) for integration into IDE.
The work is in progress and the parser is not yet ready to be used in production environment.


# Usage examples


## Use syntax and semantic parsers to find out errors in the input STIL file:  

```python
from Semi_ATE.STIL.parsers.STILParser import STILParser

stil_file = "PATH_TO_STIL_FILE"
parser = STILParser()
tree = parser.parse_syntax(stil_file)
if tree != None:
  parser.parse_semantic(tree, stil_file)
if parser.err_msg == None:
  print("No errors are found during STIL file parsing")
else:
  print("Found error during STIL file parsing")

```
