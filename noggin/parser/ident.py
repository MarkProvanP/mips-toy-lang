import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser
from primary_expression import PrimaryExpression

class Ident(PrimaryExpression):
    ident = None

    def __init__(self, ident):
        self.ident = ident
