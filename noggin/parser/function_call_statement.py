import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser
from statement import Statement
from call_arguments import CallArguments
from ident import Ident

class FunctionCallStatement(Statement):
    ident = None
    callArguments = None

    def __init__(self, ident, callArguments):
        self.ident = ident
        self.callArguments = callArguments

    @staticmethod
    def parse():
        staticIdent = None
        staticCallArguments = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        staticCallArguments = CallArguments.parse()

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return FunctionCallStatement(staticIdent, staticCallArguments)
