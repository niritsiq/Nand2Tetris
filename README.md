# Nand2Tetris
Project 10: Jack Syntax Analyzer

Overview

Developed as part of the Nand2Tetris course, this project implements a syntax analyzer for the Jack language. It parses Jack programs and outputs XML files reflecting their syntactic structure.

Objectives

Tokenize Jack programs with JackTokenizer.

Parse syntax with CompilationEngine.

Generate XML outputs identical to provided reference files.

Usage

Setup: Run make (requires Python 3.12).

Run:

./JackAnalyzer <input>

<input>: Path to a .jack file or directory.

Output: Corresponding .xml file(s) in the same directory.

Example

Single File:

./JackAnalyzer ~/path/file.jack

Directory:

./JackAnalyzer ~/path/dir/

Submission

Submit project10.zip with:

AUTHORS: niritzik23@gmail.com , itaybardin@post.runi.ac.il

JackAnalyzer: Run file.

Makefile: Automates execution.

lang.txt: Contains Python.

Source Files: Main.py, CompilationEngine.py, JackTokenizer.py.
