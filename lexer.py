from sly import Lexer


class SimpleLexer(Lexer):
    # Set of token names
    tokens = {"IDENTIFIER", "NUMBER", "STRING",
              "TRUE", "FALSE",
              "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULE",
              "EQ", "LT", "LE", "GT", "GE", "NE",
              "STR_EQ", "STR_NE",
              "AND", "OR", "NOT",
              "ASSIGN",
              "L_PAREN", "R_PAREN",
              "FOR", "TO", "DO",
              "IF", "THEN", "ELSE",
              "SEMICOLON", "COMMA",
              "READINT", "LENGTH", "POSITION",
              "READSTRING", "CONCATENATE", "SUBSTRING",
              "BEGIN", "END", "EXIT", "BREAK", "CONTINUE",
              "PRINT"
              }

    # all ignore rules need a 'ignore' prefix
    # String containing ignored characters (between tokens)
    ignore = ' \t'
    # Other ignored patterns
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    # WARNING! Tokens are matched in the order of declaration
    # if you declare IDENTIFIER before method names like readint, 'readint' will be matched identifier

    # NUMBER = r'\d+'
    STRING = r'\".*?\"'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)  # Convert to a numeric value
        return t

    TRUE = r'true'
    FALSE = r'false'

    PLUS = r'\+'
    MINUS = r'\-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    MODULE = r'\%'

    # Logical relations: strings
    STR_EQ = r'=='
    STR_NE = r'!='

    # Logical relations: numbers
    EQ = r'='
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    NE = r'<>'

    # Logical relations: booleans
    AND = r'and'
    OR = r'or'
    NOT = r'not'

    # Assignment
    ASSIGN = r':='

    # Integer value methods
    READINT = r'readint'
    LENGTH = r'length'
    POSITION = r'position'

    # String value methods
    READSTRING = r'readstring'
    CONCATENATE = r'concatenate'
    SUBSTRING = r'substring'

    # Separators
    SEMICOLON = r';'
    COMMA = r','

    # Constructs
    BEGIN = r'begin'
    END = r'end'
    EXIT = r'exit'
    BREAK = r'break'
    CONTINUE = r'continue'

    FOR = r'for'
    TO = r'to'
    DO = r'do'

    IF = r'if'
    THEN = r'then'
    ELSE = r'else'

    # Other
    PRINT = r'print'

    L_PAREN = r'\('
    R_PAREN = r'\)'

    # Regular expression rules for tokens
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

