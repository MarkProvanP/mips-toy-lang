import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser

class Expression:
    @staticmethod
    def parse():
        return Expression.fraser_hanson(1)

    @staticmethod
    def fraser_hanson(k):
        from binary_expression import BinaryExpression
        from primary_expression import PrimaryExpression

        i = 0
        left = None
        operator = None
        right = None
        left = PrimaryExpression.parse()

        i = Parser.get_token().get_precedence()
        while i >= k:
            while Parser.get_token().get_precedence() == i:
                operator = Parser.get_token()
                Parser.advance_token()
                right = fraser_hanson(i + 1)
                left = BinaryExpression(left, operator, right)
            i -= 1
        return left
