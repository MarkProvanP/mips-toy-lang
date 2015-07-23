import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser
from statement import Statement
from expression import Expression
from statements import Statements

class WhileStatement(Statement):
    whileExpression = None
    doStatements = None

    def __init__(self, whileExpression, doStatements):
        self.whileExpression = whileExpression
        self.doStatements = doStatements

    @staticmethod
    def parse():
        staticWhileExpression = None
        staticDoStatements = None

        if isinstance(Parser.get_token(), WhileToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), WhileToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        staticWhileExpression = Expression.parse()

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        staticDoStatements = Statements.parse()

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        return WhileStatement(staticWhileExpression, staticDoStatements)
