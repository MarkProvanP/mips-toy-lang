"""Parser elements module.

This module stores all of the parser element classes, which recursively call
each others' parse() methods to create the overall parse tree.
"""

from abc import ABCMeta, abstractmethod

from lexer_tokens import Token,\
    BoolToken, NumberToken, UIntBase2Token, UIntBase8Token, UIntBase10Token,\
    IntBase10Token, UIntBase16Token, CharToken, StringToken,\
    AssignToken, BreakToken, CaseToken, ColonToken, CommaToken, DeclareToken,\
    DefaultToken, DoToken, ElifToken, ElseToken, FallThroughToken,\
    ForToken, FunctionToken, IdentToken, IfToken, LeftBraceToken,\
    LeftParenToken, LeftSquareToken, OperatorToken, ReturnToken,\
    RightBraceToken, RightParenToken, RightSquareToken, SemiColonToken,\
    SwitchToken, WhileToken,\
    StatementStartingTokens, DefineArgumentContinueTokens

from parser_code import Parser, Environment, ParserException,\
    ParserWrongTokenException, ParserFunctionDefineWithoutDeclareException,\
    ParserFunctionUseWithoutDeclareException,\
    ParserVariableUseWithoutDeclareException


def expect_token(token):
    """Expect a token type.

    Keyword arguments:
    token -- the Token type

    Function which takes a Token type and checks that it is the next Token
    type in the Token stream. Used when a parse() method only needs to check
    the presence of a type of token (e.g. a keyword token) rather than
    needing to do anything special with it. If the correct token is found, it
    is returned.
    """
    if isinstance(Parser.get_token(), token):
        t = Parser.get_token()
        Parser.advance_token()
        return t
    else:
        raise ParserWrongTokenException(Parser.get_token(), token)


class Expression:

    """Expression parsing class.

    Expression.parse() will use the Fraser-Hanson algorithm to parse complex
    series of binary expressions according to the precedence of the operators.

    This class should never be instantiated. It 
    """

    @staticmethod
    def parse(environment=Environment()):
        """Parse an expression."""
        return Expression._fraser_hanson(1, environment)

    @staticmethod
    def _fraser_hanson(k, environment):
        """Use the Fraser-Hanson method to parse binary expression trees.

        This method will parse the tree of binary expressions, expecting to find
        operator tokens between each expression. It will then create the tree
        based on the precedence value set in the OperatorToken class.
        """
        i = 0
        left = None
        operator = None
        right = None
        left = PrimaryExpression.parse(environment)

        i = Parser.get_token().get_precedence()
        while i >= k:
            while Parser.get_token().get_precedence() == i:
                operator = Parser.get_token()
                Parser.advance_token()
                right = Expression._fraser_hanson(i + 1, environment)
                left = BinaryExpression(left, operator, right)
            i -= 1
        return left

    @abstractmethod
    def source_ref(self): pass


class PrimaryExpression(Expression):

    """Primary expression class.

    A primary expression is an expression of only one value, whether that be
    a single character, number, boolean, string or use of an ident as a
    variable.
    """

    @staticmethod
    def parse(environment=Environment()):
        """Parse a primary expression."""
        staticPrimaryExpression = None
        if isinstance(Parser.get_token(), NumberToken):
            staticPrimaryExpression = Number(Parser.get_token())
            Parser.advance_token()
        elif isinstance(Parser.get_token(), IdentToken):
            if isinstance(Parser.get_relative_token(1), LeftSquareToken):
                staticPrimaryExpression = ArrayAccessExpression.parse(
                    environment)
            elif isinstance(Parser.get_relative_token(1), LeftParenToken):
                staticPrimaryExpression = FunctionCallExpression.parse(
                    environment)
            else:
                staticPrimaryExpression = VariableAccessExpression.parse(
                    environment)
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
            raise ParserWrongTokenException(
                Parser.get_token(),
                PrimaryExpression)
        return staticPrimaryExpression

    def eval(self):
        """Evaluate this expression."""
        return None

    @abstractmethod
    def source_ref(self): pass


