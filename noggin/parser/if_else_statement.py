import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser
from statement import Statement
from statements import Statements
from expression import Expression

class IfElseStatement(Statement):
    ifExpression = None
    thenStatements = None
    elseStatements = None

    def __init__(self, ifExpression, thenStatements, elseStatements):
        self.ifExpression = ifExpression
        self.thenStatements = thenStatements
        self.elseStatements = elseStatements

    @staticmethod
    def parse():
        staticIfExpression = None
        staticThenStatements = None
        staticElseStatements = None

        if isinstance(Parser.get_token(), IfToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IfToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        staticIfExpression = Expression.parse()

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        staticThenStatements = Statements.parse()

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        if isinstance(Parser.get_token(), ElseToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), ElseToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        staticThenStatements = Statements.parse()

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return IfElseStatement(staticIfExpression, staticThenStatements, staticElseStatements)
