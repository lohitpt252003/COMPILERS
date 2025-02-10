# COMPILERS

**Members**
LOHIT P TALAVAR 210564



**Milestone 1**
# token.py
"""
This module implements the tokenizer for CHIRONLANG.
It converts a CHIRONLANG source string into a list of tokens.
Each token stores:
  - type (e.g., NUMBER, IDENT, KEYWORD, SYMBOL, UNKNOWN)
  - value (the string form of the token)
  - line and column (starting position in the source)

The keywords (per the document) are:
    if, else, repeat, penup, pendown, forward, backward,
    left, right, go, true, false, input

Variables are expected to start with a colon (":").
Operators such as ==, !=, <=, >=, &&, ∥ (or ||) are supported.
"""



# ast.py
"""
This module defines the Abstract Syntax Tree (AST) node classes for CHIRONLANG.
Each AST node stores its location (line and column) where applicable, so that
debugging and error reporting can later use this information.

The AST covers the following constructs:
  - Program: a sequence of statements.
  - Assignment: variable = expression.
  - IfStatement: with optional else clause.
  - RepeatStatement: loop structure.
  - PenStatement: penup or pendown.
  - MoveStatement: forward, backward, left, right, or go.
  - BinaryOp and UnaryOp: binary and unary operations.
  - Number: numeric literal.
  - Var: variable (which in CHIRONLANG starts with a colon).

Variables in CHIRONLANG are represented as identifiers beginning with a colon.
"""


# test.py
"""
This test harness scans for all ".t1" test files in the current directory,
tokenizes and parses each CHIRONLANG source file, and prints the tokens and
AST along with the test file name. It uses the tokenizer from token.py (which
records line and column information) and the AST node classes from ast.py.
The parser defined here supports the following keywords: if, else, repeat,
penup, pendown, forward, backward, left, right, go, true, false, input.

Even if an individual test fails, the harness continues processing the remaining tests.
A summary is printed at the end.
"""
