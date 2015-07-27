from lexer.tokens import *

from ng_parser.parser_code import Parser, ParserException, ParserWrongTokenException

def expect_token(token):
    if isinstance(Parser.get_token(), token):
        Parser.advance_token()
    else:
        raise ParserWrongTokenException(Parser.get_token(), token)

class Expression:
    @staticmethod
    def parse(environment = {}):
        return Expression.fraser_hanson(1)

    @staticmethod
    def fraser_hanson(k):

        i = 0
        left = None
        operator = None
        right = None
        left = PrimaryExpression.parse()

        i = Parser.get_token().get_precedence()
        while i >= k:
            while Parser.get_token().get_precedence() == i:
                operator = Parser.get_token()
                Parser.advance_token()
                right = Expression.fraser_hanson(i + 1)
                left = BinaryExpression(left, operator, right)
            i -= 1
        return left

class PrimaryExpression(Expression):
    @staticmethod
    def parse(environment = {}):
        staticPrimaryExpression = None
        if isinstance(Parser.get_token(), NumberToken):
            staticPrimaryExpression = Number(Parser.get_token())
            Parser.advance_token()
        elif isinstance(Parser.get_token(), IdentToken):
            if isinstance(Parser.get_relative_token(1), LeftSquareToken):
                staticPrimaryExpression = ArrayAccessExpression.parse()
            elif isinstance(Parser.get_relative_token(1), LeftParenToken):
                staticPrimaryExpression = FunctionCallExpression.parse()
            else:
                staticPrimaryExpression = Ident(Parser.get_token())
                Parser.advance_token()
        elif isinstance(Parser.get_token(), BoolToken):
            staticPrimaryExpression = Bool(Parser.get_token())
            Parser.advance_token()
        elif isinstance(Parser.get_token(), CharToken):
            staticPrimaryExpression = Char(Parser.get_token())
            Parser.advance_token()
        elif isinstance(Parser.get_token(), StringToken):
            staticPrimaryExpression = String(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), PrimaryExpression)
        return staticPrimaryExpression

    def eval(self):
        return None

class BinaryExpression(Expression):
    left = None
    operator = None
    right = None

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return "(" + str(self.left) + " " + str(self.operator) + " " + str(self.right) + ")"

class ArrayAccessExpression(PrimaryExpression):
    arrayName = None
    levelExpression = []

    def __init__(self, arrayName, levelExpression):
        self.arrayName = arrayName
        self.levelExpression = levelExpression

    @staticmethod
    def parse(environment = {}):
        staticArrayName = None
        staticLevelExpression = []

        if isinstance(Parser.get_token(), IdentToken):
            staticArrayName = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), LeftSquareToken):
            Parser.advance_token()
            try:
                nextStaticLevelExpression = Expression.parse()
                staticLevelExpression.append(nextStaticLevelExpression)
            except ParserException as e:
                print("Caught " + str(e) + " while parsing ArrayAccessExpression level expression no: 1")
                raise e

            expect_token(RightSquareToken)

        while isinstance(Parser.get_token(), LeftSquareToken):
            Parser.advance_token()
            try:
                nextStaticLevelExpression = Expression.parse()
                staticLevelExpression.append(nextStaticLevelExpression)
            except ParserException as e:
                print("Caught " + str(e) + " while parsing ArrayAccessExpression level expression no: " + str(1 + len(staticLevelExpression)))
                raise e

            expect_token(RightSquareToken)

    def __str__(self):
        s = self.arrayName
        for le in self.levelExpression:
            s += '[%s]' % le
        return s

class FunctionCallExpression(PrimaryExpression):
    ident = None
    callArguments = None

    def __init__(self, ident, callArguments):
        self.ident = ident
        self.callArguments = callArguments

    @staticmethod
    def parse(environment = {}):
        staticIdent = None
        staticCallArguments = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        expect_token(LeftParenToken)

        try:
            staticCallArguments = CallArguments.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing FunctionCallStatement call arguments")
            raise e

        expect_token(RightParenToken)

        return FunctionCallExpression(staticIdent, staticCallArguments)

    def __str__(self):
        return "%s(%s);" % (str(self.ident), str(self.callArguments))

