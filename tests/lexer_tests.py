from nose.tools import *
from noggin.lexer.tokens import *

def setup():
    print("Setting up lexer tests")

def teardown():
    print("Tearing down lexer tests")

def test_tokens():
    print("Testing tokens")

    assignToken = AssignToken("=", 4, 1, 2)
    print(assignToken.get_info())

    commaToken = CommaToken(",", 5, 5, 6)
    print(commaToken.get_info())

    doToken = DoToken("do", 4, 4, 6)
    print(doToken.get_info())

    elseToken = ElseToken("else", 5, 8, 12)
    print(elseToken.get_info())

    eoiToken = EOIToken()
    print(eoiToken.get_info())

    forToken = ForToken("for", 8, 1, 4)
    print(forToken.get_info())

    functionToken = FunctionToken("function", 3, 0, 7)
    print(functionToken.get_info())

    identToken = IdentToken("hello", 9, 0, 5)
    print(identToken.get_info())

    ifToken = IfToken("if", 4, 1, 3)
    print(ifToken.get_info())

    leftBraceToken = LeftBraceToken("{", 1, 4, 5)
    print(leftBraceToken.get_info())

    leftParenToken = LeftParenToken("(", 4, 2, 3)
    print(leftParenToken.get_info())

    leftSquareToken = LeftSquareToken("[", 5, 9, 10)
    print(leftSquareToken.get_info())

    numberToken = NumberToken("1", 9, 10, 11)
    print(numberToken.get_info())

    operatorToken = OperatorToken("+", 10, 12, 13)
    print(operatorToken.get_info())

    rightBraceToken = RightBraceToken("}", 4, 3, 4)
    print(rightBraceToken.get_info())

    rightParenToken = RightParenToken(")", 3, 9, 10)
    print(rightParenToken.get_info())

    rightSquareToken = RightSquareToken("]", 9, 10, 11)
    print(rightSquareToken.get_info())

    semiColonToken = SemiColonToken(";", 10, 11, 12)
    print(semiColonToken.get_info())

    whileToken = WhileToken("while", 19, 10, 15)
    print(whileToken.get_info())
