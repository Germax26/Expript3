from exp_category import *
from exp_error import *
from exp_info import *

class Operators:
    class Unary:
        class Positive:
            valid = [int, float] 
            def function(right, _):
                return +right, None
        class Negative:
            valid = [int, float]
            def function(right, _):
                return -right, None
        class Negation:
            valid = [bool]
            def function(right, _):
                return not right, None
    class Binary:
        class Radix:
            tags = ["right", bool]
            valid = [[int]]
            def function(left, _, context):
                if context.right.value.isdigit():
                    return eval(f"{left}.{context.right.value}"), None # decimals
                return None, InterpreterError("Illegal postradix, expected digits.", *context.right.uberspan(), context.expr, "IllegalPostradixError")

        class Mathematics:
            class Arithmetic:
                class Primary:
                    class Addition:
                        valid = [[int, int], [float, float], [int, float], [float, int], [str, str], [tuple, tuple]]
                        def function(left, right, _):
                            return left + right, None
                    class Subtraction:
                        valid = [[int, int], [float, float], [int, float], [float, int]]
                        def function(left, right, _):
                            return left - right, None
                class Secondary:
                    class Multiplication:
                        valid = [[int, int], [float, float], [int, float], [float, int], [str, int], [tuple, int]]
                        def function(left, right, _):
                            return left * right, None
                    class Division:
                        valid = [[int, int], [float, float], [int, float], [float, int]]
                        def function(left, right, _):
                            if right == 0:
                                return None, InterpreterError("Cannot divide by 0.", _.self.span_left, _.self.right.left_span() + _.self.right.right_span() - _.self.span_left, _.expr, "DivisionByZeroError")
                            return left / right, None
                    class Modulo:
                        pass
                    class Quotient:
                        pass
                class Tertiary:
                    class Exponentiation:
                        valid = [[int, int], [float, float], [int, float], [float, int]]
                        def function(left, right, _):
                            return left ** right, None

        class Boolean:
            class Comparisions:
                class LessThan:
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left < right, None
                class LessThanOrEqualTo:
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left <= right, None
                class GreaterThan:
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left > right, None
                class GreaterThanOrEqualTo:
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left >= right, None
                class EqualTo:
                    valid = [[object, object]]
                    def function(left, right, _):
                        return left == right, None
                class NotEqualTo:
                    valid = [[object, object]]
                    def function(left, right, _):
                        return left != right, None
            class Bitwise:
                class And:
                    pass
                class Or:
                    pass
            class Operators:
                class And:
                    pass
                class Or:
                    pass
    
class OPERATORS(CategoryList):
    def __init__(self):
        self.categories = [
            Category("radix")
                .add(".", Operators.Binary.Radix),
            
            Category("unary", "unary")
                .add('+', Operators.Unary.Positive)
                .add("-", Operators.Unary.Negative)
                .add("!", Operators.Unary.Negation),

            Category("mathematics.arithmetic.tertiary")
                .add("**", Operators.Binary.Mathematics.Arithmetic.Tertiary.Exponentiation),

            Category("mathematics.arithmetic.secondary")
                .add("*", Operators.Binary.Mathematics.Arithmetic.Secondary.Multiplication)
                .add("/", Operators.Binary.Mathematics.Arithmetic.Secondary.Division)
                .add("%", Operators.Binary.Mathematics.Arithmetic.Secondary.Modulo),

            Category("mathematics.arithmetic.primary")
                .add("+", Operators.Binary.Mathematics.Arithmetic.Primary.Addition)
                .add("-", Operators.Binary.Mathematics.Arithmetic.Primary.Subtraction),

            Category("boolean.bitwise"),

            Category("boolean.comparisions")
                .add("<", Operators.Binary.Boolean.Comparisions.LessThan)
                .add("<=", Operators.Binary.Boolean.Comparisions.LessThanOrEqualTo)
                .add(">", Operators.Binary.Boolean.Comparisions.GreaterThan)
                .add(">=", Operators.Binary.Boolean.Comparisions.GreaterThanOrEqualTo)
                .add("==", Operators.Binary.Boolean.Comparisions.EqualTo)
                .add("!=", Operators.Binary.Boolean.Comparisions.NotEqualTo),

            Category("boolean.operators")
        ]

std_ops = module(OPERATORS)

info = package_info(std_ops, "std.ops@v2.2 –– the standard operators", [exp_category, exp_error, exp_info])

if __name__ == "__main__": info()