class LiteralExpression(PrimaryExpression):
    pass

class Bool(LiteralExpression):
    value = None

    def __init__(self, value):
        self.value = value

    def eval(self):
        return bool(self.value)

    def __str__(self):
        return str(self.value)

class Ident(LiteralExpression):
    ident = None

    def __init__(self, ident):
        self.ident = ident

    def __str__(self):
        return str(self.ident)

class Number(LiteralExpression):
    number = None

    def __init__(self, number):
        self.number = number

    def __str__(self):
        return str(self.number)

class Char(LiteralExpression):
    char = None

    def __init__(self, char):
        self.char = char

    def eval(self):
        return chr(self.char)

    def __str__(self):
        return str(self.char)

class String(LiteralExpression):
    string = None

    def __init__(self, string):
        self.string = string

    def eval(self):
        return str(self.string)

    def __str__(self):
        return str(self.string)

class Statement:
    @staticmethod
    def parse(environment = {}):
        if isinstance(Parser.get_token(), IdentToken):
            if isinstance(Parser.get_relative_token(1), LeftParenToken):
                return FunctionCallStatement.parse()
            elif isinstance(Parser.get_relative_token(1), AssignToken):
                return AssignmentStatement.parse()
            else:
                raise ParserWrongTokenException(Parser.get_token(), "2ndidentstatement")
        elif isinstance(Parser.get_token(), IfToken):
            try:
                return IfElseStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, IfElseStatement")
                raise e
        elif isinstance(Parser.get_token(), DoToken):
            try:
                return DoWhileStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, DoWhileStatement")
                raise e
        elif isinstance(Parser.get_token(), WhileToken):
            try:
                return WhileStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, WhileStatement")
                raise e
        elif isinstance(Parser.get_token(), ReturnToken):
            try:
                return ReturnStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, ReturnStatement")
                raise e
        elif isinstance(Parser.get_token(), DeclareToken):
            try:
                return DeclareStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, ReturnStatement")
                raise e
        elif isinstance(Parser.get_token(), SwitchToken):
            try:
                return SwitchStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, SwitchStatement")
                raise e
        elif isinstance(Parser.get_token(), FallThroughToken):
            try:
                return FallThroughStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, FallThroughStatement")
                raise e
        elif isinstance(Parser.get_token(), BreakToken):
            try:
                return BreakStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, BreakStatement")
                raise e
        else:
            raise ParserWrongTokenException(Parser.get_token(), "StatementStartingToken")

    @staticmethod
    def able_to_start():
        return type(Parser.get_token()) in StatementStartingTokens



class AssignmentStatement(Statement):
    ident = None
    expression = None

    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

    @staticmethod
    def parse(environment = {}):
        staticIdent = None
        staticExpression = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        expect_token(AssignToken)

        try:
            staticExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing AssignmentStatement expression")
            raise e

        expect_token(SemiColonToken)

        return AssignmentStatement(staticIdent, staticExpression)

    def __str__(self):
        return "%s = %s" % (self.ident, self.expression)

class CallArguments:
    callExpressions = []

    def __init__(self, callExpressions):
        self.callExpressions = callExpressions

    @staticmethod
    def parse(environment = {}):
        staticCallExpressions = []

        if isinstance(Parser.get_token(), RightParenToken):
            pass
        else:
            try:
                nextStaticCallExpression = Expression.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing CallArguments expression no: " + str(1 + len(staticCallExpressions)))
                raise e
            staticCallExpressions.append(nextStaticCallExpression)

        while isinstance(Parser.get_token(), CommaToken):
            Parser.advance_token()
            staticCallExpressions.append(Expression.parse())

        return CallArguments(staticCallExpressions)

    def __str__(self):
        num = 0
        s = ""
        for ce in self.callExpressions:
            if num != 0:
                s += ", "
            s += str(ce)
            num += 1
        return s

