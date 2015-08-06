import sys
from lexer_tokens import *
import string

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

        while Lexer.isCharWhitespace(Lexer.c) or Lexer.c == '#':
            if Lexer.isCharWhitespace(Lexer.c):
                if Lexer.printVerbose:
                    print("Skipping over whitespace character")
                if Lexer.check_for_new_line():
                    pass
                elif Lexer.c == ' ' or Lexer.c == '\t':
                    Lexer.currentCharNo += 1
                    Lexer.c = Lexer.get_char()
            if Lexer.c == '#':
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
            if Lexer.printVerbose:
                print("Lexer.c is None, reached end")
            return None

        if Lexer.printVerbose:
            print("Processing character: " + Lexer.c)
        if Lexer.isCharIdentStarter(Lexer.c):
            if Lexer.printVerbose:
                print("Character is alphanumeric: " + Lexer.c)
            Lexer.tokenStartCharNo = Lexer.currentCharNo
            while Lexer.isCharIdentContinue(Lexer.c):
                Lexer.continue_lexing_type()
            return Lexer.makeWordToken(Lexer.string)
        elif Lexer.c.isdigit():
            if Lexer.printVerbose:
                print("First character is number: " + Lexer.c)
            # Parse a number
            Lexer.tokenStartCharNo = Lexer.currentCharNo
            Lexer.string += Lexer.c
            Lexer.c = Lexer.get_char()
            # This is where a number can be base 2, 8, 10 or 16
            if Lexer.printVerbose:
                print("Second character is: " + Lexer.c)
            if Lexer.c.isdigit():
                if Lexer.printVerbose:
                    print("Second character is digit: " + Lexer.c)
                # Standard base 10 uint literal
                while Lexer.c.isdigit():
                    Lexer.continue_lexing_type()
                return UIntBase10Token(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
            elif Lexer.c == 'b':
                if Lexer.printVerbose:
                    print("Second character is binary start: " + Lexer.c)
                # Binary literal
                Lexer.string += Lexer.c
                Lexer.c = Lexer.get_char()
                while Lexer.c == '0' or Lexer.c == '1':
                    if Lexer.printVerbose:
                        print("Next binary character is: " + Lexer.c)
                    Lexer.continue_lexing_type()
                return UIntBase2Token(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
            elif Lexer.c == 'o':
                if Lexer.printVerbose:
                    print("Second character is octal start: " + Lexer.c)
                # Octal literal
                Lexer.string += Lexer.c
                Lexer.c = Lexer.get_char()
                while ord('0') <= ord(Lexer.c) <= ord('7'):
                    Lexer.continue_lexing_type()
                return UIntBase8Token(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
            elif Lexer.c == 'x':
                if Lexer.printVerbose:
                    print("Second character is hexadecimal start: " + Lexer.c)
                # Hexadecimal literal
                Lexer.string += Lexer.c
                Lexer.c = Lexer.get_char()
                while ord('0') <= ord(Lexer.c) <= ord('9') or ord('A') <= ord(Lexer.c) <= ord('F'):
                    Lexer.continue_lexing_type()
                return UIntBase16Token(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
            else:
                return UIntBase10Token(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif Lexer.isCharPunctuation(Lexer.c):
            if Lexer.printVerbose:
                print("Looking at punctuation character: " + Lexer.c)
            Lexer.tokenStartCharNo = Lexer.currentCharNo
            if Lexer.c == "-":
                if Lexer.printVerbose:
                    print("Found possible signed number character: " + Lexer.c)
                # This could either be a signed number or an operator
                Lexer.string += Lexer.c
                Lexer.c = Lexer.get_char()
                if Lexer.c.isdigit():
                    # This is a signed number
                    if Lexer.printVerbose:
                        print("This is a signed number")
                    while Lexer.c.isdigit():
                        Lexer.continue_lexing_type()
                    return IntBase10Token(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
                else:
                    return Lexer.makePunctuationToken(Lexer.string)

            elif Lexer.isCharSinglePunctuation(Lexer.c):
                if Lexer.printVerbose:
                    print("Punctuation is singleton")
                Lexer.continue_lexing_type()
            elif Lexer.c == '\'':
                # Lex a character
                Lexer.continue_lexing_type()
                if Lexer.c == '\\':
                    # Lex an escaped character, so two chars must be read
                    Lexer.continue_lexing_type()
                Lexer.continue_lexing_type()
                if Lexer.c == '\'':
                    # The final character should be a single quote
                    Lexer.continue_lexing_type()
                    return CharToken(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
                else:
                    raise LexerException(Lexer.c, '\'')
            elif Lexer.c == '\"':
                # Lex a string
                Lexer.continue_lexing_type()
                while Lexer.c != "\"":
                    # Lex the next character in the string
                    Lexer.continue_lexing_type()
                Lexer.continue_lexing_type()
                return StringToken(Lexer.string, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
            else:
                Lexer.continue_lexing_type()
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
        elif s == 'elif':
            return ElifToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'else':
            return ElseToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'do':
            return DoToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'while':
            return WhileToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'for':
            return ForToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'return':
            return ReturnToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'declare':
            return DeclareToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'true' or s == 'false':
            return BoolToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'switch':
            return SwitchToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'case':
            return CaseToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'break':
            return BreakToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'fallthrough':
            return FallThroughToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'default':
            return DefaultToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == 'asm':
            return ASMToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        else:
            return IdentToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)

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
        elif s == ':':
            return ColonToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '/' or s == '*' or s == '+' or s == '-' or s == '==' or s == '!='\
                or s == '>' or s == '<' or s == '>=' or s == '<=' or s == '<<' or s == '>>'\
                or s == '&' or s == '|' or s == '&&' or s == '||':
            return BinaryOperatorToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)
        elif s == '++' or s == '--':
            return UnaryOperatorToken(s, Lexer.currentLineNo, Lexer.tokenStartCharNo, Lexer.tokenEndCharNo)

    @staticmethod
    def isCharPunctuation(c):
        return c in string.punctuation

    @staticmethod
    def isCharSinglePunctuation(c):
        return c == '{' or c == '}' or c == ',' or c == '(' or c == ')' \
            or c == ';' or c == '*' or c == '/' or c == '[' or c == ']' \
            or c == '%' or c == '^'

    @staticmethod
    def isCharSecondPunctuation(c):
        return c == '=' or c == '&' or c == '|' or c == '<' or c == '>' \
            or c == '+' or c == '-'

    @staticmethod
    def isCharWhitespace(c):
        return str(c) in string.whitespace

    @staticmethod
    def isCharIdentStarter(c):
        return c.isalpha() or c == '_'

    @staticmethod
    def isCharIdentContinue(c):
        return Lexer.isCharIdentStarter(c) or c.isdigit() or c == "-"

class LexerException(Exception):
    def __init__(self, string, expected):
        self.string = string
        self.expected = expected

    def __str__(self):
        return "Lexer Exception: expected " + str(self.expected.__name__) \
            + " but got " + str(self.string)
