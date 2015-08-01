from lexer_tokens import Token

class Parser:
    tokenList = []
    tokenPosition = 0
    printVerbose = True

    @staticmethod
    def has_another_token():
        return len(Parser.tokenList) > Parser.tokenPosition\
            and Parser.tokenList[Parser.tokenPosition] is not None

    @staticmethod
    def get_token():
        try:
            return Parser.tokenList[Parser.tokenPosition]
        except IndexError as ie:
            return None

    @staticmethod
    def advance_token():
        if Parser.has_another_token():
            Parser.tokenPosition += 1

    @staticmethod
    def set_tokens(ts):
        Parser.tokenList = ts
        Parser.tokenPosition = 0

    @staticmethod
    def get_relative_token(n):
        newTokenPosition = Parser.tokenPosition + n
        if len(Parser.tokenList) > newTokenPosition:
            return Parser.tokenList[newTokenPosition]
        else:
            return None


class ParserException(Exception):
    pass

class ParserWrongTokenException(ParserException):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected

    def __str__(self):
        return "ParserWrongTokenException: expected " + str(self.expected.__name__) if isinstance(self.expected, Token) else str(self.expected)\
            + " but got " + str(self.token)

class ParserFunctionDefineWithoutDeclareException(ParserException):
    def __init__(self, typeAndName):
        self.typeAndName = typeAndName

    def __str__(self):
        return "ParserFunctionDefineWithoutDeclareException: function defined without having been "

class ParserVariableUseWithoutDeclareException(ParserException):
    def __init__(self, typeAndName):
        self.typeAndName = typeAndName

    def __str__(self):
        return "ParserUseWithoutDeclareException: variable used before being declared "