class DeclareStatement(Statement):
    typeAndName = None
    value = None

    def __init__(self, typeAndName, value):
        self.typeAndName = typeAndName
        self.value = value

    @staticmethod
    def parse(environment = {}):
        staticTypeAndName = None
        staticValue = None

        expect_token(DeclareToken)

        try:
            staticTypeAndName = TypeAndName.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing DeclareStatement type and name")
            raise e

        if isinstance(Parser.get_token(), AssignToken):
            Parser.advance_token()
            try:
                staticValue = PrimaryExpression.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing DeclareStatement value")
                raise e

        expect_token(SemiColonToken)

        return DeclareStatement(staticTypeAndName, staticValue)

    def __str__(self):
        if self.value:
            return "declare %s = %s;" % (self.typeAndName, self.value)
        else:
            return "declare %s;" % self.typeAndName

class TypeAndName:
    valueType = None
    valueName = None

    def __init__(self, valueType, valueName):
        self.valueType = valueType
        self.valueName = valueName

    @staticmethod
    def parse(environment = {}):
        staticValueType = None
        staticValueName = None

        try:
            staticValueType = Type.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing TypeAndName type")
            raise e

        if isinstance(Parser.get_token(), IdentToken):
            staticValueName = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        return TypeAndName(staticValueType, staticValueName)

    def __str__(self):
        return str(self.valueType) + " " + str(self.valueName)

    def to_key(self):
        return (str(self.valueType), str(self.valueName))

class Type:
    name = None
    arrayDimension = 0

    def __init__(self, name, arrayDimension):
        self.name = name
        self.arrayDimension = arrayDimension

    @staticmethod
    def parse(environment = {}):
        staticName = None
        staticArrayDimension = 0

        if isinstance(Parser.get_token(), IdentToken):
            staticName = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        while isinstance(Parser.get_token(), LeftSquareToken):
            Parser.advance_token()
            if isinstance(Parser.get_token(), RightSquareToken):
                Parser.advance_token()
                staticArrayDimension += 1
            else:
                raise ParserWrongTokenException(Parser.get_token(), RightSquareToken)

        return Type(staticName, staticArrayDimension)

    def __str__(self):
        s = str(self.name)
        for x in range(0, self.arrayDimension):
            s += "[]"
        return s

class FunctionSignatureArguments:
    signatureArguments = []

    def __init__(self, signatureArguments):
        self.signatureArguments = signatureArguments

    @staticmethod
    def parse(environment = {}):
        staticFunctionSignatureArguments = []

        if isinstance(Parser.get_token(), IdentToken):
            staticTypeAndName = TypeAndName.parse()
            staticFunctionSignatureArguments.append(staticTypeAndName)
        elif isinstance(Parser.get_token(), RightParenToken):
            return FunctionSignatureArguments(staticFunctionSignatureArguments)
        else:
            raise ParserWrongTokenException(Parser.get_token(), "FunctionDeclareArgumentsContinueToken")

        while isinstance(Parser.get_token(), CommaToken):
            Parser.advance_token()

            if isinstance(Parser.get_token(), IdentToken):
                staticTypeAndName = TypeAndName.parse()
                staticFunctionSignatureArguments.append(staticTypeAndName)
            else:
                raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        return FunctionSignatureArguments(staticFunctionSignatureArguments)

    def __str__(self):
        num = 0
        s = ""
        for da in self.signatureArguments:
            if num != 0:
                s += ", "
            s += str(da)
            num += 1
        return s

class FallThroughStatement(Statement):
    @staticmethod
    def parse(environment = {}):
        expect_token(FallThroughToken)
        expect_token(SemiColonToken)
        return FallThroughStatement()

    def __str__(self):
        return "fallthrough"

class BreakStatement(Statement):
    @staticmethod
    def parse(environment = {}):
        expect_token(BreakToken)
        expect_token(SemiColonToken)
        return BreakStatement()

    def __str__(self):
        return "break"

class DoWhileStatement(Statement):
    doStatements = None
    whileExpression = None

    def __init__(self, doStatements, whileExpression):
        self.doStatements = doStatements
        self.whileExpression = whileExpression

    @staticmethod
    def parse(environment = {}):
        staticDoStatements = None
        staticWhileExpression = None

        expect_token(DoToken)

        expect_token(LeftBraceToken)

        try:
            staticDoStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing DoWhileStatment do statements")
            raise e

        expect_token(RightBraceToken)

        expect_token(WhileToken)

        expect_token(LeftParenToken)

        try:
            staticWhileExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing DoWhileStatement while expression")
            raise e

        expect_token(RightParenToken)

        return DoWhileStatement(staticDoStatements, staticWhileExpression)

    def __str__(self):
        return "do { %s } while (%s)" % (self.doStatements, self.whileExpression)

