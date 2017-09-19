from Token import Token


class JackTokenizer:
    # different types of tokens
    TOKEN_TYPE_KEYWORD = 'keyword'
    TOKEN_TYPE_SYMBOL = 'symbol'
    TOKEN_TYPE_IDENTIFIER = 'identifier'
    TOKEN_TYPE_INT_CONST = 'integerConstant'
    TOKEN_TYPE_STR_CONST = 'stringConstant'

    keywords = {
                'class': 0, 'method': 0, 'function': 0, 'constructor': 0, 'int': 0, 'boolean': 0, 'var': 0, 'static': 0,
                'field': 0, 'let': 0, 'do': 0, 'if': 0, 'else': 0, 'while': 0, 'return': 0, 'true': 0, 'false': 0,
                'null': 0, 'this': 0, 'void': 0, 'char': 0
               }

    symbols = {
                '{': '{', '}': '}', '(': '(', ')': ')', '[': '[', ']': ']', '.': '.', ',': ',', ';': ';', '+': '+',
                '-': '-', '*': '*', '/': '/', '&': '&amp;', '|': '|', '<': '&lt;', '>': '&gt;', '=': '=', '~': '~'
              }

    currentTokenType = None

    # string that gets built up to represent a token
    tokenString = ''

    # list of tokens
    tokenIndex = 0
    tokens = []

    foundComment = False

    def clean_line(self, line):
        # check for comments
        if self.foundComment and line.strip(' ').startswith('*'):
            return ''

        position = line.find("//")

        if position > -1:
            line = line[:position]

        position = line.find("/*")

        if position > -1:
            line = line[:position]
            self.foundComment = True

        return line.strip()

    def commit_token(self, string, type):
        self.tokens.append(Token(string, type))
        self.tokenString = ''
        self.currentTokenType = None

    def parse_character(self, character):
        # check if character is a symbol
        if character in JackTokenizer.symbols:
            if self.currentTokenType is not None:
                # commit current token
                self.commit_token(self.tokenString, self.currentTokenType)

            # it's a symbol!
            # commit, replacing symbol with xml representation
            self.commit_token(JackTokenizer.symbols[character], JackTokenizer.TOKEN_TYPE_SYMBOL)
            return

        # check for string constant closing
        if self.currentTokenType is JackTokenizer.TOKEN_TYPE_STR_CONST and character == '"':
            # commit current token
            self.tokenString = self.tokenString.replace('"', '')
            self.commit_token(self.tokenString, self.currentTokenType)
            return

        if (character == ' ' or character == '\n') and self.currentTokenType is not JackTokenizer.TOKEN_TYPE_STR_CONST:
            # space character also terminates tokens, but not string constants
            if self.currentTokenType is not None:
                # commit current token
                self.commit_token(self.tokenString, self.currentTokenType)
                return
            else:
                # white space
                return

        # append to token string and check for type
        self.tokenString += character

        # check if we've got a token yet
        type = self.tokenString.lower()

        if type in JackTokenizer.keywords:
            # likely a keyword
            self.currentTokenType = JackTokenizer.TOKEN_TYPE_KEYWORD
        else:
            # not a keyword
            if self.tokenString.isdigit():
                # likely numeric
                self.currentTokenType = JackTokenizer.TOKEN_TYPE_INT_CONST
            elif self.tokenString.startswith('"'):
                self.currentTokenType = JackTokenizer.TOKEN_TYPE_STR_CONST
            else:
                self.currentTokenType = JackTokenizer.TOKEN_TYPE_IDENTIFIER

        return

    def advance(self):
        token = self.tokens[self.tokenIndex]
        self.tokenIndex += 1
        return token

    def has_more_tokens(self):
        return self.tokenIndex < len(self.tokens)

    def __init__(self, jackFilePath):
        self.jackFilePath = jackFilePath
        self.tokens = []
        self.tokenString = ''
        self.currentTokenType = None
        self.tokenIndex = 0

        with open(self.jackFilePath) as jackFile:
            for line in jackFile:
                line = self.clean_line(line)

                for character in line:
                    self.parse_character(character)