class BinaryExpression(Expression):

    """Binary expression class.

    A binary expression is of the form: expression operator expression. This 
    class does not have its own parse() static method as parsing must be done in
    the Expression class, which has the necessary Fraser-Hanson algorithm to
    create the right parse tree based on the binary expression's operator
    precedence.
    """

    left = None
    operator = None
    right = None

    def __init__(self, left, operator, right):
        """Construct a binary expression.

        Arguments:
        left -- the expression on the left hand side
        operator -- the operator token in the middle
        right -- the expression on the right hand side
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        """Return a noggin source code representation."""
        return "(" + str(self.left) + " " + str(self.operator) \
            + " " + str(self.right) + ")"

class VariableAccessExpression(PrimaryExpression):

    """A primary expression of a variable access"""
    
    variableName = None
    
    def __init__(self, variableName, declaration):
        self.variableName = variableName
        self.declaration = declaration
    
    @staticmethod
    def parse(environment=Environment()):
        staticVariableName = None
        staticDeclaration = None
        
        try:
            staticVariableName = Name.parse()
        except ParserException as e:
            print("Caught %s while parsing variable access expression"
                % str(e))
            raise e
        
        # Look up environment to see if this function has been declared yet.
        k = str(staticVariableName)
        if not environment.contains(k):
            raise ParserVariableUseWithoutDeclareException(staticVariableName)

        return VariableAccessExpression(
            staticVariableName,
            staticDeclaration)

    def __str__(self):
        return str(self.variableName)
            
class ArrayAccessExpression(PrimaryExpression):

    """A primary expression of an array access."""

    arrayName = None
    levelExpression = []

    def __init__(self, arrayName, levelExpression):
        """Construct an array access expression.

        Arguments:
        arrayName -- the ident of the array variable
        levelExpression -- the list of expressions corresponding to the level
            of the array access. E.g. myArray[1] would have levelExpression
            of [Number] while otherArray[2][4*b] would have levelExpression
            of [Number, BinaryExpression]
        """
        self.arrayName = arrayName
        self.levelExpression = levelExpression

    @staticmethod
    def parse(environment=Environment()):
        """Parse an array access expression."""
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
                nextStaticLevelExpression = Expression.parse(environment)
                staticLevelExpression.append(nextStaticLevelExpression)
            except ParserException as e:
                print(("Caught %s while parsing ArrayAccessExpression level "
                    "expression no: 1")
                    % str(e))
                raise e

            expect_token(RightSquareToken)

        while isinstance(Parser.get_token(), LeftSquareToken):
            Parser.advance_token()
            try:
                nextStaticLevelExpression = Expression.parse(environment)
                staticLevelExpression.append(nextStaticLevelExpression)
            except ParserException as e:
                print(("Caught %s while parsing ArrayAccessExpression level "
                    "expression no: %d")
                    % (str(e),
                        1 + len(staticLevelExpression)))
                raise e

            expect_token(RightSquareToken)

        return ArrayAccessExpression(staticArrayName, staticLevelExpression)

    def __str__(self):
        """Return a noggin source code representation."""
        s = str(self.arrayName)
        for le in self.levelExpression:
            s += '[%s]' % str(le)
        return s


class FunctionCallExpression(PrimaryExpression):

    """Function call class.

    A function call expression is used so the return value of that function can
    be used as an expression term.
    """
    firstToken = None
    lastToken = None
    ident = None
    callArguments = None

    def __init__(
            self,
            firstToken,
            lastToken,
            ident,
            callArguments):
        """Construct a function call expression.

        Arguments:
        ident -- the name ident of the function
        callArguments -- the arguments of the function call
        """
        self.firstToken = firstToken
        self.lastToken = lastToken
        self.ident = ident
        self.callArguments = callArguments

    @staticmethod
    def parse(environment=Environment()):
        """Parse a function call expression."""
        staticFirstToken = None
        staticLastToken = None
        staticIdent = None
        staticCallArguments = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            staticFirstToken = staticIdent
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        expect_token(LeftParenToken)

        try:
            staticCallArguments = CallArguments.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing FunctionCallExpression call arguments"
                % str(e))
            raise e

        staticLastToken = expect_token(RightParenToken)

        return FunctionCallExpression(
            staticFirstToken,
            staticLastToken,
            staticIdent,
            staticCallArguments)

    def __str__(self):
        """Return a noggin source code representation."""
        return "%s(%s);" % (str(self.ident), str(self.callArguments))


class LiteralExpression(PrimaryExpression):

    """Literal expression class.

    A literal expression is an expression where the value is set in the source
    code, e.g. a number literal or a string literal.
    """

    pass


class Bool(LiteralExpression):

    """Boolean literal class."""

    token = None

    def __init__(self, token):
        """Construct a boolean literal.

        Arguments:
        token -- the BoolToken from the original source code
        """
        self.token = token

    def eval(self):
        """Return the original value evaluated as Python."""
        return bool(self.token)

    def __str__(self):
        """Return a noggin source code representation."""
        return str(self.token)

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Bool:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.token.source_ref()))

class Ident(LiteralExpression):

    """Ident class."""

    token = None

    def __init__(self, token):
        """Construct an ident.

        Arguments:
        token -- the IdentToken from the original source code
        """
        self.token = token

    def __str__(self):
        """Return a noggin source code representation."""
        return str(self.token)

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Ident:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.token.source_ref()))


class Number(LiteralExpression):

    """Number literal class."""

    token = None

    def __init__(self, token):
        """Construct a number literal.

        Arguments:
        token -- the NumberToken from the original source code
        """
        self.token = token

    def __str__(self):
        """Return a noggin source code representation."""
        return str(self.token)

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Number:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.token.source_ref()))


class Char(LiteralExpression):

    """Character literal class."""

    token = None

    def __init__(self, token):
        """Construct a char literal.

        Arguments:
        token -- the CharToken from the original source code
        """
        self.token = token

    def eval(self):
        return chr(self.token)

    def __str__(self):
        """Return a noggin source code representation."""
        return str(self.token)

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Char:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.token.source_ref()))

class String(LiteralExpression):

    """String literal class."""

    token = None

    def __init__(self, token):
        self.token = token

    def eval(self):
        return str(self.token)

    def __str__(self):
        """Return a noggin source code representation."""
        return str(self.token)


class Statement:

    """This abstract class is used to parse a statement."""

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of the statement and environment after that statement.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and 
        Environment is the environment representation, mapping names of
        variables and functions to their initial declaration.
        """
        if isinstance(Parser.get_token(), IdentToken):
            if isinstance(Parser.get_relative_token(1), LeftParenToken):
                return FunctionCallStatement.parse(environment)
            elif isinstance(Parser.get_relative_token(1), AssignToken):
                return AssignmentStatement.parse(environment)
            else:
                raise ParserWrongTokenException(Parser.get_token(),
                    "2ndidentstatement")
        elif isinstance(Parser.get_token(), IfToken):
            try:
                return IfElseStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, IfElseStatement"
                    % str(e))
                raise e
        elif isinstance(Parser.get_token(), DoToken):
            try:
                return DoWhileStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, DoWhileStatement"
                    % str(e))
                raise e
        elif isinstance(Parser.get_token(), WhileToken):
            try:
                return WhileStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, WhileStatement"
                    % str(e))
                raise e
        elif isinstance(Parser.get_token(), ReturnToken):
            try:
                return ReturnStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, ReturnStatement"
                    % str(e))
                raise e
        elif isinstance(Parser.get_token(), DeclareToken):
            try:
                return DeclareStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, ReturnStatement"
                    % str(e))
                raise e
        elif isinstance(Parser.get_token(), SwitchToken):
            try:
                return SwitchStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, SwitchStatement"
                    % str(e))
                raise e
        elif isinstance(Parser.get_token(), FallThroughToken):
            try:
                return FallThroughStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, FallThroughStatement"
                    % str(e))
                raise e
        elif isinstance(Parser.get_token(), BreakToken):
            try:
                return BreakStatement.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing Statement, BreakStatement"
                    % str(e))
                raise e
        else:
            raise ParserWrongTokenException(Parser.get_token(),
                "StatementStartingToken")

    @staticmethod
    def able_to_start():
        return type(Parser.get_token()) in StatementStartingTokens

    @abstractmethod
    def source_ref(self): pass


class AssignmentStatement(Statement):
    firstToken = None
    lastToken = None
    ident = None
    expression = None

    def __init__(
        self,
        firstToken,
        lastToken,
        ident,
        expression):
        self.firstToken = firstToken
        self.lastToken = lastToken
        self.ident = ident
        self.expression = expression

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of assignment statement and resulting environment.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and  
        Environment is the environment representation, mapping names of
        variables and functions to their initial declaration.

        An assignment statement will not change the environment, so the original
        one is returned.
        """
        staticFirstToken = None
        staticLastToken = None
        staticIdent = None
        staticExpression = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            staticFirstToken = staticIdent
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        expect_token(AssignToken)

        try:
            staticExpression = Expression.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing AssignmentStatement expression"
                % str(e))
            raise e

        staticLastToken = expect_token(SemiColonToken)

        newStatement = AssignmentStatement(
            staticFirstToken,
            staticLastToken,
            staticIdent,
            staticExpression)

        # An assignment statment will not change the environment, so the 
        # original one is returned alongside the statement.

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        return "%s = %s" % (self.ident, self.expression)


class CallArguments:
    callExpressions = []

    def __init__(self, callExpressions):
        self.callExpressions = callExpressions

    @staticmethod
    def parse(environment=Environment()):
        staticCallExpressions = []

        if isinstance(Parser.get_token(), RightParenToken):
            pass
        else:
            try:
                nextStaticCallExpression = Expression.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing CallArguments expression no: %d"
                    % (str(e),
                        1 + len(staticCallExpressions)))
                raise e
            staticCallExpressions.append(nextStaticCallExpression)

        while isinstance(Parser.get_token(), CommaToken):
            Parser.advance_token()
            staticCallExpressions.append(Expression.parse(environment))

        return CallArguments(staticCallExpressions)

    def __str__(self):
        """Return a noggin source code representation."""
        num = 0
        s = ""
        for ce in self.callExpressions:
            if num != 0:
                s += ", "
            s += str(ce)
            num += 1
        return s


class DeclareStatement(Statement):
    firstToken = None
    lastToken = None
    variableType = None
    variableName = None
    value = None

    def __init__(
            self,
            firstToken,
            lastToken,
            variableType,
            variableName,
            value):
        self.firstToken = firstToken
        self.lastToken = lastToken
        self.variableType = variableType
        self.variableName = variableName
        self.value = value

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of declaration statement and resulting environment.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and  
        Environment is the environment representation, mapping names of 
        variables and functions to their initial declaration.

        A declaration statement will change the environment by adding a new
        declaration, so the returned environment has this added. The changed
        environment is copied before the new key-value pair is added.
        """
        staticFirstToken = None
        staticLastToken = None
        staticVariableType = None
        staticVariableName = None
        staticValue = None

        staticFirstToken = expect_token(DeclareToken)

        try:
            staticVariableType = Type.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing DeclareStatement type" % str(e))
            raise e
        
        try:
            staticVariableName = Name.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing DeclareStatement type" % str(e))
            raise e

        if isinstance(Parser.get_token(), AssignToken):
            Parser.advance_token()
            try:
                staticValue = PrimaryExpression.parse(environment)
            except ParserException as e:
                print("Caught %s while parsing DeclareStatement value" % str(e))
                raise e

        staticLastToken = expect_token(SemiColonToken)

        newStatement = DeclareStatement(
            staticFirstToken,
            staticLastToken,
            staticVariableType,
            staticVariableName,
            staticValue)

        # The declare statement will change the environment.

        newEnvironment = environment.copy()

        newEnvironment.add(str(staticVariableName), newStatement)

        return (newStatement, newEnvironment)

    def __str__(self):
        """Return a noggin source code representation."""
        if self.value:
            return ("declare %s %s = %s;"
                % (self.variableType, self.variableName, self.value))
        else:
            return ("declare %s %s;"
                % (self.variableType, self.variableName))

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Declare statement:\n"
            "%s\n"
            "between token: %s\n"
            "and token: %s\n"
            % (str(self),
                self.firstToken.source_ref(),
                self.lastToken.source_ref()))
            