class FunctionDeclaration:
    typeAndName = None
    signatureArguments = None

    # Link to the definition of this function
    definition = None

    def __init__(self, typeAndName, signatureArguments):
        self.typeAndName = typeAndName
        self.signatureArguments = signatureArguments

    @staticmethod
    def parse(environment = {}):
        staticFunctionTypeAndName = None
        staticFunctionSignatureArguments = None

        expect_token(DeclareToken)

        expect_token(FunctionToken)

        if isinstance(Parser.get_token(), IdentToken):
            staticFunctionTypeAndName = TypeAndName.parse()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        expect_token(LeftParenToken)

        try:
            staticFunctionSignatureArguments = FunctionSignatureArguments.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Function declare arguments")
            raise e

        expect_token(RightParenToken)

        expect_token(SemiColonToken)

        return FunctionDeclaration(staticFunctionTypeAndName, staticFunctionSignatureArguments)

    def __str__(self):
        return "function %s(%s);\n" % (self.typeAndName, self.signatureArguments)

class FunctionDefinition:
    typeAndName = None
    signatureArguments = None
    statements = None

    # Link to the declaration of this function
    declaration = None

    def __init__(self, typeAndName, signatureArguments, statements):
        self.typeAndName = typeAndName
        self.signatureArguments = signatureArguments
        self.statements = statements

    @staticmethod
    def parse(environment):
        staticTypeAndName = None
        staticSignatureArguments = None
        staticStatements = None

        expect_token(FunctionToken)

        if isinstance(Parser.get_token(), IdentToken):
            staticTypeAndName = TypeAndName.parse()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        expect_token(LeftParenToken)

        try:
            staticSignatureArguments = FunctionSignatureArguments.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Function declare arguments")
            raise e

        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        try:
            staticStatements = Statements.parse(environment)
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Function statements")
            raise e

        expect_token(RightBraceToken)

        return FunctionDefinition(staticTypeAndName, staticSignatureArguments, staticStatements)

    def __str__(self):
        return "function %s(%s) {\n%s}\n" % (self.typeAndName, self.signatureArguments, self.statements)



class FunctionCallStatement(Statement):
    ident = None
    callArguments = None

    # Link to the declaration of this function
    declaration = None

    def __init__(self, ident, callArguments):
        self.ident = ident
        self.callArguments = callArguments

    @staticmethod
    def parse(environment = {}):
        staticIdent = None
        staticCallArguments = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        expect_token(LeftParenToken)

        try:
            staticCallArguments = CallArguments.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing FunctionCallStatement call arguments")
            raise e

        expect_token(RightParenToken)

        expect_token(SemiColonToken)

        return FunctionCallStatement(staticIdent, staticCallArguments)

    def __str__(self):
        return "%s(%s);" % (str(self.ident), str(self.callArguments))

class IfElseStatement(Statement):
    ifThens = []
    elseStatements = None

    def __init__(self, ifThens, elseStatements):
        self.ifThens = ifThens
        self.elseStatements = elseStatements

    @staticmethod
    def parse(environment = {}):
        staticIfThens = []
        staticElseStatements = None

        expect_token(IfToken)

        try:
            staticFirstIf = IfThen.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing IfElseStatement if condition-statements")
            raise e
        staticIfThens.append(staticFirstIf)

        while isinstance(Parser.get_token(), ElifToken):
            Parser.advance_token()
            try:
                staticNextIf = IfThen.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing IfElseStatement elif condition-statement no " + str(2 + len(staticIfThens)))
            staticIfThens.append(staticNextIf)

        if isinstance(Parser.get_token(), ElseToken):
            Parser.advance_token()
        elif Statement.able_to_start() or isinstance(Parser.get_token(), RightBraceToken):
            # If this is just an 'if' with no 'else'
            return IfElseStatement(staticIfThens, None)
        else:
            raise ParserWrongTokenException(Parser.get_token(), ElseToken)

        expect_token(LeftBraceToken)

        try:
            staticElseStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing IfElseStatement then statements")
            raise e

        expect_token(RightBraceToken)

        return IfElseStatement(staticIfThens, staticElseStatements)

    def __str__(self):
        s = ""
        no = 0
        for ifthen in self.ifThens:
            if no == 0:
                s += "if %s" % ifthen
            else:
                s += "elif %s" % ifthen
            no += 1
        if self.elseStatements:
            s += "else {\n%s}" % self.elseStatements
        return s

