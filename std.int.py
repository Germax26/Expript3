from exp_error import *
from exp_context import *
from exp_variable import *
from exp_info import *
from exp_package import *

def stringify(x): return str(type(x))[8:-2].split('.')[-1]

class INTERPRETER:
    def __init__(self, lexer, parser):
        self.lexer = lexer
        self.parser = parser

    def interpret(self, source, root, categories, variables=VARIABLE_LIST(), depth=0):
        if root.is_op:
            if root.left:
                for category in categories.binary:
                    if category.contains(root.value):
                        operator = category[root.value]

                        operands = [None, None]

                        if "left" not in operator.tags:
                            operands[0], err = self.interpret(source, root.left, categories, variables, depth+1)
                            if err: return None, err

                        if "right" not in operator.tags:
                            operands[1], err = self.interpret(source, root.right, categories, variables, depth+1)
                            if err: return None, err

                        types = [type(operand) for operand in operands]

                        for valid_type in operator.valid:
                            if "left" in operator.tags or issubclass(types[0], valid_type[0]):
                                if "right" in operator.tags or issubclass(types[1], valid_type[-1]):
                                    break
                        else:
                            if operator.valid:
                                return None, InterpreterError(f"Invalid types. Got types {stringify(operands[0])}, {stringify(operands[1])}.", *root.uberspan(), source, "InvalidTypesError")

                        context = Context(self, root, operands, variables, source, categories)
                        return operator.function(*operands, context)
                else:
                    _, err = self.interpret(source, root.left, categories, variables, depth+1)
                    if err: return None, err
                    return None, InterpreterError(f"Unknown binary operator '{root.value}'.", *root.span, source, "UnknownBinaryOperatorError")
            else:
                # return not_implemented("Unary operators are not implemented.", *root.uberspan(), source, "interpreter")

                if categories.unary.contains(root.value):
                    operator = categories.unary[root.value]

                    right = None

                    if "right" not in operator.tags:
                        right, err = self.interpret(source, root.right, categories, variables, depth+1)
                        if err: return None, err

                        type_right = type(right)

                        for valid_type in operator.valid:
                            if issubclass(type_right, valid_type):
                                break
                        else:
                            return None, InterpreterError("Invalid type.",root.span_left, root.right_span(), source, "InvalidTypeError")
                        
                    context = Context(self, root, [None, right], variables, source, categories)
                    return operator.function(right, context)

                else:
                    return None, InterpreterError(f"Unknown unary operator '{root.value}'.", *root.span, source, "UnknownUnaryOperatorError")
        else:
            if root.value in variables:
                return variables[root.value]()
            
            if root.value.isnumeric():
                if root.value.count('0') == len(root.value): return 0, None
                return eval((x:=root.value.lstrip("0"))), None

            if root.value[0] + root.value[-1] == '""':
                return root.value[1:-1], None

            return None, InterpreterError(f"Undefined variable '{root.value}'.", *root.span, source, "UndefinedVariableError")

std_int = module(INTERPRETER)

info = package_info(std_int, "std.int@v1 –– the standard interpreter", [exp_error, exp_context, exp_variable, exp_info])

if __name__ == "__main__": info()