class Parser:
    tokenList = []
    tokenPosition = 0

    @staticmethod
    def has_another_token():
        return len(Parser.tokenList) > Parser.tokenPosition\
            and Parser.tokenList[Parser.tokenPosition] is not None

    @staticmethod
    def get_token():
        return Parser.tokenList[tokenPosition]

    @staticmethod
    def advance_token():
        if Parser.has_another_token():
            Parser.tokenPosition += 1

    @staticmethod
    def set_tokens(ts):
        Parser.tokenList = ts
        Parser.tokenPosition = 0

class ParserException(Exception):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected
