from exp_error import *
from exp_context import *
from exp_variable import *
from exp_info import *
from exp_package import *

# std_ops = import_packages({"ops": path("std")})["ops"]

def stringify(x): return str(type(x))[8:-2].split('.')[-1]

class INTERPRETER:
    def __init__(self, lexer, parser):
        self.lexer = lexer
        self.parser = parser

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
                                operator_tags = []

                            if "left" not in operator_tags:
                                operands[0], err = self.interpret(source, root.left, categories, variables, depth+1)
                                if err: return None, err

                            if "right" not in operator_tags:
                                operands[1], err = self.interpret(source, root.right, categories, variables, depth+1)
                                if err: return None, err

                            types = [type(operand) for operand in operands]

                            try:
                                operator_valid = operator.valid
                            except AttributeError:
                                return None, OperatorError(f"Unspecified type requirements for binary operator '{root.value}'.\nUnable to complete calculation.", *root.span, source, "UnspecifiedBinaryOperatorTypeRequirementsError")

                            for valid_type in operator_valid:
                                if "left" in operator_tags or isinstance(operands[0], valid_type[0]):
                                    if "right" in operator_tags or isinstance(operands[1], valid_type[-1]):
                                        break
                            else:
                                if operator_valid:
                                    return None, InterpreterError(f"Invalid types for operator '{root.value}'.\nGot types {stringify(operands[0])}, {stringify(operands[1])}. Expected otherwise.", *root.uberspan(), source, "InvalidTypesError")

                            context = Context(self, root, operands, variables, source, categories)
                            try:
                                return operator.function(*operands, context)
                            except AttributeError as err:
                                if str(err)[-27:] == "has no attribute 'function'":
                                    return None, OperatorError(f"Unspecified function for binary operator '{root.value}'.\nUnable to complete calculation.", *root.span, source, "UnspecifiedBinaryOperatorFunctionError")
                                raise err
                        return None, OperatorError(f"Missing left operand for binary operator {root.value}", *root.span, source, "MissingLeftOperandForBinaryOperatorError")
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

                            type_right = type(right)

                            try:
                                operator_valid = operator.valid
                            except AttributeError:
                                return None, OperatorError(f"Unspecified type requirements for unary operator '{root.value}'.\nUnable to complete calculation.", *root.span, source, "UnspecifiedUnaryOperatorTypeRequirementsError")

                            for valid_type in operator_valid:
                                if issubclass(type_right, valid_type):
                                    break
                            else:
                                if operator_valid:
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
            if root.value in variables:
                return variables[root.value]()
            
            if root.value.isnumeric():
                if root.value.count('0') == len(root.value): return 0, None
                return eval(root.value.lstrip("0")), None

            if root.value[0] + root.value[-1] == '""':
                return root.value[1:-1], None

            return None, InterpreterError(f"Undefined variable '{root.value}'.", *root.span, source, "UndefinedVariableError")

std_int = module(INTERPRETER)

info = package_info(std_int, "std.int@v1 –– the standard interpreter", [exp_error, exp_context, exp_variable, exp_info])

if __name__ == "__main__": info()
