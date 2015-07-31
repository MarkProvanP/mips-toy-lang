from nose.tools import *
import sys

print("parser_tests: current path is:")
print(sys.path)

from lexer_tokens import *
from parser_code import Parser
from parser_elements import *

def setup():
    print("Setting up parser tests")

def teardown():
    print("Tearing down parser tests")

def test_parse_prog():
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
