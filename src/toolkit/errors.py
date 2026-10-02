class ToolkitError(Exception):
    pass

class CalculatorError(ToolkitError):
    pass

class EmptyExpressionError(CalculatorError):
    pass

class InvalidCharacterError(CalculatorError):
    pass

class MissingOperandError(CalculatorError):
    pass

class MissingOperatorError(CalculatorError):
    pass

class ConsecutiveOperatorsError(CalculatorError):
    pass

class DivisionByZeroError(CalculatorError):
    pass

class InvalidNumberError(CalculatorError):
    pass

class ConverterError(ToolkitError):
    pass

class UnknownUnitError(ConverterError):
    pass

class IncompatibleUnitsError(ConverterError):
    pass

class BelowAbsoluteZeroError(ConverterError):
    pass