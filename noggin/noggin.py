import argparse
import sys

import lexer_code
import lexer_tokens
from parser_code import Parser
from parser_elements import *

printVerbose = False

def main():
    a_parser = argparse.ArgumentParser(
        description='Compile noggin language to SPIM assembly'
    )
    args = a_parser.parse_args()

    myLexer = lexer_code.Lexer

    lexedTokens = []
    newToken = myLexer.lex()
    while newToken is not None:
        if printVerbose:
            print("Lexed new token: " + str(newToken))
        lexedTokens.append(newToken)
        newToken = myLexer.lex()
    if printVerbose:
        print("Reached end of tokens")
        for t in lexedTokens:
            print(t.get_info())

    Parser.set_tokens(lexedTokens)

    try:
        p = Program.parse()
        if printVerbose:
            print(p)
    except ParserException as e:
        print(e)



if __name__ == "__main__":
    main()
