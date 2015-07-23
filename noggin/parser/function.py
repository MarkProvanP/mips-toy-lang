import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser
from noggin.parser.ident import Ident
from noggin.parser.define_arguments import DefineArguments
from noggin.parser.statements import Statements

class Function:
    functionName = None
    functionDefineArguments = None
    statements = None

    def __init__(self, functionName, functionDefineArguments, statements):
        self.functionName = functionName
        self.functionDefineArguments = functionDefineArguments
        self.statements = statements

    @staticmethod
    def parse():
        staticFunctionName = None
        staticFunctionDefineArguments = None
        staticStatements = None

        # If a function is being parsed, then we already have a function token
        # here so we don't need to check again
        Parser.advance_token()

        if isinstance(Parser.get_token(), IdentToken):
            staticFunctionName = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        staticFunctionDefineArguments = DefineArguments.parse()

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        staticStatements = Statements.parse()

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        return Function(staticFunctionName, staticFunctionDefineArguments, staticStatements)
