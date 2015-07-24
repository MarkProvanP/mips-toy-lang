from lexer.tokens import *

from parser_new.parser_code_new import Parser, ParserException

class Statement:
    @staticmethod
    def parse():
        if isinstance(Parser.get_token(), IdentToken):
            if isinstance(Parser.get_relative_token(1), LeftParenToken):
                return FunctionCallStatement.parse()
            elif isinstance(Parser.get_relative_token(1), AssignToken):
                return AssignmentStatement.parse()
            else:
                raise ParserException(Parser.get_token(), "2ndidentstatement")
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
                return Return.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, ReturnStatement")
                raise e
        elif isinstance(Parser.get_token(), DeclareToken):
            try:
                return Declare.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statement, ReturnStatement")
                raise e
        else:
            raise ParserException(Parser.get_token(), "StatementStartingToken")

    @staticmethod
    def able_to_start():
        return type(Parser.get_token()) in StatementStartingTokens

class Expression:
    @staticmethod
    def parse():
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
    def parse():
        staticPrimaryExpression = None
        if isinstance(Parser.get_token(), NumberToken):
            staticPrimaryExpression = Number(Parser.get_token())
            Parser.advance_token()
        elif isinstance(Parser.get_token(), IdentToken):
            staticPrimaryExpression = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), PrimaryExpression)
        return staticPrimaryExpression


class AssignmentStatement(Statement):
    ident = None
    expression = None

    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

    @staticmethod
    def parse():
        staticIdent = None
        staticExpression = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), AssignToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), AssignToken)

        try:
            staticExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing AssignmentStatement expression")
            raise e

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return AssignmentStatement(staticIdent, staticExpression)

class BinaryExpression(Expression):
    left = None
    operator = None
    right = None

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class CallArguments:
    callExpressions = []

    def __init__(self, callExpressions):
        self.callExpressions = callExpressions

    @staticmethod
    def parse():
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

class Declare(Statement):
    typeAndName = None

    def __init__(self, typeAndName):
        self.typeAndName = typeAndName

    @staticmethod
    def parse():
        staticTypeAndName = None

        if isinstance(Parser.get_token(), DeclareToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), DeclareToken)

        try:
            staticTypeAndName = TypeAndName.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Declare type and name")
            raise e

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return Declare(staticTypeAndName)

class TypeAndName:
    valueType = None
    valueName = None

    def __init__(self, valueType, valueName):
        self.valueType = valueType
        self.valueName = valueName

    @staticmethod
    def parse():
        staticValueType = None
        staticValueName = None

        if isinstance(Parser.get_token(), IdentToken):
            staticValueType = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), IdentToken):
            staticValueName = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        return TypeAndName(staticValueType, staticValueName)

class FunctionDeclareArguments:
    defineArguments = []

    def __init__(self, defineArguments):
        self.defineArguments = defineArguments

    @staticmethod
    def parse():
        staticFunctionDeclareArguments = []

        if isinstance(Parser.get_token(), IdentToken):
            staticTypeAndName = TypeAndName.parse()
            staticFunctionDeclareArguments.append(staticTypeAndName)
        elif isinstance(Parser.get_token(), RightParenToken):
            return FunctionDeclareArguments(staticFunctionDeclareArguments)
        else:
            raise ParserException(Parser.get_token(), "FunctionDeclareArgumentsContinueToken")

        while isinstance(Parser.get_token(), CommaToken):
            Parser.advance_token()

            if isinstance(Parser.get_token(), IdentToken):
                staticTypeAndName = TypeAndName.parse()
                staticFunctionDeclareArguments.append(staticTypeAndName)
            else:
                raise ParserException(Parser.get_token(), IdentToken)

        return FunctionDeclareArguments(staticFunctionDeclareArguments)

class DoWhileStatement(Statement):
    doStatements = None
    whileExpression = None

    def __init__(self, doStatements, whileExpression):
        self.doStatements = doStatements
        self.whileExpression = whileExpression

    @staticmethod
    def parse():
        staticDoStatements = None
        staticWhileExpression = None

        if isinstance(Parser.get_token(), DoToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), DoToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        try:
            staticDoStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing DoWhileStatment do statements")
            raise e

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        if isinstance(Parser.get_token(), WhileToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), WhileToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        try:
            staticWhileExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing DoWhileStatement while expression")
            raise e

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        return DoWhileStatement(staticDoStatements, staticWhileExpression)


