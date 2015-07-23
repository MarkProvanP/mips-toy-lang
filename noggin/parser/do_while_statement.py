import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser
from noggin.parser.statement import Statement
from noggin.parser.expression import Expression

class DoWhileStatement(Statement):
    doStatements = None
    whileExpression = None

    def __init__(self, doStatements, whileExpression):
        self.doStatements = doStatements
        self.whileExpression = whileExpression

    @staticmethod
    def parse():
        staticDoStatements = None
        staticWhileExpression = None

        if isinstance(Parser.get_token(), DoToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), DoToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        staticDoStatements = Statements.parse()

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

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

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return DoWhileStatement(staticDoStatements, staticWhileExpression)
