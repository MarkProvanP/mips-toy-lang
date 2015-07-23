import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser
from noggin.parser.statement import Statement

class Statements:
    statements = []

    def __init__(self, statements):
        self.statements = statements

    @staticmethod
    def parse():
        staticStatements = []
        while Statement.able_to_start():
            nextStaticStatement = Statement.parse()
            staticStatements.append(nextStaticStatement)
        return Statements(staticStatements)
