import re
import string


# Constants
ALPHABET = string.ascii_letters
DIGITS = string.digits
DELIM = string.whitespace
ARITHMETIC_OPERATORS = '+-*/%'
COMPAR = '<>='
PUNCTUATION = '[]\{\}(),;'


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

#Specific error for introducing illegal character in a context
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


#Keeps track of file name, text, line, column and number id 
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    #Advances the position and checks wherever column has changed
    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

    #copies the current position 
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


######## TOKENS #########

TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_CHAR     = 'CHAR'
TT_STRING   = 'STRING'
TT_STR_CHAR = 'STR_CHAR' # "ABC"
TT_FUNC     = 'FUNC'  # func
TT_VOID     = 'VOID'
TT_CONST    = 'CONST'

# Arithmetic operators
TT_PLUS    = 'PLUS'  # +
TT_MINUS   = 'MINUS' # -
TT_MUL     = 'MUL'   # *
TT_DIV     = 'DIV'   # /
TT_MOD     = 'MOD'   # %

# Comparison operators
TT_EQ      = 'EQ'    # =
TT_NEQ     = 'NEQ'   # !=
TT_LT      = 'LT'    # <
TT_GT      = 'GT'    # >
TT_LTEQ    = 'LTEQ'  # <=
TT_GTEQ    = 'GTEQ'  # >=

# Boolean operators
TT_NOT = 'NOT'  # !
TT_AND = 'AND'  # &&
TT_OR  = 'OR'   # ||

# IDENTIFIER
TT_ID = 'ID'

# ASSIGNMENT
TT_ASN = 'ASN'  # :=

# RESERVED WORDS
TT_IF      = 'IF'  
TT_ELSE    = 'ELSE'  
TT_VAR     = 'VAR'  
TT_FOR     = 'FOR' 
TT_WHILE   = 'WHILE'
TT_PRINT   = 'PRINT'
TT_RETURN  = 'RETURN'
TT_TRUE    = 'TRUE'
TT_FALSE   = 'FALSE'

reservedWords = {
    "func": TT_FUNC,
    "if": TT_IF,
    "else": TT_ELSE,
    "while": TT_WHILE,
    "var": TT_VAR,
    "for": TT_FOR,
    "const": TT_CONST,
    "int": TT_INT,
    "float": TT_FLOAT,
    "char": TT_CHAR,
    "string": TT_STRING,
    "print": TT_PRINT,
    "return": TT_RETURN,
    "true": TT_TRUE,
    "false": TT_FALSE
}

# Punctuation
TT_LPAREN  = 'LPAREN'  # (
TT_RPAREN  = 'RPAREN'  # )
TT_LBRAC   = 'LBRAC'   # {
TT_RBRAC   = 'RBRAC'   # }
TT_LSBRAC  = 'LSBRAC'  # [
TT_RSBRAC  = 'RSBRAC'  # ]
TT_SQUOT   = 'SQUOT'   # '
TT_DQUOT   = 'DQUOT'   # "
TT_COMMA   = 'COMMA'   # ,
TT_COMMENT = 'COMMENT' #
TT_COL     = 'COL'  # :
TT_SEMICOL = 'SEMICOL' #;

class Token:
    def __init__(self, _type, value=None, pos=None):
        self.type = _type
        self.value = value
        self.pos = pos

    def __repr__(self):
        line = self.pos.ln + 1
        if self.value:
            return f'[Line {line}] token {self.type}: {self.value}'
        return f'[Line {line}] token {self.type}'


############ LEXER #############

