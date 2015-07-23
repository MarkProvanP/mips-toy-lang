from nose.tools import *
from noggin.parser.parser_code import Parser

def setup():
    print("Setting up parser tests")

def teardown():
    print("Tearing down parser tests")

def test_parse_prog():
    from noggin.parser.program import Program
    emptyProg = []
    Parser.set_tokens(emptyProg)
    p = Program.parse()
