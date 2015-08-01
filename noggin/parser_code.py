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
        if isinstance(self.expected, Token):
            x = str(self.expected.__name__)
        else:
            x = str(self.expected)
        return "ParserWrongTokenException: expected %s but got %s" % (x, str(type(self.token)))

class ParserFunctionDefineWithoutDeclareException(ParserException):
    def __init__(self, typeAndName):
        self.typeAndName = typeAndName

    def __str__(self):
        return "ParserFunctionDefineWithoutDeclareException: function %s defined without having been declared" % self.functionName

class ParserFunctionUseWithoutDeclareException(ParserException):
    def __init__(self, functionName):
        self.functionName = functionName

    def __str__(self):
        return "ParserFunctionUseWithoutDeclareException: function %s used before being declared" % self.functionName
        
class ParserVariableUseWithoutDeclareException(ParserException):
    def __init__(self, variableName):
        self.variableName = variableName

    def __str__(self):
        return "ParserVariableUseWithoutDeclareException: variable %s used before being declared" % self.variableName
