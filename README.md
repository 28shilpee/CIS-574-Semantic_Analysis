# DLang Semantic Analyzer

# Overview
This project implements a semantic analyzer for the DLang programming language. The analyzer reads a DLang source file, performs semantic analysis according to defined language rules, and reports any semantic errors encountered.

# Features
The semantic analyzer checks the following language rules:

1. Variable Declaration: All identifiers must be declared before they are used.
2. Type Compatibility: Operands in any expression must be type-compatible.
3. Type Conversion Safety: All type conversions (especially explicit ones) are checked for safety.
4. Function Parameters: Function calls are verified for:
  - Type compatibility between actual and formal parameters 
  - Correct number of arguments (no missing or extra parameters)
5. Return Type Matching: Return values of functions must match their declared return types.

# Files
- `hw3-starter.py' - Main program containing the lexer, parser, and semantic analyzer
- `test-hw3.dlang' - Test file with examples of semantic errors

# Requirements
- Python 3.6+
- SLY (Sly Lex-Yacc) library

# Installation
-  Install required dependencies:
   pip install sly


# Usage
Run the analyzer with a DLang source file:
python hw3-starter.py test-hw3.dlang


# Output
The analyzer produces the following output:
- Detailed semantic error messages for each violation found
- Symbol table contents showing identifiers and their properties
- "No Semantic Error!" message if no errors are found

# Implementation Details:
# SymbolTable Class
The symbol table is used to store information about identifiers, including:
- Names
- Types
- Function parameters
- Values
- Current function context (for return type checking)

# DLangLexer Class
Based on SLY's Lexer, tokenizes DLang source code with support for:
- Keywords
- Operators
- Literals (strings, integers, doubles)
- Identifiers
- Comments

# DLangParser Class
Implements the grammar rules for DLang and performs semantic checks at appropriate points:
- Variable declarations are added to the symbol table
- Function declarations store their return types and parameters
- Expressions carry type information for compatibility checking
- Assignments verify type compatibility
- Function calls check parameter counts and types

# Simple Type System
The type system includes:
- Basic types: int, double, string, bool
- Type compatibility rules (e.g., int can be assigned to double but not vice versa)
- Special handling for string concatenation
- Logical operations requiring boolean operands

# Error Handling
Semantic errors are reported with detailed messages including:
- The nature of the error
- The line/context where the error occurred
- Related identifiers or types involved

# Errors Detected
- Use of undeclared variables
- Type mismatches in expressions
- Unsafe type conversions
- Incorrect function parameter counts or types
- Mismatched return types
