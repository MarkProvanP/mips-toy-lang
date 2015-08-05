from lexer_tokens import Token

from noggin_types import NT_types_base

class Parser:
    tokenList = []
    tokenPosition = 0
    printVerbose = True

    @staticmethod
    def has_another_token():
        return len(Parser.tokenList) > Parser.tokenPosition\
            and Parser.tokenList[Parser.tokenPosition] is not None

    @staticmethod
    def get_token():
        try:
            return Parser.tokenList[Parser.tokenPosition]
        except IndexError as ie:
            return None

    @staticmethod
    def advance_token():
        if Parser.has_another_token():
            Parser.tokenPosition += 1

    @staticmethod
    def set_tokens(ts):
        Parser.tokenList = ts
        Parser.tokenPosition = 0

    @staticmethod
    def get_relative_token(n):
        newTokenPosition = Parser.tokenPosition + n
        if len(Parser.tokenList) > newTokenPosition:
            return Parser.tokenList[newTokenPosition]
        else:
            return None

class Environment:
    d = {}
    t = {}

    def __init__(self, d={}):
        self.d = d
        self.t = NT_types_base

    def get(self, k):
        return self.d[k]

    def set(self, k, v):
        self.d[k] = v

    def contains(self, k):
        return k in self.d

    def copy(self):
        return Environment(self.d.copy())

    def add(self, k, v):
        if self.contains(k):
            raise ParserRepeatedDeclarationException(
                self.get(k),
                v)
        else:
            self.set(k, v)

    def items(self):
        return self.d.items()

    def types(self, name):
        return self.t[name]

class ParserException(Exception):
    pass

class ParserWrongTokenException(ParserException):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected

    def __str__(self):
        if isinstance(self.expected, Token):
            x = str(self.expected.__name__)
        else:
            x = str(self.expected)
        return ("ParserWrongTokenException: expected %s but got %s,\n"
            "on line %d between char %d and %d\n"
            % (x,
                str(type(self.token)),
                self.token.lineNo,
                self.token.charStart,
                self.token.charEnd
                ))

class ParserFunctionDefineWithoutDeclareException(ParserException):
    def __init__(self, functionName):
        self.functionName = functionName

    def __str__(self):
        return ("ParserFunctionDefineWithoutDeclareException: function %s "
            "defined without having been declared"
            % self.functionName.source_ref())

class ParserFunctionUseWithoutDeclareException(ParserException):
    def __init__(self, functionName):
        self.functionName = functionName

    def __str__(self):
        return ("ParserFunctionUseWithoutDeclareException: function %s used "
            "before being declared"
            % self.functionName.source_ref())
        
class ParserVariableUseWithoutDeclareException(ParserException):
    def __init__(self, variableName):
        self.variableName = variableName

    def __str__(self):
        return ("ParserVariableUseWithoutDeclareException: variable %s used "
            "before being declared"
            % self.variableName.source_ref())

class ParserRepeatedDeclarationException(ParserException):
    def __init__(self, originalDeclaration, newDeclaration):
        self.originalDeclaration = originalDeclaration
        self.newDeclaration = newDeclaration

    def __str__(self):
        return ("ParserRepeatedDeclarationException: original declaration %s "
            "repeated %s"
            % (self.originalDeclaration.source_ref(),
                self.newDeclaration.source_ref()))

class ParserFunctionSignatureDefinitionNotEqualException(ParserException):
    def __init__(self, declaration, definition):
        self.declaration = declaration
        self.definition = definition

    def __str__(self):
        return ("ParserFunctionSignatureDefinitionNotEqualException: function "
            "definition\n"
            "%s\n"
            "argument types different from those in "
            "declaration\n"
            "%s\n"
            % (self.definition.source_ref_sig_only(), self.declaration.source_ref()))

class ParserFunctionVariableDeclareDefineMismatchException(ParserException):
    def __init__(self, declaration, definition):
        self.declaration = declaration
        self.definition = definition

    def __str__(self):
        return ("ParserFunctionVariableDeclareDefineMismatchException:"
            "definition\n"
            "%s\n"
            "mismatches declaration"
            "%s\n"
            % (self.definition.source_ref(), self.declaration.source_ref()))

class ParserUnknownTypeException(ParserException):
    def __init__(self, unknownType):
        self.unknownType = unknownType

    def __str__(self):
        return ("ParserUnknownTypeException:"
            "type: %s is unknown"
            % (str(self.unknownType)))