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
            return char
        else:
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

        if Lexer.c.isalpha():
            Lexer.tokenStartCharNo = Lexer.currentCharNo
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
            Lexer.tokenStartCharNo = Lexer.currentCharNo
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
            string += Lexer.c
            Lexer.tokenStartCharNo = Lexer.currentCharNo
            if Lexer.isCharSinglePunctuation(Lexer.c):
                Lexer.c = Lexer.get_char()
                Lexer.tokenEndCharNo = Lexer.currentCharNo
                Lexer.currentCharNo += 1
                if Lexer.c == '\n':
                    Lexer.currentLineNo += 1
                    Lexer.currentCharNo = 1
            else:
                Lexer.c = get_char()
                if Lexer.isCharSecondPunctuation(Lexer.c):
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
        return NumberToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)

    @staticmethod
    def makePunctuationToken(s):
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
