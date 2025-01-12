import re


class JackTokenizer:
    # Token types
    KEYWORD = 'keyword'          # Reserved words in Jack language
    SYMBOL = 'symbol'           # Special characters and operators
    IDENTIFIER = 'identifier'    # Variable and class names
    INT_CONST = 'integerConstant'  # Integer literals
    STRING_CONST = 'stringConstant'  # String literals

    # Lists of valid tokens
    KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char",
                "boolean", "void", "true", "false", "null", "this", "do", "if", "else", "while", "return", "let"]
    SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~',]
    
    # XML escape sequences for special symbols
    SPECIAL_SYMBOLS = {'<': '&lt;', '>': '&gt;', '"': '&qu;', '&': '&amp;'}

    def __init__(self, file):
        """
        Creates a new tokenizer for the input Jack file.
        Prepares to tokenize the input by initializing the tokenizer state.

        Parameters:
        - file (str): Path to the Jack source file to be tokenized.
        """
        self.currToken = None        # Current token being processed
        self.file = open(file, "r")  # Input file stream
        self.line = None             # Current line being processed
        self.hasMoreLines = True     # Whether more lines remain
        self.currTokenType = None    # Type of current token

    def advance(self):
        """
        Gets the next token from the input and makes it the current token.
        Should be called only if hasMoreTokens() is true.
        
        Handles:
        - Keywords
        - Symbols
        - Integer constants
        - String constants
        - Identifiers
        """
        # Read next line if current line is empty
        while (not self.line) and self.hasMoreLines:
            self.line = self.file.readline()
            originLine = self.line  # Save original line for comment handling
            if not self.line:
                self.hasMoreLines = False
            else:
                self.line = self.stripLine(self.line, originLine)

        # Process next token if there are more lines
        if self.hasMoreLines:
            # Check for keywords at start of line
            isKeyword = [keyword for keyword in JackTokenizer.KEYWORDS if self.line.startswith(keyword)]
            # Check for symbols at start of line
            isSymbol = [symbol for symbol in JackTokenizer.SYMBOLS if self.line.startswith(symbol)]

            # Determine token type and extract token
            if isKeyword:  # Found keyword
                self.currToken = isKeyword[0]
                self.currTokenType = JackTokenizer.KEYWORD

            elif isSymbol:  # Found symbol
                self.currToken = isSymbol[0]
                self.currTokenType = JackTokenizer.SYMBOL

            elif re.match(r'(\d+)(.*)', self.line):  # Found integer constant
                self.currToken = re.match(r'(\d+)(.*)', self.line).group(1)
                self.currTokenType = JackTokenizer.INT_CONST

            elif self.line.startswith('"'):  # Found string constant
                self.currToken = self.line.split('"')[1]
                self.currTokenType = JackTokenizer.STRING_CONST

            elif re.compile(r'^[a-zA-Z_]+').match(self.line):  # Found identifier
                self.currToken = re.compile(r'^[a-zA-Z_]+').search(self.line).group().strip()
                self.currTokenType = JackTokenizer.IDENTIFIER

            else:
                raise Exception("Input has an invalid token!")

            # Update line by removing processed token
            startIndex = len(self.currToken) + 2 if self.currTokenType == JackTokenizer.STRING_CONST else len(
                self.currToken)
            # Handle XML special characters
            self.currToken = self.currToken if self.currToken not in JackTokenizer.SPECIAL_SYMBOLS else (
                JackTokenizer.SPECIAL_SYMBOLS)[self.currToken]
            self.line = self.line[startIndex:].strip()

    def tokenType(self):
        """
        Returns the type of the current token as a constant.
        Used for XML tag generation.

        Returns:
        - str: Token type (keyword, symbol, identifier, integerConstant, stringConstant)
        """
        return self.currTokenType

    def keyword(self):
        """
        Returns the keyword which is the current token.
        Should be called only when tokenType() is KEYWORD.

        Returns:
        - str: The keyword string
        """
        return self.currToken

    def symbol(self):
        """
        Returns the character which is the current token.
        Should be called only when tokenType() is SYMBOL.

        Returns:
        - str: The symbol character (possibly escaped for XML)
        """
        return self.currToken

    def identifier(self):
        """
        Returns the identifier which is the current token.
        Should be called only when tokenType() is IDENTIFIER.

        Returns:
        - str: The identifier string
        """
        return self.currToken

    def intVal(self):
        """
        Returns the integer value of the current token.
        Should be called only when tokenType() is INT_CONST.

        Returns:
        - int: The integer value
        """
        return int(self.currToken)

    def stringVal(self):
        """
        Returns the string value of the current token.
        Should be called only when tokenType() is STRING_CONST.

        Returns:
        - str: The string value without the double quotes
        """
        return self.currToken

    def stripLine(this, line, originLine):
        """
        Removes comments and whitespace from a line of Jack code.
        Handles both inline and block comments.

        Parameters:
        - line (str): The line to process
        - originLine (str): Original line before any processing

        Returns:
        - str: The cleaned line with comments removed and whitespace trimmed
        """
        if originLine == line:
            for char in ['/**', '*/', '*']:  # Handle block comments
                if line.strip().startswith(char):
                    line = line.split(char)[0]
                    break
        line = line.split('//')[0]  # Remove inline comments
        return line.strip()

    def close(self):
        """
        Closes the input file and releases system resources.
        Should be called when finished with the tokenizer.
        """
        self.file.close()


if __name__ == '__main__':
    # Test the tokenizer
    tokenizer = JackTokenizer('Prog.jack')
    tokenizer.advance()
    while tokenizer.hasMoreLines:
        tokenType = tokenizer.currTokenType
        print(f'<{tokenType}>', end="")
        print(tokenizer.currToken, end="")
        print(f'</{tokenType}>')
        tokenizer.advance()