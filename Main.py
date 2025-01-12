import os
import sys
from CompilationEngine import *


def main():
    """
    Main program for the Jack Analyzer.
    
    Takes a Jack source file or directory as input and generates XML output.
    For a single .jack file, creates a corresponding .xml file.
    For a directory, processes all .jack files in that directory.
    
    Command line usage:
    python JackAnalyzer.py <input-file-or-directory>
    """
    if len(sys.argv) != 2:
        print("Usage: JackAnalyzer <input-file-or-directory>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path) and path.endswith(".jack"):
        process_file(path)
    elif os.path.isdir(path):
        files = [f for f in os.listdir(path) if f.endswith(".jack")]
        for file in files:
            process_file(os.path.join(path, file))
    else:
        print(f"Error: Invalid input path: {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)


def process_file(in_file):
    """
    Processes a single Jack file and generates XML output.

    Args:
        in_file (str): Path to input .jack file

    Creates an XML file with the same name as the input file.
    Example: Main.jack -> Main.xml
    """
    outfile = in_file.split(".jack")[0] + ".xml"
    compilationEngine = CompilationEngine(in_file, outfile)
    compilationEngine.compileClass()


if __name__ == "__main__":
    main() 