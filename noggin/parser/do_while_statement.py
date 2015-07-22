import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser

class DoWhileStatement(Statement):
    doStatements = None
    whileExpression = None

    def __init__(self, doStatements, whileExpression):
        self.doStatements = doStatements
        self.whileExpression = whileExpression

    
