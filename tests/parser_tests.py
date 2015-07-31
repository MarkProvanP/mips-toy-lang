from nose.tools import *

from noggin.lexer.tokens import *
from noggin.ng_parser.parser_code import Parser

def setup():
    print("Setting up parser tests")

def teardown():
    print("Tearing down parser tests")

def test_parse_prog():
    from noggin.parser.program import Program
    emptyProg = []
    Parser.set_tokens(emptyProg)
    pe = Program.parse()

    prog1 = [
        FunctionToken(),
        IdentToken("hello"),
        LeftParenToken(),
        RightParenToken(),
        LeftBraceToken(),
        RightBraceToken()
        ]
    Parser.set_tokens(prog1)
    p1 = Program.parse()