class IfThen:
    condition = None
    then = None

    def __init__(self, condition, then):
        self.condition = condition
        self.then = then

    @staticmethod
    def parse(environment = {}):
        staticCondition = None
        staticThen = None

        expect_token(LeftParenToken)

        try:
            staticCondition = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing IfThen condition")
            raise e

        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        try:
            staticThen = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing IfThen statements")
            raise e

        expect_token(RightBraceToken)

        return IfThen(staticCondition, staticThen)

    def __str__(self):
        s = "(" + str(self.condition) + ") {\n"
        s += str(self.then)
        s += "\n}"
        return s

class Program:
    functionDeclarations = []
    globalVariableDeclarations = []
    functionDefinitions = []

    def __init__(self, functionDeclarations, globalVariableDeclarations, functionDefinitions):
        self.functionDeclarations = functionDeclarations
        self.globalVariableDeclarations = globalVariableDeclarations
        self.functionDefinitions = functionDefinitions

    @staticmethod
    def parse(environment = {}):
        staticFunctionDeclarations = []
        staticGlobalVariableDeclarations = []
        staticFunctionDefinitions = []

        # Parse all function and global variable declarations
        while isinstance(Parser.get_token(), DeclareToken):
            if isinstance(Parser.get_relative_token(1), FunctionToken):
                try:
                    nextFunctionDeclaration = FunctionDeclaration.parse()
                    staticFunctionDeclarations.append(nextFunctionDeclaration)
                except ParserException as e:
                    print("Caught " + str(e) + " while parsing Program function\
                         declaration no " + str(1 + len(staticFunctionDeclarations)))
                    raise e
            else:
                try:
                    nextGlobalVariableDeclaration = DeclareStatement.parse()
                    staticGlobalVariableDeclarations.append(\
                        nextGlobalVariableDeclaration)
                except ParserException as e:
                    print("Caught " + str(e) + " while parsing Program global \
                        variable declaration no " \
                        + str(1 + len(staticGlobalVariableDeclarations)))
                    raise e

        # Once all the declarations have been made, it is now necessary to
        # create the program 'environment'. This is a dictionary of types and
        # names to the declaration object. To create it, iterate over the lists
        # and for each declaration, create a tuple of type and name to use as
        # the key.

        environment = {}

        for fdeclare in staticFunctionDeclarations:
            tan = fdeclare.typeAndName
            k = tan.to_key()
            environment[k] = fdeclare

        for vdeclare in staticGlobalVariableDeclarations:
            tan = vdeclare.typeAndName
            k = tan.to_key()
            environment[k] = vdeclare

        print("Current environment after declarations: ")
        print(environment)

        # Parser all function definitions
        while Parser.has_another_token():
            if isinstance(Parser.get_token(), FunctionToken):
                try:
                    nextFunctionDefinition = FunctionDefinition.parse(environment)
                    staticFunctionDefinitions.append(nextFunctionDefinition)
                except ParserException as e:
                    print("Caught " + str(e) + " while parsing Program function/declaration no " + str(1 + len(staticFuncsAndDeclarations)))
                    raise e
            else:
                raise ParserWrongTokenException(Parser.get_token(), FunctionToken)

        return Program(staticFunctionDeclarations, staticGlobalVariableDeclarations, staticFunctionDefinitions)

    def __str__(self):
        print("program info: no fdeclares: %d, no vdeclares: %d, no fdefines: %d" % (len(self.functionDeclarations), len(self.globalVariableDeclarations), len(self.functionDefinitions)))
        s = ""
        for fdeclare in self.functionDeclarations:
            s += str(fdeclare) + "\n"
        for vdeclare in self.globalVariableDeclarations:
            s += str(vdeclare) + "\n"
        for fdefine in self.functionDefinitions:
            s += str(fdefine) + "\n"
        return s

