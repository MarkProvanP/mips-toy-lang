import argparse
from lexer import lexer_code
from lexer import tokens

def main():
    parser = argparse.ArgumentParser(description='Compile noggin language to SPIM assembly')
    args = parser.parse_args()

    print("hello world")

    myLexer = lexer_code.Lexer()

    lexedTokens = []
    newToken = myLexer.lex()
    while (newToken != None):
        lexedTokens.append(newToken)
        newToken = myLexer.lex()
    for t in lexedTokens:
        print(t.get_info())

if __name__ == "__main__":
    main()
