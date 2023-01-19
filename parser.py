from sly import Parser
from lexer import SimpleLexer


class SimpleParser(Parser):
    # Get the token list from the lexer (required)
    tokens = SimpleLexer.tokens

    # TODO precedence - fix shift/reduce conflicts (ambiguous grammar)
    # TODO remember - declaration order matters! otherwise define 'start' property of this class
    # TODO build AST tree
    # TODO tests

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

    # region basic constructs TODO
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
    # endregion

    # region assignment: :=
    '''
        assign = IDENT ":=" num_expr
            | IDENT ":=" str_expr ;
    '''
    @_('IDENTIFIER ASSIGN expr')
    def assign_stat(self, p):
        # raise ValueError('TODO')
        return 'ASSIGN', p.IDENTIFIER, p.expr

    @_('IDENTIFIER ASSIGN str_expr')
    def assign_stat(self, p):
        raise ValueError('TODO')
    # endregion

    # region for loop
    '''
        for_stat = "for" IDENT ":=" num_expr "to" num_expr "do" simple_instr ;
    '''
    @_('FOR IDENTIFIER ASSIGN expr TO DO simple_instr')
    def for_stat(self, p):
        return p
    # endregion

    # region conditional statement: if/if else
    '''
        if_stat = "if" bool_expr "then" simple_instr 
                | "if" bool_expr "then" simple_instr "else" simple_instr ;
    '''
    @_('IF bool_expr THEN simple_instr')
    def if_stat(self, p):
        return p

    @_('IF bool_expr THEN simple_instr ELSE simple_instr')
    def if_stat(self, p):
        return p
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
        return 'BOOLEAN EXPRESSION', p.f_bool_expr,

    @_('L_PAREN f_bool_expr R_PAREN')
    def f_bool_expr(self, p):
        raise ValueError('TODO')

    @_('NOT f_bool_expr')
    def f_bool_expr(self, p):
        return 'NOT', p.f_bool_expr,

    @_('expr num_rel expr')
    def f_bool_expr(self, p):
        return 'NUMBER COMPARISON', p.f_bool_expr,

    @_('str_expr str_rel str_expr')
    def f_bool_expr(self, p):
        return 'STRING COMPARISON', p.f_bool_expr,
    # endregion

    # region boolean multiplication: AND
    '''
        t_bool_expr = t_bool_expr "and" f_bool_expr | f_bool_expr ;
    '''
    @_('t_bool_expr AND f_bool_expr')
    def t_bool_expr(self, p):
        return 'AND', p.f_bool_expr,

    @_('f_bool_expr')
    def t_bool_expr(self, p):
        return p
    # endregion

    # region boolean sum: OR
    '''
        bool_expr = bool_expr "or" t_bool_expr | t_bool_expr ;
    '''
    @_('t_bool_expr OR t_bool_expr')
    def bool_expr(self, p):
        return 'AND', p.f_bool_expr,

    @_('t_bool_expr')
    def bool_expr(self, p):
        return p
    # endregion

    # region boolean string relations: ==, !=
    @_('STR_EQ')
    @_('STR_NE')
    def str_rel(self, p):
        raise ValueError('TODO')
    # endregion

    # region boolean numerical relations: =, <, <=, >, >=, <>
    @_('EQ')
    @_('LT')
    @_('LE')
    @_('GT')
    @_('GE')
    @_('NE')
    def num_rel(self, p):
        raise ValueError('TODO')
    # endregion

    # region numerical expressions: +, -
    ''' numerical expressions: addition
        expr = expr "+" term 
            | expr "-" term 
            | term ;
    '''
    @_('expr PLUS term')
    def expr(self, p):
        # return p.expr + p.term
        return 'binary-expression', p[0], p[1], p[2]

    @_('expr MINUS term')
    def expr(self, p):
        return p.expr - p.term

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
        return p.term * p.factor

    @_('term DIVIDE factor')
    def term(self, p):
        return p.term / p.factor

    @_('term MODULE factor')
    def term(self, p):
        return p.term % p.factor

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
        raise ValueError('TODO')

    @_('MINUS expr')
    def factor(self, p):
        return -p.expr

    @_('L_PAREN expr R_PAREN')
    def factor(self, p):
        raise ValueError('TODO')

    @_('LENGTH L_PAREN str_expr R_PAREN')
    def factor(self, p):
        raise ValueError('TODO')

    @_('POSITION L_PAREN str_expr COMMA str_expr R_PAREN')
    def factor(self, p):
        raise ValueError('TODO')
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
        raise ValueError('TODO')

    @_('IDENTIFIER')
    def str_expr(self, p):
        raise ValueError('TODO')

    @_('READSTRING')
    def str_expr(self, p):
        raise ValueError('TODO')

    @_('CONCATENATE L_PAREN str_expr COMMA str_expr R_PAREN')
    def str_expr(self, p):
        raise ValueError('TODO')

    @_('SUBSTRING L_PAREN str_expr COMMA expr COMMA expr R_PAREN')
    def str_expr(self, p):
        raise ValueError('TODO')
    # endregion