class Type:
    ident = None
    arrayDimension = 0

    def __init__(self, ident, arrayDimension):
        self.ident = ident
        self.arrayDimension = arrayDimension

    @staticmethod
    def parse(environment=Environment()):
        staticIdent = None
        staticArrayDimension = 0

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        while isinstance(Parser.get_token(), LeftSquareToken):
            Parser.advance_token()
            if isinstance(Parser.get_token(), RightSquareToken):
                Parser.advance_token()
                staticArrayDimension += 1
            else:
                raise ParserWrongTokenException(Parser.get_token(),
                    RightSquareToken)

        return Type(staticIdent, staticArrayDimension)

    def __str__(self):
        """Return a noggin source code representation."""
        s = str(self.ident)
        for x in range(0, self.arrayDimension):
            s += "[]"
        return s

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Type:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.ident.source_ref()))

class Name:
    ident = None

    def __init__(self, ident):
        self.ident = ident

    @staticmethod
    def parse(environment=Environment()):
        ident = None

        if isinstance(Parser.get_token(), IdentToken):
            ident = Ident(Parser.get_token())
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)
        
        return Name(ident)
    
    def __str__(self):
        """Return a noggin source code representation"""
        return str(self.ident)

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Name:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.ident.source_ref()))

class FunctionSignatureDeclare:
    sigVariableType = None
    sigVariableName = None

    def __init__(self, sigVariableType, sigVariableName):
        self.sigVariableType = sigVariableType
        self.sigVariableName = sigVariableName

    @staticmethod
    def parse(environment=Environment()):
        staticSigVariableType = None
        staticSigVariableName = None

        if isinstance(Parser.get_token(), IdentToken):
            try:
                staticSigVariableType = Type.parse()
            except ParserException as e:
                print(("Caught %s while parsing function signature "
                    "declaration - type")
                    % str(e))
                raise e
            try:
                staticSigVariableName = Name.parse()
            except ParserException as e:
                print(("Caught %s while parsing function signature "
                    "declaration - name")
                    % str(e))
                raise e
            return FunctionSignatureDeclare(
                staticSigVariableType,
                staticSigVariableName)

    def __str__(self):
        """Return a noggin source code representation"""
        return "%s %s" % (self.sigVariableType, self.sigVariableName)

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Function signature declare:\n"
            "%s\n"
            "between token: %s\n"
            "and token: %s\n"
            % (str(self),
                self.sigVariableType.source_ref(),
                self.sigVariableName.source_ref()))

class FunctionSignatureArguments:
    signatureArguments = []

    def __init__(self, signatureArguments):
        self.signatureArguments = signatureArguments

    @staticmethod
    def parse(environment=Environment()):
        staticFunctionSignatureArguments = []

        firstSignatureDeclare = FunctionSignatureDeclare.parse()

        if not firstSignatureDeclare:
            # If no signature declaration was parsed
            return FunctionSignatureArguments(staticFunctionSignatureArguments)

        staticFunctionSignatureArguments.append(firstSignatureDeclare)

        while isinstance(Parser.get_token(), CommaToken):
            Parser.advance_token()

            nextSignatureDeclare = FunctionSignatureDeclare.parse()
            staticFunctionSignatureArguments.append(nextSignatureDeclare)

        return FunctionSignatureArguments(staticFunctionSignatureArguments)

    def __str__(self):
        """Return a noggin source code representation."""
        num = 0
        s = ""
        for da in self.signatureArguments:
            if num != 0:
                s += ", "
            s += str(da)
            num += 1
        return s


