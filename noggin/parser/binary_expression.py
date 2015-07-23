import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser
from noggin.parser.expression import Expression

class BinaryExpression(Expression):
    left = None
    operator = None
    right = None

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
