import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser
from function import Function

class Program:
    functions = []

    def __init__(self, functions):
        self.functions = functions

    @staticmethod
    def parse():
        staticFunctions = []

        while Parser.has_more_tokens():
            if isinstance(Parser.get_token(), FunctionToken):
                nextFunction = Function.parse()
                staticFunctions.append(nextFunction)
            else:
                raise ParserException(Parser.get_token(), FunctionToken)

        return Program(staticFunctions)
