import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser
from ident import Ident

class DefineArguments:
    defineArguments = []

    def __init__(self, defineArguments):
        self.defineArguments = defineArguments

    @staticmethod
    def parse():
        staticDefineArguments = []

        if isinstance(Parser.get_token(), IdentToken):
            staticDefineArguments.append(Ident(Parser.get_token()))
            Parser.advance_token()
        elif isinstance(Parser.get_token(), RightParenToken):
            return DefineArguments(staticDefineArguments)
        else:
            raise ParserException(Parser.get_token(), "DefineArgumentsContinueToken")

        while isinstance(Parser.get_token(), CommaToken):
            Parser.advance_token()

            if isinstance(Parser.get_token(), IdentToken):
                staticDefineArguments.append(Ident(Parser.get_token()))
                Parser.advance_token()
            else:
                raise ParserException(Parser.get_token(), IdentToken)

        return DefineArguments(staticDefineArguments)
