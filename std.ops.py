from exp_category import *
from exp_error import *
from exp_info import *

class Binding:
    pass

class Function:
    pass

class Operators:
    class Unary: # [ ]
        pass 
    class Binary: # [ ]
        class Special: # [-]
            class Radix: # [.]
                pass
            class Application: # [ ]
                tags = ["right"]
                valid = [[Function]]

        class Mathematics: # [-]
            class Arithmetic: # [-]
                class Primary: # [x]
                    class Addition: # [x]
                        tags = []
                        valid = [[int, int], [float, float], [int, float], [float, int], [str, str], [list, list]]
                        def function(left, right, _):
                            return left + right, None
                    class Subtraction: # [x]
                        tags = []
                        valid = [[int, int], [float, float], [int, float], [float, int]]
                        def function(left, right, _):
                            return left - right, None
                class Secondary: # [-]
                    class Multiplication: # [x]
                        tags = []
                        valid = [[int, int], [float, float], [int, float], [float, int], [str, int], [list, int]]
                        def function(left, right, _):
                            return left * right, None
                    class Division: # [x]
                        tags = []
                        valid = [[int, int], [float, float], [int, float], [float, int]]
                        def function(left, right, _):
                            if right == 0:
                                return None, InterpreterError("Cannot divide by 0.", _.self.span_left, _.self.right.left_span() + _.self.right.right_span() - _.self.span_left, _.expr, "DivisionByZeroError")
                            return left / right, None
                    class Modulo: # [.]
                        pass
                    class Quotient: # [.]
                        pass
                class Tertiary: # [.]
                    pass
            class Trigenometry: # [.]
                pass

        class Boolean: # [-]
            class Comparisions: # [x]
                class LessThan: # [x]
                    tags = []
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left < right, None
                class LessThanOrEqualTo: # [x]
                    tags = []
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left <= right, None
                class GreaterThan: # [x]
                    tags = []
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left > right, None
                class GreaterThanOrEqualTo: # [x]
                    tags = []
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left >= right, None
                class EqualTo: # [x]
                    tags = []
                    valid = [[object, object]]
                    def function(left, right, _):
                        return left == right, None
                class NotEqualTo: # [x]
                    tags = []
                    valid = [[object, object]]
                    def function(left, right, _):
                        return left != right, None
            class Bitwise: # [.]
                class And: # [ ]
                    pass
                class Or: # [ ]
                    pass
            class Tests: # [.]
                pass
        class Lambda: # [-]
            tags = ["left", "right"]
            valid = []
            def function(_, __, context):
                return None, InterpreterError("Lambda expressions are not implemented.", *context.self.uberspan(), context.expr, "LambdaExpressionsAreNotImplementedError")

        class Binding: # [ ]
            pass

        class Sequention: # [ ]
            pass
class OPERATORS:
    def __init__(self):
        self.unary = [Category("unary")
            
        ][0]
        self.binary = [
            Category("Special")
                .add(".", Operators.Binary.Special.Radix)
                .add("<-", Operators.Binary.Special.Application),

            Category("Mathematics.Arithmetic.Tertiary"),

            Category("Mathematics.Arithmetic.Secondary")
                .add("*", Operators.Binary.Mathematics.Arithmetic.Secondary.Multiplication)
                .add("/", Operators.Binary.Mathematics.Arithmetic.Secondary.Division)
                .add("%", Operators.Binary.Mathematics.Arithmetic.Secondary.Modulo),

            Category("Mathematics.Arithmetic.Primary")
                .add("+", Operators.Binary.Mathematics.Arithmetic.Primary.Addition)
                .add("-", Operators.Binary.Mathematics.Arithmetic.Primary.Subtraction),

            Category("Boolean.Bitwise"),

            Category("Boolean.Tests"),

            Category("Boolean.Comparisions")
                .add("<", Operators.Binary.Boolean.Comparisions.LessThan)
                .add("<=", Operators.Binary.Boolean.Comparisions.LessThanOrEqualTo)
                .add(">", Operators.Binary.Boolean.Comparisions.GreaterThan)
                .add(">=", Operators.Binary.Boolean.Comparisions.GreaterThanOrEqualTo)
                .add("==", Operators.Binary.Boolean.Comparisions.EqualTo)
                .add("!=", Operators.Binary.Boolean.Comparisions.NotEqualTo),

            Category("Lambda", "reverse-collapse")
                .add("=>", Operators.Binary.Lambda),

            Category("Binding"),

            Category("Sequention")
        ]

std_ops = module(OPERATORS)

info = package_info(std_ops, "std.ops@v2 –– the standard operators", [exp_category, exp_error, exp_info])

if __name__ == "__main__": info()