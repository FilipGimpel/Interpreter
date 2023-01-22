from sly import Parser
from lexer import SimpleLexer


class SimpleParser(Parser):
    # Get the token list from the lexer (required)
    tokens = SimpleLexer.tokens

    # error output
    # debugfile = 'parser.out'

    # TODO precedence - fix shift/reduce conflicts (ambiguous grammar)
    # TODO I omitted the program = instr; rule because it seems unnecessary

    # TODO unary minus?
    precedence = (
       ('left', "PLUS", "MINUS"),
       ('left', "MULTIPLY", "DIVIDE", "MODULE"),
       ('left', "OR"),
       ('left', "AND"),
    )

    # WARNING!! declaration order matters! otherwise define 'start' property of this class

    # region instruction sequence
    '''
        instr = instr simple_instr ";" | epsilon ;
    '''
    @_('instr simple_instr SEMICOLON')
    def instr(self, p):
        if p.simple_instr is not None:
            return p.instr, p.simple_instr
        return 'instruction', p.instr,

    @_('')
    def instr(self, p):
        return 'instruction'
    # endregion

    # region basic constructs
    '''
        simple_instr = assign_stat
            | if_stat
            | for_stat
            | "begin" instr "end"
            | output_stat
            | "break" ;
            | "continue"
            | "exit" ;
    '''
    @_('assign_stat')
    def simple_instr(self, p):
        return p

    @_('if_stat')
    def simple_instr(self, p):
        return p

    @_('for_stat')
    def simple_instr(self, p):
        return p

    @_('BEGIN instr END')
    def simple_instr(self, p):
        return p.instr

    @_('output_stat')
    def simple_instr(self, p):
        return p

    @_('BREAK')
    def simple_instr(self, p):
        return p

    @_('CONTINUE')
    def simple_instr(self, p):
        return p.CONTINUE

    @_('EXIT')
    def simple_instr(self, p):
        return p.EXIT
    # endregion

    # region assignment: :=
    '''
        assign = IDENT ":=" num_expr
            | IDENT ":=" str_expr ;
    '''
    @_('IDENTIFIER ASSIGN expr')
    def assign_stat(self, p):
        return 'ASSIGN', p.IDENTIFIER, p.expr

    @_('IDENTIFIER ASSIGN str_expr')
    def assign_stat(self, p):
        return 'ASSIGN', p.IDENTIFIER, p.str_expr
    # endregion

    # region for loop
    '''
        for_stat = "for" IDENT ":=" num_expr "to" num_expr "do" simple_instr ;
    '''
    @_('FOR IDENTIFIER ASSIGN expr TO expr DO simple_instr')
    def for_stat(self, p):
        return p.FOR, p.IDENTIFIER, p.expr0, p.expr1, p.simple_instr
    # endregion

    # region conditional statement: if/if else
    '''
        if_stat = "if" bool_expr "then" simple_instr 
                | "if" bool_expr "then" simple_instr "else" simple_instr ;
    '''
    @_('IF bool_expr THEN simple_instr')
    def if_stat(self, p):
        return p.IF, p.bool_expr, p.THEN, p.simple_instr

    @_('IF bool_expr THEN simple_instr ELSE simple_instr')
    def if_stat(self, p):
        return p.IF, p.bool_expr, p.THEN, p.simple_instr0, p.ELSE, p.simple_instr1
    # endregion

    # region printing
    '''
        output_stat = print(" expr ")"
            | "print(" str_expr ")" ;
    '''
    @_('PRINT L_PAREN expr R_PAREN')
    def output_stat(self, p):
        return p.PRINT, p.expr

    @_('PRINT L_PAREN str_expr R_PAREN')
    def output_stat(self, p):
        return p.PRINT, p.str_expr
    # endregion

    # region logical relations: boolean expressions
    # TODO
    '''
        f_bool_exp = "true" | "false"
            | "(" bool_expr ")"
            | "not" bool_expr
            | num_expr num_rel num_expr
            | str_expr str_rel str_expr ;
    '''
    @_('TRUE')
    @_('FALSE')
    def f_bool_expr(self, p):
        return p.f_bool_expr,

    @_('L_PAREN bool_expr R_PAREN')
    def f_bool_expr(self, p):
        return p.bool_expr

    @_('NOT bool_expr')
    def f_bool_expr(self, p):
        return p.NOT, p.bool_expr,

    @_('expr num_rel expr')
    def f_bool_expr(self, p):
        return p.num_rel, p[0], p[2]

    @_('str_expr str_rel str_expr')
    def f_bool_expr(self, p):
        return p.str_rel, p[0], p[2]
    # endregion

    # region boolean multiplication: AND
    '''
        t_bool_expr = t_bool_expr "and" f_bool_expr | f_bool_expr ;
    '''
    @_('t_bool_expr AND f_bool_expr')
    def t_bool_expr(self, p):
        return p.AND, p.t_bool_expr, p.f_bool_expr

    @_('f_bool_expr')
    def t_bool_expr(self, p):
        return p.f_bool_expr
    # endregion

    # region boolean sum: OR
    '''
        bool_expr = bool_expr "or" t_bool_expr | t_bool_expr ;
    '''
    @_('bool_expr OR t_bool_expr')
    def bool_expr(self, p):
        return p.OR, p.bool_expr, p.t_bool_expr,

    @_('t_bool_expr')
    def bool_expr(self, p):
        return p.t_bool_expr
    # endregion

    # region boolean string relations: ==, !=
    @_('STR_EQ')
    @_('STR_NE')
    def str_rel(self, p):
        return p[0]
    # endregion

    # region boolean numerical relations: =, <, <=, >, >=, <>
    @_('EQ')
    @_('LT')
    @_('LE')
    @_('GT')
    @_('GE')
    @_('NE')
    def num_rel(self, p):
        return p[0]
    # endregion

    # region numerical expressions: +, -
    ''' numerical expressions: addition
        expr = expr "+" term 
            | expr "-" term 
            | term ;
    '''
    @_('expr PLUS term')
    def expr(self, p):
        return p.PLUS, p.expr, p.term

    @_('expr MINUS term')
    def expr(self, p):
        return p.MINUS, p.expr, p.term

    @_('term')
    def expr(self, p):
        return p.term
    # endregion

    # region numerical expressions: *, /, %
    ''' numerical expressions: multiplication, module
        term = term "*" factor 
            | term "/" factor 
            | term "%" factor 
            | factor ;
    '''
    @_('term MULTIPLY factor')
    def term(self, p):
        return p.MULTIPLY, p.term, p.factor

    @_('term DIVIDE factor')
    def term(self, p):
        return p.DIVIDE, p.term, p.factor

    @_('term MODULE factor')
    def term(self, p):
        return p.MODULE, p.term, p.factor

    @_('factor')
    def term(self, p):
        return p.factor
    # endregion

    # region numerical expressions: readint, -, (), length, position
    ''' numerical expressions: methods, parenthesis, minus
        factor = NUMBER | IDENTIFIER
            | "readint"
            | "-" factor
            | "(" factor ")"
            | "length" "(" str_expr ")"
            | "position" "(" str_expr "," str_expr ")" ;
    '''
    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('IDENTIFIER')
    def factor(self, p):
        return p.IDENTIFIER

    @_('READINT')
    def factor(self, p):
        return p.READINT

    @_('MINUS expr')
    def factor(self, p):
        return -p.expr

    @_('L_PAREN expr R_PAREN')
    def factor(self, p):
        return p.expr

    @_('LENGTH L_PAREN str_expr R_PAREN')
    def factor(self, p):
        return p.LENGTH, p.str_expr

    @_('POSITION L_PAREN str_expr COMMA str_expr R_PAREN')
    def factor(self, p):
        return p.POSITION, p[2], p[4]
    # endregion

    # region string expressions: readstring, concatenate, substring
    '''
        str_expr = STRING | IDENT
            | "readstr"
            | "concatenate(" str_expr "," str_expr ")"
            | "substring(" str_expr "," num_expr "," num_expr ")" ;
    '''
    @_('STRING')
    def str_expr(self, p):
        return p.STRING

    @_('IDENTIFIER')
    def str_expr(self, p):
        return p.IDENTIFIER

    @_('READSTRING')
    def str_expr(self, p):
        return p.READSTRING

    @_('CONCATENATE L_PAREN str_expr COMMA str_expr R_PAREN')
    def str_expr(self, p):
        return p.CONCATENATE, p[2], p[4]

    @_('SUBSTRING L_PAREN str_expr COMMA expr COMMA expr R_PAREN')
    def str_expr(self, p):
        return p.SUBSTRING, p[2], p[4], p[6]
    # endregion




