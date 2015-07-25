from lexer.tokens import Token

class Parser:
    tokenList = []
    tokenPosition = 0

    @staticmethod
    def has_another_token():
        return len(Parser.tokenList) > Parser.tokenPosition\
            and Parser.tokenList[Parser.tokenPosition] is not None

    @staticmethod
    def get_token():
        return Parser.tokenList[Parser.tokenPosition]

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
            return EOIToken()


class ParserException(Exception):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected

    def __str__(self):
        return "Parser Exception: expected " + str(self.expected.__name__) if isinstance(self.expected, Token) else str(self.expected)\
            + " but got " + str(self.token)
