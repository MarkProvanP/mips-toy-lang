import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser

class CallArguments:
    callExpressions = []

    def __init__(self, callExpressions):
        self.callExpressions = callExpressions

    @staticmethod
    def parse():
        staticCallExpressions = []

        if isinstance(Parser.get_token(), RightParenToken):
            pass
        else:
            staticCallExpressions.append(Expression.parse())

        while isinstance(Parser.get_token(), CommaToken):
            Parser.advance_token()
            staticCallExpressions.append(Expression.parse())

        return CallArguments(staticCallExpressions)
