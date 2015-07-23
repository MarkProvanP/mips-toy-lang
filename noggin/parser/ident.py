import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser
from noggin.parser.primary_expression import PrimaryExpression

class Ident(PrimaryExpression):
    ident = None

    def __init__(self, ident):
        self.ident = ident
