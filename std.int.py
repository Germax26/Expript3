from exp_package import *
from exp_context import *
from exp_error import *
from exp_variable import *
from exp_type import *
from exp_info import *

class INTERPRETER:
    def __init__(self, lexer, parser, literals):
        self.lexer = lexer
        self.parser = parser
        self.literals = literals

    def interpret(self, source, root, categories, variables=VARIABLE_LIST(), depth=0):
        if root.is_op:
            for category in categories.categories:
                if category.contains(root.value):
                    if "unary" not in category.tags:
                        if root.left:
                            operator = category[root.value]

                            operands = [None, None]

                            try:
                                operator_tags = operator.tags
                            except AttributeError:
                                operator_tags = {}

                            if "left" not in operator_tags:
                                operands[0], err = self.interpret(source, root.left, categories, variables, depth+1)
                                if err: return None, err

                            if "right" not in operator_tags:
                                operands[1], err = self.interpret(source, root.right, categories, variables, depth+1)
                                if err: return None, err

                            try:
                                operator_valid = operator.valid
                            except AttributeError:
                                return None, OperatorError(f"Unspecified type requirements for binary operator '{root.value}'.\nUnable to complete calculation.", *root.span, source, "UnspecifiedBinaryOperatorTypeRequirementsError")

                            try:
                                if not operator_valid.check(operands):
                                    return None, InterpreterError(f"Invalid types for operator '{root.value}'.\nGot types {stringify(operands[0])}, {stringify(operands[1])}. Expected otherwise.", *root.uberspan(), source, "InvalidTypesError")
                            except Error as err:
                                return None, err
                                
                            context = Context(self, root, operands, variables, source, categories)
                            try:
                                return operator.function(*operands, context)
                            except AttributeError as err:
                                if str(err)[-27:] == "has no attribute 'function'":
                                    return None, OperatorError(f"Unspecified function for binary operator '{root.value}'.\nUnable to complete calculation.", *root.span, source, "UnspecifiedBinaryOperatorFunctionError")
                                raise err
                            except RecursionError:
                                return None, OperatorError("Too much recursion!", *root.span, source, "RecursionError")
                        return None, OperatorError(f"Missing left operand for binary operator '{root.value}'", *root.span, source, "MissingLeftOperandForBinaryOperatorError")
                    elif not root.left:
                        operator = category[root.value]

                        right = None

                        try:
                            operator_tags = operator.tags
                        except AttributeError:
                            operator_tags = []

                        if "right" not in operator_tags:
                            right, err = self.interpret(source, root.right, categories, variables, depth+1)
                            if err: return None, err

                            try:
                                operator_valid = operator.valid
                            except AttributeError:
                                return None, OperatorError(f"Unspecified type requirements for unary operator '{root.value}'.\nUnable to complete calculation.", *root.span, source, "UnspecifiedUnaryOperatorTypeRequirementsError")
                            
                            if not operator_valid.check([None, right]):
                                return None, InterpreterError(f"Invalid type for the '{root.value}' operator.\nGot type {stringify(right)}. Expected otherwise.",root.span_left, root.right_span(), source, "InvalidTypeError")
                            
                        context = Context(self, root, [None, right], variables, source, categories)
                        try:
                            return operator.function(right, context)
                        except AttributeError as err:
                            if str(err)[-27:] == "has no attribute 'function'":
                                return None, OperatorError(f"Unspecified function for unary operator '{root.value}'.\nUnable to complete calculation.", *root.span, source, "UnspecifiedUnaryOperatorFunctionError")
                            raise err
                        
            else:
                return None, InterpreterError(f"Unknown operator '{root.value}'", *root.span, source, "UnknownOperaterError")
        else:
            for literal in self.literals.literals:
                if literal[0](root, variables):
                    return literal[1](root, variables)
            return None, InterpreterError(f"Undefined variable '{root.value}'.", *root.span, source, "UndefinedVariableError")

std_int = module(INTERPRETER)

info = package_info(std_int, "std.int@v1.1 ?????? the standard interpreter", [exp_error, exp_context, exp_variable, exp_info])

if __name__ == "__main__": info()