class ReturnStatement:
    expression = None

    def __init__(self, expression):
        self.expression = expression

    @staticmethod
    def parse(environment = {}):
        staticExpression = None

        expect_token(ReturnToken)

        try:
            staticExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Return expression")
            raise e

        expect_token(SemiColonToken)

        return ReturnStatement(staticExpression)

    def __str__(self):
        return "return %s;" % self.expression

class Statements:
    statements = []

    def __init__(self, statements):
        self.statements = statements

    @staticmethod
    def parse(environment = {}):
        staticStatements = []
        while Statement.able_to_start():
            try:
                nextStaticStatement = Statement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statements statement no " + str(1 + len(staticStatements)))
                raise e
            staticStatements.append(nextStaticStatement)
        return Statements(staticStatements)

    def __str__(self):
        s = ""
        for statement in self.statements:
            s += str(statement)
            s += '\n'
        return s

class SwitchStatement(Statement):
    switchExpression = None
    cases = []
    default = None

    def __init__(self, switchExpression, cases, default):
        self.switchExpression = switchExpression
        self.cases = cases
        self.default = default

    @staticmethod
    def parse(environment = {}):
        staticSwitchExpression = None
        staticCases = []
        staticDefault = None

        expect_token(SwitchToken)

        expect_token(LeftParenToken)

        try:
            staticSwitchExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing SwitchStatement switch expression")
            raise e

        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        while isinstance(Parser.get_token(), CaseToken):
            try:
                nextStaticCase = CaseNotAStatement.parse()
                staticCases.append(nextStaticCase)
            except ParserException as e:
                print("Caught " + str(e) + " while parsing SwitchStatement case not-a-statement no " + str(1 + len(staticCases)))
                raise e

        if isinstance(Parser.get_token(), DefaultToken):
            try:
                staticDefault = DefaultNotAStatement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing SwitchStatement default not-a-statement")
                raise e

        expect_token(RightBraceToken)

    def __str__(self):
        s = "switch (%s) {\n" % self.expression
        for c in self.cases:
            s += "%s\n" % str(c)
        if self.default:
            s += "%s\n" % str(c)
        return c

class CaseNotAStatement:
    primaryExpression = None
    statements = None

    def __init__(self, primaryExpression, statements):
        self.primaryExpression = primaryExpression
        self.statements = statements

    @staticmethod
    def parse(environment = {}):
        staticPrimaryExpression = None
        staticStatements = None

        expect_token(CaseToken)

        try:
            staticPrimaryExpression = PrimaryExpression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing CaseNotAStatement case expression")
            raise e

        expect_token(ColonToken)

        try:
            staticStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing CaseNotAStatement case statements")
            raise e

        return CaseNotAStatement(staticPrimaryExpression, staticStatements)

    def __str__(self):
        return "case %s: %s" % (self.primaryExpression, self.statements)

class DefaultNotAStatement:
    statements = None

    def __init__(self, statements):
        self.statements = statements

    @staticmethod
    def parse(environment = {}):
        staticStatements = None

        expect_token(DefaultToken)

        expect_token(ColonToken)

        try:
            staticStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing CaseNotAStatement case statements")
            raise e

        return DefaultNotAStatement(staticStatements)

    def __str__(self):
        return "default: %s" % self.statements

class WhileStatement(Statement):
    whileExpression = None
    doStatements = None

    def __init__(self, whileExpression, doStatements):
        self.whileExpression = whileExpression
        self.doStatements = doStatements

    @staticmethod
    def parse(environment = {}):
        staticWhileExpression = None
        staticDoStatements = None

        expect_token(WhileToken)

        expect_token(LeftParenToken)

        try:
            staticWhileExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing WhileStatement while expression")
            raise e

        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        try:
            staticDoStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing WhileStatement statements")
            raise e

        expect_token(RightBraceToken)

        return WhileStatement(staticWhileExpression, staticDoStatements)

    def __str__(self):
        return "while (" + str(self.whileExpression) + ") do {\n" + str(self.doStatements) + "}"
