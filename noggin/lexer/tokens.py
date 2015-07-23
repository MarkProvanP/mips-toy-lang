StatementStartingTokens = []
DefineArgumentContinueTokens = []

uln = "?"
ucs = "?"
uce = "?"

class Token(object):
    '''Common base class for all Tokens'''

    def __init__(self, original,\
            lineNo = uln,\
            charStart = ucs,\
            charEnd = uce\
    ):
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
    def __init__(self, original = "=", lineNo = uln, charStart = ucs, charEnd = uce):
        super(AssignToken, self).__init__(original, lineNo, charStart, charEnd)

class CommaToken(Token):
    def __init__(self, original = ",", lineNo = uln, charStart = ucs, charEnd = uce):
        super(CommaToken, self).__init__(original, lineNo, charStart, charEnd)

class DoToken(Token):
    def __init__(self, original = "do", lineNo = uln, charStart = ucs, charEnd = uce):
        super(DoToken, self).__init__(original, lineNo, charStart, charEnd)

StatementStartingTokens.append(DoToken)

class ElseToken(Token):
    def __init__(self, original = "else", lineNo = uln, charStart = ucs, charEnd = uce):
        super(ElseToken, self).__init__(original, lineNo, charStart, charEnd)

class EOIToken(Token):
    def __init__(self):
        super(EOIToken, self).__init__(None, None, None, None)

class ForToken(Token):
    def __init__(self, original = "for", lineNo = uln, charStart = ucs, charEnd = uce):
        super(ForToken, self).__init__(original, lineNo, charStart, charEnd)

class FunctionToken(Token):
    def __init__(self, original = "function", lineNo = uln, charStart = ucs, charEnd = uce):
        super(FunctionToken, self).__init__(original, lineNo, charStart, charEnd)

class IdentToken(Token):
    def __init__(self, original, lineNo = uln, charStart = ucs, charEnd = uce):
        super(IdentToken, self).__init__(original, lineNo, charStart, charEnd)
StatementStartingTokens.append(IdentToken)
DefineArgumentContinueTokens.append(IdentToken)

class IfToken(Token):
    def __init__(self, original = "if", lineNo = uln, charStart = ucs, charEnd = uce):
        super(IfToken, self).__init__(original, lineNo, charStart, charEnd)
StatementStartingTokens.append(IfToken)

class LeftBraceToken(Token):
    def __init__(self, original = "{", lineNo = uln, charStart = ucs, charEnd = uce):
        super(LeftBraceToken, self).__init__(original, lineNo, charStart, charEnd)

class LeftParenToken(Token):
    def __init__(self, original = "(", lineNo = uln, charStart = ucs, charEnd = uce):
        super(LeftParenToken, self).__init__(original, lineNo, charStart, charEnd)

class LeftSquareToken(Token):
    def __init__(self, original = "[", lineNo = uln, charStart = ucs, charEnd = uce):
        super(LeftSquareToken, self).__init__(original, lineNo, charStart, charEnd)

class NumberToken(Token):
    def __init__(self, original, lineNo = uln, charStart = ucs, charEnd = uce):
        super(NumberToken, self).__init__(original, lineNo, charStart, charEnd)

class OperatorToken(Token):
    def __init__(self, original, lineNo = uln, charStart = ucs, charEnd = uce):
        super(OperatorToken, self).__init__(original, lineNo, charStart, charEnd)

class RightBraceToken(Token):
    def __init__(self, original = "]", lineNo = uln, charStart = ucs, charEnd = uce):
        super(RightBraceToken, self).__init__(original, lineNo, charStart, charEnd)

class RightParenToken(Token):
    def __init__(self, original = ")", lineNo = uln, charStart = ucs, charEnd = uce):
        super(RightParenToken, self).__init__(original, lineNo, charStart, charEnd)
DefineArgumentContinueTokens.append(RightParenToken)

class RightSquareToken(Token):
    def __init__(self, original = "]", lineNo = uln, charStart = ucs, charEnd = uce):
        super(RightSquareToken, self).__init__(original, lineNo, charStart, charEnd)

class SemiColonToken(Token):
    def __init__(self, original, lineNo = uln, charStart = ucs, charEnd = uce):
        super(SemiColonToken, self).__init__(original, lineNo, charStart, charEnd)

class WhileToken(Token):
    def __init__(self, original = ";", lineNo = uln, charStart = ucs, charEnd = uce):
        super(WhileToken, self).__init__(original, lineNo, charStart, charEnd)
StatementStartingTokens.append(WhileToken)
