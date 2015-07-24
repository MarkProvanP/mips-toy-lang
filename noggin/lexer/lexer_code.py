import sys
import lexer.tokens
from lexer.tokens import *

class Lexer:

    setUp = True
    currentLineNo = 1
    currentCharNo = 1
    tokenStartCharNo = 0
    tokenEndCharNo = 0

    printVerbose = True

    firstCharacterRead = False
    c = ''
    string = ""

    def get_char_stdin():
        char = sys.stdin.read(1)
        if len(char) > 0:
            if ord(char) == 13:
                # if we've just read a '\r' carriage return character
                return get_char_stdin()
            return char
        else:
            return None

    get_char = get_char_stdin

    @staticmethod
    def check_for_new_line():
        if Lexer.c == '\n':
            if Lexer.printVerbose:
                print("Newline at line: %d char: %d" % (Lexer.currentLineNo, Lexer.currentCharNo))
            Lexer.advance_line()
            return True
        return False

    @staticmethod
    def advance_line():
        Lexer.currentLineNo += 1
        Lexer.currentCharNo = 1
        Lexer.c = Lexer.get_char()

    @staticmethod
    def continue_lexing_type():
        Lexer.string += Lexer.c
        Lexer.c = Lexer.get_char()
        Lexer.tokenEndCharNo = Lexer.currentCharNo + 1
        Lexer.currentCharNo += 1

    @staticmethod
    def lex():
        Lexer.string = ""

        if not Lexer.setUp:
            print("Error, lexer not set up!")
            sys.exit(1)

        if not Lexer.firstCharacterRead:
            Lexer.firstCharacterRead = True
            Lexer.c = Lexer.get_char()

        while Lexer.c == ' ' or Lexer.c == '\t' or Lexer.c == '\r' or Lexer.c == '\n':
            if Lexer.printVerbose:
                print("Skipping over whitespace character")
            if Lexer.check_for_new_line():
                pass
            elif Lexer.c == ' ' or Lexer.c == '\t':
                Lexer.currentCharNo += 1
                Lexer.c = Lexer.get_char()

        while Lexer.c == '#':
            # Then we have a comment for the rest of this line
            if Lexer.printVerbose:
                print("Found a comment!")
            Lexer.c = Lexer.get_char()
            comment = ""
            while Lexer.c != '\n':
                comment += Lexer.c
                Lexer.c = Lexer.get_char()
            if Lexer.printVerbose:
                print("Complete comment: %s" % comment)
            Lexer.advance_line()

        if Lexer.c is None:
            return None

        if Lexer.c.isalpha():
            Lexer.tokenStartCharNo = Lexer.currentCharNo
            while Lexer.c.isalpha() or Lexer.c.isdigit():
                Lexer.continue_lexing_type()
            return Lexer.makeWordToken(Lexer.string)
        elif Lexer.c.isdigit():
            Lexer.tokenStartCharNo = Lexer.currentCharNo
            while Lexer.c.isdigit():
                Lexer.continue_lexing_type()
            return Lexer.makeNumToken(Lexer.string)
        elif Lexer.isCharPunctuation(Lexer.c):
            Lexer.tokenStartCharNo = Lexer.currentCharNo
            if Lexer.isCharSinglePunctuation(Lexer.c):
                Lexer.continue_lexing_type()
            else:
                Lexer.string += Lexer.c
                Lexer.c = get_char()
                if Lexer.isCharSecondPunctuation(Lexer.c):
                    Lexer.continue_lexing_type()
            return Lexer.makePunctuationToken(Lexer.string)
        return None

    @staticmethod
    def makeWordToken(s):
        if Lexer.printVerbose:
            print("Making word token from \"%s\", length: %d" % (s, len(s)))
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
