import argparse
import sys

from lexer import lexer_code
from lexer import tokens
from ir import ir_code
from parser_new.parser_code_new import Parser
from parser_new.parser_elements_new import *

def main():
    a_parser = argparse.ArgumentParser(description='Compile noggin language to SPIM assembly')
    args = a_parser.parse_args()

    myLexer = lexer_code.Lexer

    lexedTokens = []
    newToken = myLexer.lex()
    while (newToken != None):
        lexedTokens.append(newToken)
        newToken = myLexer.lex()
    for t in lexedTokens:
        print(t.get_info())

    Parser.set_tokens(lexedTokens)

    try:
        p = Program.parse()
    except ParserException as e:
        print(e)

if __name__ == "__main__":
    main()
