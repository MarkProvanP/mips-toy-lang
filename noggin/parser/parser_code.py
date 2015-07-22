class Parser:
    @staticmethod
    def get_token():
        pass

class ParserException(Exception):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected
