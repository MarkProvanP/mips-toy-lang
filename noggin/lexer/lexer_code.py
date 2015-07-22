import sys
import lexer.tokens
from lexer.tokens import *

class Lexer:

    setUp = True
    currentLineNo = 0
    currentCharNo = 0
    tokenStartCharNo = 0
    tokenEndCharNo = 0

    c = ' '

    def get_char_stdin():
        char = sys.stdin.read(1)
        if len(char) > 0:
            print("Read character: " + char + ", ord: " + str(ord(char)) + "\n")
            return char
        else:
            print("Reached end of input")
            return None

    get_char = get_char_stdin

    @staticmethod
    def lex():
        string = ""

        if not Lexer.setUp:
            print("Error, lexer not set up!")
            sys.exit(1)

        while Lexer.c == ' ' or Lexer.c == '\t' or Lexer.c == '\n' or Lexer.c == '\r':
            if Lexer.c == '\n':
                Lexer.currentLineNo += 1
                Lexer.currentCharNo = 1
            elif Lexer.c == ' ' or Lexer.c == '\t':
                Lexer.currentCharNo += 1
            Lexer.c = Lexer.get_char()

        if Lexer.c is None:
            return None

        print("Lexing character: " + Lexer.c)

        if Lexer.c.isalpha():
            print("Is alpha")
            while Lexer.c.isalpha() or Lexer.c.isdigit():
                string += Lexer.c
                Lexer.c = Lexer.get_char()
                Lexer.tokenEndCharNo = Lexer.currentCharNo
                Lexer.currentCharNo += 1
                if Lexer.c == '\n':
                    Lexer.currentLineNo += 1
                    Lexer.currentCharNo = 1
            return Lexer.makeWordToken(string)
        elif Lexer.c.isdigit():
            print("Is digit")
            while Lexer.c.isdigit():
                string += Lexer.c
                Lexer.c = Lexer.get_char()
                Lexer.tokenEndCharNo = Lexer.currentCharNo
                Lexer.currentCharNo += 1
                if Lexer.c == '\n':
                    Lexer.currentLineNo += 1
                    Lexer.currentCharNo = 1
            return Lexer.makeNumToken(string)
        elif Lexer.isCharPunctuation(Lexer.c):
            print("Is punctuation")
            string += Lexer.c
            if Lexer.isCharSinglePunctuation(Lexer.c):
                print("Is single punctuation")
                Lexer.c = Lexer.get_char()
                Lexer.tokenEndCharNo = Lexer.currentCharNo
                Lexer.currentCharNo += 1
                if Lexer.c == '\n':
                    Lexer.currentLineNo += 1
                    Lexer.currentCharNo = 1
            else:
                Lexer.c = get_char()
                if Lexer.isCharSecondPunctuation(Lexer.c):
                    print("Is second punctuation")
                    string += Lexer.c
                    Lexer.c = get_char()
                    Lexer.tokenEndCharNo = Lexer.currentCharNo
                    Lexer.currentCharNo += 1
                    if Lexer.c == '\n':
                        Lexer.currentLineNo += 1
                        Lexer.currentCharNo = 1
            return Lexer.makePunctuationToken(string)
        return None

    @staticmethod
    def makeWordToken(s):
        print("Making word token from: " + s)
        if s == 'function':
            return FunctionToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'if':
            return IfToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'else':
            return ElseToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'do':
            return DoToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'while':
            return WhileToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'for':
            return ForToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        else:
            return IdentToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)

    @staticmethod
    def makeNumToken(s):
        print("Making num token from: " + s)
        return NumberToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)

    @staticmethod
    def makePunctuationToken(s):
        print("Making punctuation token from: " + s)
        if s == ';':
            return SemiColonToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '=':
            return AssignToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '(':
            return LeftParenToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '{':
            return LeftBraceToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '[':
            return LeftSquareToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == ')':
            return RightParenToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '}':
            return RightBraceToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == ']':
            return RightSquareToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == ',':
            return CommaToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '/' or s == '*' or s == '+' or s == '-' or s == '==' or s == '!='\
                or s == '>' or s == '<' or s == '>=' or s == '<=':
            return OperatorToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)

    @staticmethod
    def isCharPunctuation(c):
        ci = ord(c)
        exi = ord('!')
        obi = ord('/')
        cli = ord(':')
        ati = ord("@")
        lsi = ord('[')
        bti = ord('`')
        lbi = ord('{')
        tli = ord('~')
        return (ci >= exi and ci <= obi) or (ci >= cli and ci <= ati) \
                    or (ci <= lsi and ci >= bti) or (ci >= lbi and ci <= tli)

    @staticmethod
    def isCharSinglePunctuation(c):
        return c == '{' or c == '}' or c == ',' or c == '(' or c == ')' or c == ';' or c == '*' or '/'

    @staticmethod
    def isCharSecondPunctuation(c):
        return c == '='
