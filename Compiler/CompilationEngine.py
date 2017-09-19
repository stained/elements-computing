class CompilationEngine:

    # compile complete class
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        if self.tokenizer.has_more_tokens():
            token = self.tokenizer.advance()



        return

    # compile static or field declaration
    # ('static' | 'field') type varName (',' varName)* ';'
    # type = 'int' | 'char' | 'boolean' | className
    def compile_class_var_dec(self):
        return

    # compile complete method, function, or constructor
    # ('constructor' | 'function' | 'method')
    # ('void | type) subRoutineName '(' parameterList ')'
    # subRoutineBody = '{' varDec* statements '}'
    def compile_sub_routine(self):
        return

    # compile (possibly empty) parameter list, excluding enclosing ()
    # ((type varName) (',' type varName)*)?
    # ? = 0 | 1 times, * = 0 or more
    def compile_parameter_list(self):
        return

    # compiles a var declaration
    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        return

    # compile sequence of statements, excluding {}
    # statement *
    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statements(self):
        return

    # compiles a do statement
    # 'do' subRoutineCall
    def compile_do(self):
        return

    # compiles a let statement
    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        return

    # compiles a while statement
    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        return

    # compiles a return statement
    # 'return' expression? ';'
    def compile_return(self):
        return

    # compiles an if statement
    # 'if' '(' expression ')' '{' statements '}'
    # ('else' '{' statements '}')?
    def compile_if(self):
        return

    # compiles an expression
    # term (op term)*
    # op = '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    def compile_expression(self):
        return

    # compiles a term
    # If token is identifier, must distinguish between var ., array [], and subroutine call ()
    # A single lookahead (for . [ {) is enough to determine which
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' |
    # subRoutineCall | '(' expression ')' | unaryOp term ('-' | '~')
    # keywordConstant = 'true' | 'false' | 'null' | 'this'
    # subRoutineCall = subRoutineName '(' expressionList ')' |
    #                  (className | varName) '.' subRoutineName '(' expressionList ')'
    def compile_term(self):
        return

    # compiles a (possible empty) comma-separated list of expressions
    # (expression (',' expression)*)?
    def compile_expression_list(self):
        return

    def __init__(self, tokenizer, outputFilename):
        self.tokenizer = tokenizer

        outFile = open(outputFilename, 'w')

        # begin class compilation
        self.compile_class()

            #outFile.write('<' + token.type + '>' + token.value + '</' + token.type + '>\n')

        outFile.close()

