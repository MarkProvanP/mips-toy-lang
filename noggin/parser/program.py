import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser
from noggin.parser.function import Function

class Program:
    functions = []

    def __init__(self, functions):
        self.functions = functions

    @staticmethod
    def parse():
        staticFunctions = []

        while Parser.has_another_token():
            if isinstance(Parser.get_token(), FunctionToken):
                nextFunction = Function.parse()
                staticFunctions.append(nextFunction)
            else:
                raise ParserException(Parser.get_token(), FunctionToken)

        return Program(staticFunctions)