class FallThroughStatement(Statement):
    token = None

    def __init__(self, token):
        self.token = token

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of fallthrough statement and resulting environment.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and 
        Environment is the environment representation, mapping names of
        variables and functions to their initial declaration.

        A fallthrough statement will not change the environment, so the original
        one is returned.
        """
        staticToken = None

        staticToken = expect_token(FallThroughToken)

        expect_token(SemiColonToken)

        newStatement = FallThroughStatement(staticToken)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        return "fallthrough"

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Fallthrough statement:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.token.source_ref()))


class BreakStatement(Statement):
    token = None

    def __init__(self, token):
        self.token = token

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of break statement and resulting environment.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and 
        Environment is the environment representation, mapping names of 
        variables and functions to their initial declaration.

        A break statement will not change the environment, so the original
        one is returned.
        """
        staticToken = None

        staticToken = expect_token(BreakToken)

        expect_token(SemiColonToken)
        
        newStatement = BreakStatement(staticToken)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        return "break"

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Break statement:\n"
            "%s\n"
            "at token: %s\n"
            % (str(self),
                self.token.source_ref()))


class DoWhileStatement(Statement):
    firstToken = None
    lastToken = None
    doStatements = None
    whileExpression = None

    def __init__(
            self,
            firstToken,
            lastToken,
            doStatements,
            whileExpression):
        self.firstToken = firstToken
        self.lastToken = lastToken
        self.doStatements = doStatements
        self.whileExpression = whileExpression

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of do-while statement and resulting environment.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and 
        Environment is the environment representation, mapping names of
        variables and functions to their initial declaration.

        A do-while statement will not change the environment, so the original
        one is returned.
        """
        staticFirstToken = None
        staticLastToken = None
        staticDoStatements = None
        staticWhileExpression = None

        staticFirstToken = expect_token(DoToken)

        expect_token(LeftBraceToken)

        try:
            staticDoStatements = Statements.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing DoWhileStatment do statements"
                % str(e))
            raise e

        expect_token(RightBraceToken)

        expect_token(WhileToken)

        expect_token(LeftParenToken)

        try:
            staticWhileExpression = Expression.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing DoWhileStatement while expression"
                % str(e))
            raise e

        staticLastToken = expect_token(RightParenToken)

        newStatement = DoWhileStatement(
            staticFirstToken,
            staticLastToken,
            staticDoStatements,
            staticWhileExpression)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        return ("do { %s } while (%s)"
            % (self.doStatements, self.whileExpression))

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Do-while statement:\n"
            "%s\n"
            "between token: %s\n"
            "and token: %s\n"
            % (str(self),
                self.firstToken.source_ref(),
                self.lastToken.source_ref()))

class FunctionDeclaration:
    firstToken = None
    lastToken = None
    functionType = None
    functionName = None
    signatureArguments = None

    # Link to the definition of this function
    definition = None

    def __init__(
            self,
            firstToken,
            lastToken,
            functionType,
            functionName,
            signatureArguments):
        self.firstToken = firstToken
        self.lastToken = lastToken
        self.functionName = functionName
        self.functionType = functionType
        self.signatureArguments = signatureArguments

    @staticmethod
    def parse(environment=Environment()):
        staticFirstToken = None
        staticLastToken = None
        staticFunctionType = None
        staticFunctionName = None
        staticFunctionSignatureArguments = None

        staticFirstToken = expect_token(DeclareToken)

        expect_token(FunctionToken)

        try:
            staticFunctionType = Type.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing Function declaration type" % str(e))
            raise e
        
        try:
            staticFunctionName = Name.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing function declaration name" % str(e))
            raise e

        expect_token(LeftParenToken)

        try:
            staticFunctionSignatureArguments\
                = FunctionSignatureArguments.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing Function declare arguments" % str(e))
            raise e

        expect_token(RightParenToken)

        staticLastToken = expect_token(SemiColonToken)

        return FunctionDeclaration(
            staticFirstToken,
            staticLastToken,
            staticFunctionType,
            staticFunctionName,
            staticFunctionSignatureArguments)

    def __str__(self):
        """Return a noggin source code representation."""
        return ("function %s %s(%s);"
            % (self.functionType, self.functionName, self.signatureArguments))

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return ("Function declaration:\n"
            "%s\n"
            "between token: %s\n"
            "and token: %s\n"
            % (str(self),
                self.firstToken.source_ref(),
                self.lastToken.source_ref()))

class FunctionDefinition:
    firstToken = None
    lastToken = None
    functionType = None
    functionName = None
    signatureArguments = None
    statements = None

    # Link to the declaration of this function
    declaration = None

    def __init__(
            self,
            firstToken,
            lastToken,
            functionType,
            functionName,
            signatureArguments,
            statements,
            declaration):
        self.firstToken = firstToken
        self.lastToken = lastToken
        self.functionType = functionType
        self.functionName = functionName
        self.signatureArguments = signatureArguments
        self.statements = statements
        self.declaration = declaration


    @staticmethod
    def parse(globalEnvironment):
        staticFirstToken = None
        staticLastToken = None
        staticFunctionType = None
        staticFunctionName = None
        staticSignatureArguments = None
        staticStatements = None
        staticDeclaration = None

        staticFirstToken = expect_token(FunctionToken)

        staticFunctionType = Type.parse(globalEnvironment)
        
        staticFunctionName = Name.parse(globalEnvironment)

        # Look up environment to see if this function has been declared yet.
        k = str(staticFunctionName)
        try:
            # Then this function type and name is already in the environment
            staticDeclaration = globalEnvironment.get(k)
        except KeyError as e:
            raise ParserFunctionDefineWithoutDeclareException(
                staticFunctionName)

        expect_token(LeftParenToken)

        try:
            staticSignatureArguments = \
                FunctionSignatureArguments.parse(globalEnvironment)
        except ParserException as e:
            print("Caught %s while parsing Function declare arguments" % str(e))
            raise e

        # Now, after parsing the function arguments, the environment now needs
        # to include these arguments as well as the ones already in the global
        # one.

        functionEnvironment = globalEnvironment.copy()
        for sigDeclare in staticSignatureArguments.signatureArguments:
            sigDeclareName = str(sigDeclare.sigVariableName)
            print("sigDeclareName: %s", sigDeclareName)
            functionEnvironment.add(sigDeclareName, sigDeclare)


        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        try:
            staticStatements = Statements.parse(functionEnvironment)
        except ParserException as e:
            print("Caught %s while parsing Function statements" % str(e))
            raise e

        staticLastToken = expect_token(RightBraceToken)

        return FunctionDefinition(
            staticFirstToken,
            staticLastToken,
            staticFunctionType,
            staticFunctionName,
            staticSignatureArguments,
            staticStatements,
            staticDeclaration)

    def __str__(self):
        """Return a noggin source code representation."""
        return "function %s %s(%s) {\n%s}\n" % (
            self.functionType,
            self.functionName,
            self.signatureArguments,
            self.statements)

    def source_ref(self):
        """Return a string referring to original source code.

        This string will include the original line number and character start
        and end numbers.
        """
        return "Function definition statement: \n"\
            + str(self) + "\n"\
            + "between tokens: %s and %s" % (
                self.firstToken.source_ref(),
                self.lastToken.source_ref())


class FunctionCallStatement(Statement):
    firstToken = None
    lastToken = None
    ident = None
    callArguments = None

    # Link to the declaration of this function
    declaration = None

    def __init__(
            self,
            firstToken,
            lastToken,
            ident,
            callArguments,
            declaration):
        self.firstToken = firstToken
        self.lastToken = lastToken
        self.ident = ident
        self.callArguments = callArguments
        self.declaration = declaration

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of function call statement and resulting environment.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and the 
        Environment is the environment representation, mapping names of variables and
        and functions to their initial declaration.

        A function call statement will not change the environment, so the
        original one is returned.
        """
        staticFirstToken = None
        staticLastToken = None
        staticIdent = None
        staticCallArguments = None
        staticDeclaration = None

        if isinstance(Parser.get_token(), IdentToken):
            staticIdent = Ident(Parser.get_token())
            staticFirstToken = staticIdent
            Parser.advance_token()
        else:
            raise ParserWrongTokenException(Parser.get_token(), IdentToken)

        # Look up environment to see if this function has been declared yet.
        k = str(staticIdent)
        try:
            staticDeclaration = environment.get(k)
            # Then this function type and name is already in the environment
        except KeyError as e:
            raise ParserFunctionUseWithoutDeclareException(staticIdent)

        expect_token(LeftParenToken)

        try:
            staticCallArguments = CallArguments.parse(environment)
        except ParserException as e:
            print(("Caught %s while parsing FunctionCallStatement "
                "call arguments")
                % str(e))
            raise e

        expect_token(RightParenToken)

        expect_token(SemiColonToken)

        newStatement = FunctionCallStatement(
            staticFirstToken,
            staticLastToken,
            staticIdent,
            staticCallArguments,
            staticDeclaration)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        return "%s(%s);" % (str(self.ident), str(self.callArguments))