#Declaration of initial values for position, name file, the text of the program, and current character 
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.getChar()

    #Function to move to the next character
    def getChar(self):
        #Moves the position using specification from Position Class
        self.pos.advance(self.current_char)
        #Checks if there are any more characters left to be tokenized
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    #Creates the tokens themselves by comparing the current character with characters described by rules of grammar 
    def make_tokens(self):
        tokens = []

        #Checking current character.
        while self.current_char != None:
            if self.current_char in DELIM:
                self.getChar()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in ALPHABET + '_':
                tokens.append(self.make_word())
            elif self.current_char in ARITHMETIC_OPERATORS:
                tokens.append(self.make_arithmetic_op())
                self.getChar()
            elif self.current_char in COMPAR:
                tokens.append(self.make_compar())
            elif self.current_char in PUNCTUATION:
                tokens.append(self.make_punctuation())
                self.getChar()
            elif self.current_char == '\'':
                pos_start = self.pos.copy()
                char = self.current_char
                try:
                    tokens.append(self.make_char())
                except Exception as e:
                    return [], IllegalCharError(pos_start, self.pos, "'" + str(e)[-1] + "'")
            elif self.current_char == '\"':
                pos_start = self.pos.copy()
                char = self.current_char
                try:
                    tokens.append(self.make_string())
                except Exception as e:
                    return [], IllegalCharError(pos_start, self.pos, "'" + str(e)[-1] + "'")
            elif self.current_char == '#':
                tokens.append(self.make_comment())
            elif self.current_char == ':':
                tokens.append(self.make_assign())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.getChar()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    # Construct number
    def make_number(self):
        pos_start = self.pos.copy()
        num_str = ''
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.getChar()

        return Token(TT_INT, int(num_str), pos_start)

    # Construct word
    def make_word(self):
        pos_start = self.pos.copy()
        word = ''
        while self.current_char != None and re.match("[_a-zA-Z0-9]", self.current_char):
            word += self.current_char
            self.getChar()

        # Check if word exists in the map of reserved words
        if word in reservedWords.keys():
            return Token(reservedWords[word], word, pos_start)

        # Check if word is a valid identifier
        if(re.match("[_a-zA-Z]([_a-zA-Z0-9])*", word)):
            return Token(TT_ID, word, pos_start)

    # Arithmetic Operators
    def make_arithmetic_op(self):
        pos_start = self.pos.copy()
        if self.current_char == '+':
            return Token(TT_PLUS, self.current_char, pos_start)
        elif self.current_char == '-':
            return Token(TT_MINUS, self.current_char, pos_start)
        elif self.current_char == '*':
            return Token(TT_MUL, self.current_char, pos_start)
        elif self.current_char == '/':
            return Token(TT_DIV, self.current_char, pos_start)
        else:
            return Token(TT_MOD, self.current_char, pos_start)

    # Relational Operators
    def make_compar(self):
        pos_start = self.pos.copy()
        if self.current_char == '=':
            self.getChar()
            return Token(TT_EQ, '=', pos_start)
        elif self.current_char == '<':
            self.getChar()
            if self.current_char == '=':
                self.getChar()
                return Token(TT_LTEQ, '<=', pos_start)
            else:
                return Token(TT_LT, '<', pos_start)
        else:
            self.getChar()
            if self.current_char == '=':
                self.getChar()
                return Token(TT_GTEQ, '>=', pos_start)
            else:
                return Token(TT_GT, '>', pos_start)

    # Punctuation
    def make_punctuation(self):
        pos_start = self.pos.copy()
        if self.current_char == '(':
            return Token(TT_LPAREN, self.current_char, pos_start)
        elif self.current_char == ')':
            return Token(TT_RPAREN, self.current_char, pos_start)
        elif self.current_char == '{':
            return Token(TT_LBRAC, self.current_char, pos_start)
        elif self.current_char == '}':
            return Token(TT_RBRAC, self.current_char, pos_start)
        elif self.current_char == '[':
            return Token(TT_LSBRAC, self.current_char, pos_start)
        elif self.current_char == ']':
            return Token(TT_RSBRAC, self.current_char, pos_start)
        elif self.current_char == ',':
            return Token(TT_COMMA, self.current_char, pos_start)
        elif self.current_char == ';':
            return Token(TT_SEMICOL, self.current_char, pos_start)

    # Assignment
    def make_assign(self):
        pos_start = self.pos.copy()
        self.getChar()
        if(self.current_char == '='):
            self.getChar()
            return Token(TT_ASN, ':=', pos_start)
        else:
            return Token(TT_COL, ':', pos_start)

    # Construct character
    def make_char(self):
        pos_start = self.pos.copy()
        char = '\''
        self.getChar()
        if self.current_char != None:
            char += self.current_char
            # If empty character
            if self.current_char == '\'':
                self.getChar()
                return Token(TT_CHAR, char, pos=pos_start)
            else:
                self.getChar()
                char += self.current_char
                if self.current_char == '\'':
                    self.getChar()
                    return Token(TT_CHAR, char, pos=pos_start)
                else:
                    raise Exception(char)

    def make_string(self):
        pos_start = self.pos.copy()
        string = '\"'
        self.getChar()
        while self.current_char != None and self.current_char != '\"':
            string += self.current_char
            self.getChar()
        if self.current_char == '\"':
            string += self.current_char
            self.getChar()
            return Token(TT_STRING, string, pos_start)
        else:
            raise Exception(string)

    def make_comment(self):
        pos_start = self.pos.copy()
        comment = ''
        while self.current_char != None and self.current_char != '\n':
            comment += self.current_char
            self.getChar()
        return Token(TT_COMMENT, comment, pos=pos_start)


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error