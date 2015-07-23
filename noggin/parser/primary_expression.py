import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser
from noggin.parser.expression import Expression

class PrimaryExpression(Expression):
    @staticmethod
    def parse():
        staticPrimaryExpression = None
        if isinstance(Parser.get_token(), NumberToken):
            staticPrimaryExpression = Number(Parser.get_token())
            Parser.advance_token()
        elif isinstance(Parser.get_token(), IdentToken):
            staticPrimaryExpression = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), PrimaryExpression)
        return staticPrimaryExpression