class IfElseStatement(Statement):
    ifThens = []
    elseStatements = None

    def __init__(self, ifThens, elseStatements):
        self.ifThens = ifThens
        self.elseStatements = elseStatements

    @staticmethod
    def parse(environment=Environment()):
        """Returns tuple of if-else statement and resulting environment.

        A statement, if parsed, could return a changed environment. As a result
        this method will return a tuple of the type:

        (Statement, Environment)

        where the Statement is whatever type of statement was parsed and 
        Environment is the environment representation, mapping names of
        variables and functions to their initial declaration.

        An if-else statement will not change the environment, so the original
        one is returned.
        """
        staticIfThens = []
        staticElseStatements = None

        expect_token(IfToken)

        try:
            staticFirstIf = IfThen.parse(environment)
        except ParserException as e:
            print(("Caught %s while parsing IfElseStatement if "
                "condition-statements")
                % str(e))
            raise e
        staticIfThens.append(staticFirstIf)

        while isinstance(Parser.get_token(), ElifToken):
            Parser.advance_token()
            try:
                staticNextIf = IfThen.parse(environment)
            except ParserException as e:
                print(("Caught %s while parsing IfElseStatement elif "
                    "condition-statement no %d")
                    % (str(e),
                    2 + len(staticIfThens)))
                raise e
            staticIfThens.append(staticNextIf)

        if isinstance(Parser.get_token(), ElseToken):
            Parser.advance_token()
        elif Statement.able_to_start()\
                or isinstance(Parser.get_token(), RightBraceToken):
            # If this is just an 'if' with no 'else'
            newStatement = IfElseStatement(staticIfThens, staticElseStatements)
            # No change to the environment

            return (newStatement, environment)
        else:
            raise ParserWrongTokenException(Parser.get_token(), ElseToken)

        expect_token(LeftBraceToken)

        try:
            staticElseStatements = Statements.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing IfElseStatement then statements"
                % str(e))
            raise e

        expect_token(RightBraceToken)

        newStatement = IfElseStatement(staticIfThens, staticElseStatements)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
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
    def parse(environment=Environment()):
        staticCondition = None
        staticThen = None

        expect_token(LeftParenToken)

        try:
            staticCondition = Expression.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing IfThen condition" % str(e))
            raise e

        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        try:
            staticThen = Statements.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing IfThen statements" % str(e))
            raise e

        expect_token(RightBraceToken)

        return IfThen(staticCondition, staticThen)

    def __str__(self):
        """Return a noggin source code representation."""
        s = "(" + str(self.condition) + ") {\n"
        s += str(self.then)
        s += "\n}"
        return s


