class Token(object):
    '''Common base class for all Tokens'''

    def __init__(self, original, lineNo, charStart, charEnd):
        self.original = original
        self.lineNo = lineNo
        self.charStart = charStart
        self.charEnd = charEnd

    def get_precedence(self):
        return 0

    def get_info(self):
        return "Token type {}, original text: {} on line {} between char: {} and {}".format(
            self.__class__.__name__,
            self.original,
            self.lineNo,
            self.charStart,
            self.charEnd
        )

class AssignToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(AssignToken, self).__init__(original, lineNo, charStart, charEnd)

class CommaToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(CommaToken, self).__init__(original, lineNo, charStart, charEnd)

class DoToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(DoToken, self).__init__(original, lineNo, charStart, charEnd)

class ElseToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(ElseToken, self).__init__(original, lineNo, charStart, charEnd)

class EOIToken(Token):
    def __init__(self):
        super(EOIToken, self).__init__(None, None, None, None)

class ForToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(ForToken, self).__init__(original, lineNo, charStart, charEnd)

class FunctionToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(FunctionToken, self).__init__(original, lineNo, charStart, charEnd)

class IdentToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(IdentToken, self).__init__(original, lineNo, charStart, charEnd)

class IfToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(IfToken, self).__init__(original, lineNo, charStart, charEnd)

class LeftBraceToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(LeftBraceToken, self).__init__(original, lineNo, charStart, charEnd)

class LeftParenToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(LeftParenToken, self).__init__(original, lineNo, charStart, charEnd)

class LeftSquareToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(LeftSquareToken, self).__init__(original, lineNo, charStart, charEnd)

class NumberToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(NumberToken, self).__init__(original, lineNo, charStart, charEnd)

class OperatorToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(OperatorToken, self).__init__(original, lineNo, charStart, charEnd)

class RightBraceToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(RightBraceToken, self).__init__(original, lineNo, charStart, charEnd)

class RightParenToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(RightParenToken, self).__init__(original, lineNo, charStart, charEnd)

class RightSquareToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(RightSquareToken, self).__init__(original, lineNo, charStart, charEnd)

class SemiColonToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(SemiColonToken, self).__init__(original, lineNo, charStart, charEnd)

class WhileToken(Token):
    def __init__(self, original, lineNo, charStart, charEnd):
        super(WhileToken, self).__init__(original, lineNo, charStart, charEnd)
