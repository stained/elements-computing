from JackTokenizer import JackTokenizer


class CompilationEngine:

    currentTabStop = 0
    currentToken = None
    outText = ""

    def getTabs(self):
        return ''.join('\t' * self.currentTabStop)

    def output(self, text):
        tabs = self.getTabs()
        self.outText += tabs + text + "\n"

    def removeText(self, text):
        tabs = self.getTabs()
        text = tabs + text + "\n"
        if self.outText.endswith(text):
            self.outText = self.outText[:-len(text)]

    def output_type_value(self, type, value):
        self.output("<" + type + "> " + value + " </" + type + ">")

    def output_current_type_value(self):
        self.output_type_value(self.currentToken.type, self.currentToken.value)

    def print_current(self):
        print(self.currentToken.type, self.currentToken.value)

    def get_token(self):
        self.currentToken = self.tokenizer.get_current_token()
        return self.currentToken

    def advance(self):
        self.currentToken = self.tokenizer.advance()

    def look_ahead(self, distance):
        return self.tokenizer.look_ahead(distance)

    def check(self, requiredToken):
        self.currentToken = self.get_token()
        return self.currentToken.value == requiredToken

    def check_type(self, requiredType):
        self.currentToken = self.get_token()
        return self.currentToken.type == requiredType

    def check_type_value(self, type, value):
        return self.check_type(type) and self.check(value)

    def check_jack_type(self):
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "int") is False and \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "char") is False and \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "boolean") is False:
                if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
                    return False

        return True

    # compile complete class
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        # 'class'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "class") is False:
            return False

        self.output("<class>")
        self.currentTabStop += 1
        self.output_current_type_value()

        # className
        self.advance()
        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
            return False

        self.output_current_type_value()

        # '{'
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, "{") is False:
            return False

        self.output_current_type_value()

        # classVarDec*
        self.advance()
        while self.compile_class_var_dec() is not False:
            self.advance()

        # subroutineDec*
        while self.compile_sub_routine() is not False:
            self.advance()

        # '}'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, "}") is False:
            return False

        self.output_current_type_value()

        self.currentTabStop -= 1
        self.output("</class>")
        return

    # compile static or field declaration
    # ('static' | 'field') type varName (',' varName)* ';'
    # type = 'int' | 'char' | 'boolean' | className
    def compile_class_var_dec(self):
        # ('static' | 'field')
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "static") is False and \
           self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "field") is False:
            return False

        self.output("<classVarDec>")
        self.currentTabStop += 1
        self.output_current_type_value()

        # type
        self.advance()

        if self.check_jack_type() is False:
            return False

        self.output_current_type_value()

        # varName
        self.advance()
        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
            return False

        self.output_current_type_value()

        # (',' varName)*
        self.advance()
        while self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ",") is True:
            self.output_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, self.currentToken.value)
            self.advance()
            if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
                return False
            self.output_current_type_value()
            self.advance()

        # ';'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ";") is False:
            return False

        self.output_current_type_value()

        self.currentTabStop -= 1
        self.output("</classVarDec>")
        return

    # compile complete method, function, or constructor
    # ('constructor' | 'function' | 'method')
    # ('void' | type) subRoutineName '(' parameterList ')'
    # subRoutineBody = '{' varDec* statements '}'
    def compile_sub_routine(self):
        # ('constructor' | 'function' | 'method')
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "constructor") is False and \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "function") is False and \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "method") is False:
                return False

        self.output("<subroutineDec>")
        self.currentTabStop += 1

        self.output_current_type_value()

        # ('void' | type)
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, "void") is False and \
            self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
                return False

        self.output_current_type_value()

        # subRoutineName
        self.advance()
        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
            return False

        self.output_current_type_value()

        # '('
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, "(") is False:
            return False

        self.output_current_type_value()

        # parameterList
        self.advance()
        self.output("<parameterList>")
        self.currentTabStop += 1
        self.compile_parameter_list()
        self.currentTabStop -= 1
        self.output("</parameterList>")

        # ')'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ")") is False:
            return False

        self.output_current_type_value()

        # subRoutineBody
        self.output("<subroutineBody>")
        self.currentTabStop += 1

        # '{'
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, "{") is False:
            return False

        self.output_current_type_value()

        # varDec
        self.advance()
        while self.compile_var_dec() is True:
            self.advance()

        # statements
        self.output("<statements>")
        self.currentTabStop += 1
        if self.compile_statements() is True:
            self.advance()
        self.currentTabStop -= 1
        self.output("</statements>")

        # '}'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, "}") is False:
            return False

        self.output_current_type_value()

        self.currentTabStop -= 1
        self.output("</subroutineBody>")

        self.currentTabStop -= 1
        self.output("</subroutineDec>")
        return

    # compile (possibly empty) parameter list, excluding enclosing ()
    # ((type varName) (',' type varName)*)?
    # ? = 0 | 1 times, * = 0 or more
    def compile_parameter_list(self):
        # type
        if self.check_jack_type() is False:
            return False

        self.output_current_type_value()

        # varName
        self.advance()
        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
            return False

        self.output_current_type_value()

        # ,
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ',') is False:
            return False

        self.output_current_type_value()

        self.advance()
        while self.compile_parameter_list() is True:
            self.advance()

        return

    # compiles a var declaration
    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        # var
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'var') is False:
            return False

        self.output("<varDec>")
        self.currentTabStop += 1

        self.output_current_type_value()

        # type
        self.advance()
        if self.check_jack_type() is False:
            return False

        self.output_current_type_value()

        while True:
            # varName
            self.advance()
            if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
                return False

            self.output_current_type_value()

            # ,
            self.advance()
            if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ',') is False:
                break

            self.output_current_type_value()

        # ;
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ';') is True:
            self.output_current_type_value()

        self.currentTabStop -= 1
        self.output("</varDec>")

        return True

    # compile sequence of statements, excluding {}
    # statement *
    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statements(self):

        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'let') is True:
            self.output("<letStatement>")
            self.currentTabStop += 1

            if self.compile_let() is False:
                return False

            self.currentTabStop -= 1
            self.output("</letStatement>")
        elif self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'return') is True:
            self.output("<returnStatement>")
            self.currentTabStop += 1

            if self.compile_return() is False:
                return False

            self.currentTabStop -= 1
            self.output("</returnStatement>")
        elif self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'do') is True:
            self.output("<doStatement>")
            self.currentTabStop += 1

            if self.compile_do() is False:
                return False

            self.currentTabStop -= 1
            self.output("</doStatement>")
        elif self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'if') is True:
            self.output("<ifStatement>")
            self.currentTabStop += 1

            if self.compile_if() is False:
                return False

            self.currentTabStop -= 1
            self.output("</ifStatement>")
        elif self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'while') is True:
            self.output("<whileStatement>")
            self.currentTabStop += 1

            if self.compile_while() is False:
                return False

            self.currentTabStop -= 1
            self.output("</whileStatement>")
        else:
            return False

        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'let') is True or \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'do') is True or \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'while') is True or \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'if') is True or \
            self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'return') is True:
                self.compile_statements()
        else:
            futureToken = self.look_ahead(1)

            if futureToken is not False:
                if futureToken.type == JackTokenizer.TOKEN_TYPE_KEYWORD:
                    if futureToken.value == 'let' or \
                        futureToken.value == 'do' or \
                        futureToken.value == 'while' or \
                        futureToken.value == 'if' or \
                        futureToken.value == 'return':
                            self.advance()
                            self.compile_statements()

        return True

    # compiles a do statement
    # 'do' subRoutineCall
    # subRoutineCall = subRoutineName '(' expressionList ')' |
    #                  (className | varName) '.' subRoutineName '(' expressionList ')'
    def compile_do(self):
        # do
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'do') is False:
            return False

        self.output_current_type_value()

        # subRoutineName | className | varName
        self.advance()
        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
            return False

        self.output_current_type_value()

        # . or (
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '.') is True:
            self.output_current_type_value()

            # subRoutineName
            self.advance()
            if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
                return False

            self.output_current_type_value()

            self.advance()

            if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '(') is False:
                return False

            self.output_current_type_value()

            # expressionList
            self.advance()
            self.compile_expression_list()

        elif self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '(') is True:
            self.output_current_type_value()

            # expressionList
            self.advance()
            self.compile_expression_list()
        else:
            return False

        # ')'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ')') is False:
            return False

        self.output_current_type_value()

        # ';'
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ';') is False:
            return False

        self.output_current_type_value()

        return True

    # compiles a let statement
    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        # let
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'let') is False:
            return False

        self.output_current_type_value()

        # varName
        self.advance()
        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
            return False

        self.output_current_type_value()

        # '['
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '[') is True:
            self.output_current_type_value()

            # expression
            self.advance()
            if self.compile_expression() is True:
                self.advance()

            # ']'
            if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ']') is False:
                return False

            self.output_current_type_value()

            self.advance()

        # '='
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '=') is False:
            return False

        self.output_current_type_value()

        # expression
        self.advance()
        if self.compile_expression() is False:
            return False

        # ';'
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ';') is False:
            return False

        self.output_current_type_value()

        return True

    # compiles a while statement
    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        # while
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'while') is False:
            return False

        self.output_current_type_value()

        # '('
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '(') is False:
            return False

        self.output_current_type_value()

        # expression
        self.advance()
        if self.compile_expression() is True:
            self.advance()

        # ')'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ')') is False:
            return False

        self.output_current_type_value()

        # '{'
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '{') is False:
            return False

        self.output_current_type_value()

        # statements
        self.output("<statements>")
        self.currentTabStop += 1

        self.advance()
        if self.compile_statements() is True:
            self.advance()

        self.currentTabStop -= 1
        self.output("</statements>")

        # '}'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '}') is False:
            return False

        self.output_current_type_value()

        return True

    # compiles a return statement
    # 'return' expression? ';'
    def compile_return(self):
        # return
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'return') is False:
            return False

        self.output_current_type_value()

        # expression
        self.advance()
        if self.compile_expression() is True:
            self.advance()

        # ';'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ';') is False:
            return False

        self.output_current_type_value()

        return True

    # compiles an if statement
    # 'if' '(' expression ')' '{' statements '}'
    # ('else' '{' statements '}')?
    def compile_if(self):
        # if
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'if') is False:
            return False

        self.output_current_type_value()

        # '('
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '(') is False:
            return False

        self.output_current_type_value()

        # expression
        self.advance()
        if self.compile_expression() is True:
            self.advance()

        # ')'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ')') is False:
            return False

        self.output_current_type_value()

        # '{'
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '{') is False:
            return False

        self.output_current_type_value()

        # statements
        self.output("<statements>")
        self.currentTabStop += 1

        self.advance()
        if self.compile_statements() is True:
            self.advance()

        self.currentTabStop -= 1
        self.output("</statements>")

        # '}'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '}') is False:
            return False

        self.output_current_type_value()

        # else
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'else') is True:
            if self.compile_else() is False:
                return False

        return True

    # compile else, split for simplicity
    # ('else' '{' statements '}')?
    def compile_else(self):
        # else
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_KEYWORD, 'else') is False:
            return False

        self.output_current_type_value()

        # '{'
        self.advance()
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '{') is False:
            return False

        self.output_current_type_value()

        # statements
        self.output("<statements>")
        self.currentTabStop += 1

        self.advance()
        if self.compile_statements() is True:
            self.advance()

        self.currentTabStop -= 1
        self.output("</statements>")

        # '}'
        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '}') is False:
            return False

        self.output_current_type_value()

        return True

    # compiles an expression
    # term (op term)*
    # op = '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    def compile_expression(self):
        self.output("<expression>")
        self.currentTabStop += 1

        if self.compile_term() is False:
            self.currentTabStop -= 1
            self.removeText("<expression>")
            return False

        # compile more terms?
        # more terms!
        while True:
            futureToken = self.look_ahead(1)

            if futureToken is not False:
                if (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '+') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '-') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '*') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '/') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '&amp;') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '|') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '&lt;') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '&gt;') or \
                    (futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL and futureToken.value == '='):
                        self.advance()
                        self.output_current_type_value()

                        self.advance()
                        if self.compile_term() is False:
                            break
                else:
                    break
            else:
                break

        self.currentTabStop -= 1
        self.output("</expression>")

        return True

    # compiles a term
    # If token is identifier, must distinguish between var ., array [], and subroutine call ()
    # A single lookahead (for . [ {) is enough to determine which
    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' |
    # subRoutineCall | '(' expression ')' | unaryOp term ('-' | '~')
    # keywordConstant = 'true' | 'false' | 'null' | 'this'
    # subRoutineCall = subRoutineName '(' expressionList ')' |
    #                  (className | varName) '.' subRoutineName '(' expressionList ')'
    def compile_term(self):
        self.output("<term>")
        self.currentTabStop += 1

        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is True:
            # varName
            self.output_current_type_value()

            futureToken = self.look_ahead(1)

            if futureToken is not False:
                if futureToken.type == JackTokenizer.TOKEN_TYPE_SYMBOL:
                    # array
                    if futureToken.value == '[':
                        self.advance()
                        self.output_current_type_value()

                        # expression
                        self.advance()
                        if self.compile_expression() is True:
                            self.advance()

                        # ']'
                        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ']') is False:
                            self.currentTabStop -= 1
                            self.removeText("<term>")
                            return False

                        self.output_current_type_value()

                    # subroutine
                    elif futureToken.value == '.':
                        self.advance()
                        self.output_current_type_value()

                        # subRoutineName
                        self.advance()
                        if self.check_type(JackTokenizer.TOKEN_TYPE_IDENTIFIER) is False:
                            self.currentTabStop -= 1
                            self.removeText("<term>")
                            return False

                        self.output_current_type_value()

                        # '('
                        self.advance()
                        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, '(') is False:
                            self.currentTabStop -= 1
                            self.removeText("<term>")
                            return False

                        self.output_current_type_value()

                        # expressionList
                        self.advance()
                        self.compile_expression_list()

                        # ')'
                        if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ')') is False:
                            self.currentTabStop -= 1
                            self.removeText("<term>")
                            return False

                        self.output_current_type_value()

        elif self.check_type(JackTokenizer.TOKEN_TYPE_KEYWORD) is True:
            if self.check('true') is False and \
                self.check('false') is False and \
                self.check('null') is False and \
                self.check('this') is False:
                    self.currentTabStop -= 1
                    self.removeText("<term>")
                    return False

            self.output_current_type_value()
        elif self.check_type(JackTokenizer.TOKEN_TYPE_INT_CONST) is True:
            self.output_current_type_value()
        elif self.check_type(JackTokenizer.TOKEN_TYPE_STR_CONST) is True:
            self.output_current_type_value()
        elif self.check_type(JackTokenizer.TOKEN_TYPE_SYMBOL) is True:
            if self.check('-') is False and \
                self.check('(') is False and \
                self.check('&lt;') is False and \
                self.check('&gt;') is False and \
                self.check('&amp;') is False and \
                self.check('~') is False:
                    self.currentTabStop -= 1
                    self.removeText("<term>")
                    return False

            self.output_current_type_value()

            if self.check('(') is True:
                # expression
                self.advance()
                if self.compile_expression() is True:
                    self.advance()

                # ')'
                if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ')') is False:
                    self.currentTabStop -= 1
                    self.removeText("<term>")
                    return False

                self.output_current_type_value()

            elif self.check('-') is True or \
                self.check('&gt;') is True or \
                self.check('&lt;') is True or \
                self.check('&amp;') is True or \
                self.check('~') is True:
                    self.advance()
                    self.compile_term()
        else:
            self.currentTabStop -= 1
            self.removeText("<term>")
            return False

        self.currentTabStop -= 1
        self.output("</term>")

        return True

    # compiles a (possible empty) comma-separated list of expressions
    # (expression (',' expression)*)?
    def compile_expression_list(self):
        self.output("<expressionList>")
        self.currentTabStop += 1

        while self.compile_expression() is True:
            # ','
            self.advance()
            if self.check_type_value(JackTokenizer.TOKEN_TYPE_SYMBOL, ',') is False:
                break

            self.output_current_type_value()
            self.advance()

        self.currentTabStop -= 1
        self.output("</expressionList>")


    def __init__(self, tokenizer, outputFilename):
        self.tokenizer = tokenizer
        print ("Compiling: " + outputFilename + "\n")
        self.outFile = open(outputFilename, 'w')

        # begin class compilation
        self.compile_class()

        # write to file
        self.outFile.write(self.outText)

        self.outFile.close()