class Program:
    functionDeclarations = []
    globalVariableDeclarations = []
    functionDefinitions = []

    def __init__(
            self, functionDeclarations, globalVariableDeclarations,
            functionDefinitions):
        self.functionDeclarations = functionDeclarations
        self.globalVariableDeclarations = globalVariableDeclarations
        self.functionDefinitions = functionDefinitions

    @staticmethod
    def parse(environment=Environment()):
        staticFunctionDeclarations = []
        staticGlobalVariableDeclarations = []
        staticFunctionDefinitions = []

        # As each declaration is made, add to the 'environment' object

        environment = Environment()

        # Parse all function and global variable declarations
        while isinstance(Parser.get_token(), DeclareToken):
            if isinstance(Parser.get_relative_token(1), FunctionToken):
                try:
                    nextFunctionDeclaration = FunctionDeclaration.parse(
                        environment)
                    staticFunctionDeclarations.append(nextFunctionDeclaration)
                    functionName = nextFunctionDeclaration.functionName
                    k = str(functionName)
                    environment.add(k, nextFunctionDeclaration)
                except ParserException as e:
                    print(("Caught %s while parsing Program function "
                        "declaration no %d")
                        % (str(e),
                        1 + len(staticFunctionDeclarations)))
                    raise e
            else:
                try:
                    (nextGblVarDeclare, newEnv) = DeclareStatement.parse(
                        environment)
                    staticGlobalVariableDeclarations.append(nextGblVarDeclare)
                    # the newEnv is the new environment after parsing the
                    # declare statement
                    environment = newEnv
                except ParserException as e:
                    print(("Caught %s while parsing Program global variable "
                        "declaration no %d")
                        % (str(e),
                        1 + len(staticGlobalVariableDeclarations)))
                    raise e

        if Parser.printVerbose:
            print("Current environment after declarations: ")
            print(environment)
            for k, v in environment.items():
                print("Key: ", k)
                print("Value: ", v.source_ref())
                print("-----")

        # Parser all function definitions
        while Parser.has_another_token():
            if isinstance(Parser.get_token(), FunctionToken):
                try:
                    nextFunctionDefinition\
                        = FunctionDefinition.parse(environment)
                    staticFunctionDefinitions.append(nextFunctionDefinition)
                except ParserException as e:
                    print(("Caught %s while parsing Program function "
                        "definition no %d")
                        % (str(e),
                        1 + len(staticFunctionDefinitions)))
                    raise e
            else:
                raise ParserWrongTokenException(
                    Parser.get_token(),
                    FunctionToken)

        return Program(
            staticFunctionDeclarations,
            staticGlobalVariableDeclarations,
            staticFunctionDefinitions
        )

    def __str__(self):
        """Return a noggin source code representation."""
        s = ""
        for fdeclare in self.functionDeclarations:
            s += str(fdeclare) + "\n"
        for vdeclare in self.globalVariableDeclarations:
            s += str(vdeclare) + "\n"
        for fdefine in self.functionDefinitions:
            s += str(fdefine) + "\n"
        return s

    def info_str(self):
        return ("\n"
            "##########################################\n"
            "# Program info:\n"
            "# Number of function declarations: %d\n"
            "# Number of global variables: %d\n"
            "# Number of function definitions: %d\n"
            "##########################################\n"
            % (len(self.functionDeclarations),
                len(self.globalVariableDeclarations),
                len(self.functionDefinitions)))

