import argparse
import sys

from lexer import lexer_code
from lexer import tokens
from parser import parser_code, program
from parser.parser_code import Parser
from program import Program

def main():
    parser = argparse.ArgumentParser(description='Compile noggin language to SPIM assembly')
    args = parser.parse_args()

    print("hello world")

    myLexer = lexer_code.Lexer

    lexedTokens = []
    newToken = myLexer.lex()
    while (newToken != None):
        lexedTokens.append(newToken)
        newToken = myLexer.lex()
    for t in lexedTokens:
        print(t.get_info())

    Parser.set_tokens(lexedTokens)

    p = Program.parse()

if __name__ == "__main__":
    main()
