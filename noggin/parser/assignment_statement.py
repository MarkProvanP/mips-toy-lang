import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser
from statement import Statement

class AssignmentStatement(Statement):
    ident = None
    expression = None

    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

    @staticmethod
    def parse():
        staticIdent = None
        staticExpression = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), AssignToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), AssignToken)

        staticExpression = Expression.parse()

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return AssignmentStatement(staticIdent, staticExpression)