class Function:
    functionName = None
    functionDeclareArguments = None
    statements = None

    def __init__(self, functionName, functionDeclareArguments, statements):
        self.functionName = functionName
        self.functionDeclareArguments = functionDeclareArguments
        self.statements = statements

    @staticmethod
    def parse():
        staticFunctionName = None
        staticFunctionDeclareArguments = None
        staticStatements = None

        # If a function is being parsed, then we already have a function token
        # here so we don't need to check again
        Parser.advance_token()

        if isinstance(Parser.get_token(), IdentToken):
            staticFunctionName = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        try:
            staticFunctionDeclareArguments = FunctionDeclareArguments.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Function declare arguments")
            raise e

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        try:
            staticStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Function statements")
            raise e

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        return Function(staticFunctionName, staticFunctionDeclareArguments, staticStatements)

class FunctionCallStatement(Statement):
    ident = None
    callArguments = None

    def __init__(self, ident, callArguments):
        self.ident = ident
        self.callArguments = callArguments

    @staticmethod
    def parse():
        staticIdent = None
        staticCallArguments = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IdentToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        try:
            staticCallArguments = CallArguments.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing FunctionCallStatement call arguments")
            raise e

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return FunctionCallStatement(staticIdent, staticCallArguments)

class Ident(PrimaryExpression):
    ident = None

    def __init__(self, ident):
        self.ident = ident

class IfElseStatement(Statement):
    ifThens = []
    elseStatements = None

    def __init__(self, ifThens, elseStatements):
        self.ifThens = ifThens
        self.elseStatements = elseStatements

    @staticmethod
    def parse():
        staticIfThens = []
        staticElseStatements = None

        if isinstance(Parser.get_token(), IfToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), IfToken)

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
            raise ParserException(Parser.get_token(), ElseToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        try:
            staticThenStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing IfElseStatement then statements")
            raise e

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        return IfElseStatement(staticIfThens, staticElseStatements)

class IfThen:
    condition = None
    then = None

    def __init__(self, condition, then):
        self.condition = condition
        self.then = then

    @staticmethod
    def parse():
        staticCondition = None
        staticThen = None

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        try:
            staticCondition = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing IfThen condition")
            raise e

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        try:
            staticThen = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing IfThen statements")
            raise e

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

class Number(PrimaryExpression):
    number = None

    def __init__(self, number):
        self.number = number


class Program:
    functions = []

    def __init__(self, functions):
        self.functions = functions

    @staticmethod
    def parse():
        staticFunctions = []

        while Parser.has_another_token():
            if isinstance(Parser.get_token(), FunctionToken):
                try:
                    nextFunction = Function.parse()
                except ParserException as e:
                    print("Caught " + str(e) + " while parsing Program function no " + str(1 + len(staticFunctions)))
                    raise e
                staticFunctions.append(nextFunction)
            else:
                raise ParserException(Parser.get_token(), FunctionToken)

        return Program(staticFunctions)

class Return:
    expression = None

    def __init__(self, expression):
        self.expression = expression

    @staticmethod
    def parse():
        staticExpression = None

        if isinstance(Parser.get_token(), ReturnToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), ReturnToken)

        try:
            staticExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing Return expression")
            raise e

        if isinstance(Parser.get_token(), SemiColonToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), SemiColonToken)

        return Return(staticExpression)

class Statements:
    statements = []

    def __init__(self, statements):
        self.statements = statements

    @staticmethod
    def parse():
        staticStatements = []
        while Statement.able_to_start():
            try:
                nextStaticStatement = Statement.parse()
            except ParserException as e:
                print("Caught " + str(e) + " while parsing Statements statement no " + str(1 + len(staticStatements)))
                raise e
            staticStatements.append(nextStaticStatement)
        return Statements(staticStatements)

class WhileStatement(Statement):
    whileExpression = None
    doStatements = None

    def __init__(self, whileExpression, doStatements):
        self.whileExpression = whileExpression
        self.doStatements = doStatements

    @staticmethod
    def parse():
        staticWhileExpression = None
        staticDoStatements = None

        if isinstance(Parser.get_token(), WhileToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), WhileToken)

        if isinstance(Parser.get_token(), LeftParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftParenToken)

        try:
            staticWhileExpression = Expression.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing WhileStatement while expression")
            raise e

        if isinstance(Parser.get_token(), RightParenToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightParenToken)

        if isinstance(Parser.get_token(), LeftBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), LeftBraceToken)

        try:
            staticDoStatements = Statements.parse()
        except ParserException as e:
            print("Caught " + str(e) + " while parsing WhileStatement statements")
            raise e

        if isinstance(Parser.get_token(), RightBraceToken):
            Parser.advance_token()
        else:
            raise ParserException(Parser.get_token(), RightBraceToken)

        return WhileStatement(staticWhileExpression, staticDoStatements)