class ReturnStatement(Statement):
    """Class for a return statement.

    """
    expression = None

    def __init__(self, expression):
        self.expression = expression

    @staticmethod
    def parse(environment=Environment()):
        staticExpression = None

        expect_token(ReturnToken)

        try:
            staticExpression = Expression.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing Return expression" % str(e))
            raise e

        expect_token(SemiColonToken)

        newStatement = ReturnStatement(staticExpression)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        return "return %s;" % self.expression


class Statements:
    statements = []

    def __init__(self, statements):
        self.statements = statements

    @staticmethod
    def parse(environment=Environment()):
        staticStatements = []
        while Statement.able_to_start():
            try:
                # Each statement could change the environment for the next 
                # statements, so each Statement.parse() call returns a tuple
                # of the parsed statement and the environment after that 
                # statement, regardless of whether the environment did change.
                print("Parse Statements, v:")
                v = Statement.parse(environment)
                print("type(v): %s" % type(v))
                (nextStaticStatement, newEnv) = v
            except ParserException as e:
                print("Caught %s while parsing Statements statement no %d" % (
                    str(e),
                    1 + len(staticStatements)))
                raise e
            staticStatements.append(nextStaticStatement)
        return Statements(staticStatements)

    def __str__(self):
        """Return a noggin source code representation."""
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
    def parse(environment=Environment()):
        staticSwitchExpression = None
        staticCases = []
        staticDefault = None

        expect_token(SwitchToken)

        expect_token(LeftParenToken)

        try:
            staticSwitchExpression = Expression.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing SwitchStatement switch expression"
                % str(e))
            raise e

        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        while isinstance(Parser.get_token(), CaseToken):
            try:
                nextStaticCase = CaseNotAStatement.parse(environment)
                staticCases.append(nextStaticCase)
            except ParserException as e:
                print(("Caught %s while parsing SwitchStatement case "
                    "not-a-statement no %d")
                    % (str(e),
                    1 + len(staticCases)))
                raise e

        if isinstance(Parser.get_token(), DefaultToken):
            try:
                staticDefault = DefaultNotAStatement.parse(environment)
            except ParserException as e:
                print(("Caught %s while parsing SwitchStatement default "
                    "not-a-statement")
                    % str(e))
                raise e

        expect_token(RightBraceToken)

        newStatement = SwitchStatement(
            staticSwitchExpression,
            staticCases,
            staticDefault)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        s = "switch (%s) {\n" % self.switchExpression
        for c in self.cases:
            s += "%s\n" % str(c)
        if self.default:
            s += "%s\n" % str(c)
        return s


class CaseNotAStatement:
    primaryExpression = None
    statements = None

    def __init__(self, primaryExpression, statements):
        self.primaryExpression = primaryExpression
        self.statements = statements

    @staticmethod
    def parse(environment=Environment()):
        staticPrimaryExpression = None
        staticStatements = None

        expect_token(CaseToken)

        try:
            staticPrimaryExpression = PrimaryExpression.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing CaseNotAStatement case expression"
                % str(e))
            raise e

        expect_token(ColonToken)

        try:
            staticStatements = Statements.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing CaseNotAStatement case statements"
                % str(e))
            raise e

        return CaseNotAStatement(staticPrimaryExpression, staticStatements)

    def __str__(self):
        """Return a noggin source code representation."""
        return "case %s: %s" % (self.primaryExpression, self.statements)


class DefaultNotAStatement:
    statements = None

    def __init__(self, statements):
        self.statements = statements

    @staticmethod
    def parse(environment=Environment()):
        staticStatements = None

        expect_token(DefaultToken)

        expect_token(ColonToken)

        try:
            staticStatements = Statements.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing CaseNotAStatement case statements"
                % str(e))
            raise e

        return DefaultNotAStatement(staticStatements)

    def __str__(self):
        """Return a noggin source code representation."""
        return "default: %s" % self.statements


class WhileStatement(Statement):
    whileExpression = None
    doStatements = None

    def __init__(self, whileExpression, doStatements):
        self.whileExpression = whileExpression
        self.doStatements = doStatements

    @staticmethod
    def parse(environment=Environment()):
        staticWhileExpression = None
        staticDoStatements = None

        expect_token(WhileToken)

        expect_token(LeftParenToken)

        try:
            staticWhileExpression = Expression.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing WhileStatement while expression"
                % str(e))
            raise e

        expect_token(RightParenToken)

        expect_token(LeftBraceToken)

        try:
            staticDoStatements = Statements.parse(environment)
        except ParserException as e:
            print("Caught %s while parsing WhileStatement statements" % str(e))
            raise e

        expect_token(RightBraceToken)

        newStatement = WhileStatement(staticWhileExpression, staticDoStatements)

        # No change to the environment

        return (newStatement, environment)

    def __str__(self):
        """Return a noggin source code representation."""
        return "while (" + str(self.whileExpression) + ") do {\n"\
            + str(self.doStatements) + "}"
