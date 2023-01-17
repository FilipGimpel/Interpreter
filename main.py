from sly import Lexer


class SimpleLexer(Lexer):
    # Set of token names
    tokens = {"IDENTIFIER", "NUMBER", "STRING",
              "TRUE", "FALSE",
              "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULE",
              "EQ", "LT", "LE", "GT", "GE", "NE",
              "STR_EQ", "STR_NE",
              "AND", "OR", "NOT",
              "L_PAREN", "R_PAREN",
              "FOR", "TO", "DO",
              "IF", "THEN", "ELSE",
              "SEMI", "COMMA",
              "READINT", "LENGTH", "POSITION",
              "READSTRING", "CONCATENATE", "SUBSTRING",
              "BEGIN", "END", "EXIT", "BREAK", "CONTINUE",
              "PRINT"
              }

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    STRING = r'\".*?\"'

    TRUE = r'true'
    FALSE = r'false'

    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    MODULE = r'\%'

    # Logical relations: numbers
    EQ = r'='
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    NE = r'<>'

    # Logical relations: strings
    STR_EQ = r'=='
    STR_NE = r'!='

    # Logical relations: booleans
    AND = r'and'
    OR = r'or'
    NOT = r'not'

    # Integer methods
    READINT = r'readint'
    LENGTH = r'length'
    POSITION = r'position'

    # String methods
    READSTRING = r'readstring'
    CONCATENATE = r'concatenate'
    SUBSTRING = r'substring'

    # Separators
    SEMI = r';'
    COMMA = r','

    # Constructs
    BEGIN = r';'
    END = r','
    EXIT = r'exit'
    BREAK = r'break'
    CONTINUE = r'continue'

    FOR = r'for'
    TO = r'to'
    DO = r'do'

    IF = r'if'
    THEN = r'then'
    ELSE = r'else'

    L_PAREN = r'\('
    R_PAREN = r'\)'


if __name__ == '__main__':
    data = open("sample.txt", "r").read()
    lexer = SimpleLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
