import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import noggin.lexer
from noggin.lexer.tokens import *
from parser_code import Parser


class Statement:
    @staticmethod
    def parse():
        from function_call_statement import FunctionCallStatement
        from assignment_statement import AssignmentStatement
        from if_else_statement import IfElseStatement
        from do_while_statement import DoWhileStatement
        from while_statement import WhileStatement

        if isinstance(Parser.get_token(), IdentToken):
            if isinstance(Parser.get_relative_token(1), LeftParenToken):
                return FunctionCallStatement.parse()
            elif isinstance(Parser.get_relative_token(1), AssignToken):
                return AssignmentStatement.parse()
            else:
                raise ParserException(Parser.get_token(), "2ndidentstatement")
        elif isinstance(Parser.get_token(), IfToken):
            return IfElseStatement.parse()
        elif isinstance(Parser.get_token(), DoToken):
            return DoWhileStatement.parse()
        elif isinstance(Parser.get_token(), WhileToken):
            return WhileStatement.parse()
        else:
            raise ParserException(Parser.get_token(), "StatementStartingToken")

    @staticmethod
    def able_to_start():
        return type(Parser.get_token()) in StatementStartingTokens