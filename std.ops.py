from exp_category import *
from exp_error import *
from exp_package import *
from exp_variable import *
from exp_info import *

from types import FunctionType

std_lib = import_package(here("std"), "lib")

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
        class Length:
            valid = [tuple, str]
            def function(right, _):
                return len(right), None
        class Reverse:
            valid = [tuple, str]
            def function(right, _):
                return right[::-1], None
    class Binary:
        class Cons:
            valid = [[object, tuple]]
            def function(left, right, context):
                return (left,) + right, None

        class Radix:
            tags = ["right"]
            valid = [[int], [tuple]]
            def function(left, _, context):
                if context.type_left == int: 
                    if context.right.value.isdigit():
                        return eval(f"{left}.{context.right.value}"), None # decimals
                    return None, InterpreterError("Illegal postradix, expected digits.", *context.right.uberspan(), context.expr, "IllegalPostradixError")

                right, err = context.evaluate()
                if err: return None, err

                type_right = type(right)

                if (type_right) != int: 
                    return None, InterpreterError("Illegal index, expected int.", *context.right.uberspan(), context.expr, "IllegalIndexError")
                
                len_left = len(left)
                if right + 1 and right < len_left:
                    return left[right], None

                return None, InterpreterError(f"Index out of range. List was {len_left} element{'s' if len_left > 1 else ''} long.", *context.self.uberspan(), context.expr, "IndexOutOfRangeError")
                
        class Application:
            tags = ["right"]
            valid = [[std_lib.Function], [FunctionType]]
            def function(left, _, context):
                if context.type_left == std_lib.Function:
                    return left(None, context)

                right, err = context.evaluate()
                if err: return None, err

                try:
                    return left(right, context)
                except RecursionError:
                    return None, InterpreterError("Too much recursion.", *context.self.span, context.expr, "RecursionError")

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
            class Trigenometry:
                pass

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
            class Tests:
                pass
        
        class Lambda:
            tags = ["left", "right"]
            valid = []
            def function(_, __, context):
                if context.left.is_op:
                    return None, InterpreterError("An expression cannot be the parameter of a function.", *context.left.uberspan(), context.expr, "ExpressionParameterError")
                return std_lib.Function(context), None

        class Binding:
            tags = ["left", "right"]
            valid = []
            def function(_, __, context):
                if context.left.is_op:
                    return None, InterpreterError("Cannot bind value to expression.", *context.left.uberspan(), context.expr, "CannotAssignToExpressionError")
                return std_lib.Binding(context), None

        class Sequention:
            tags = ["right"]
            valid = [[object]]
            def function(left, _, context):
                if context.type_left == std_lib.Binding:
                    return context.evaluate(variables=context.variables.union(VARIABLE_LIST(left.var)))
                return context.evaluate()

class OPERATORS:
    def __init__(self):
        self.categories = [
            Category("Radix –– Radix operator")
                .add(".", Operators.Binary.Radix),
            
            Category("Unary –– General unary operators", "unary")
                .add('+', Operators.Unary.Positive)
                .add("-", Operators.Unary.Negative)
                .add("!", Operators.Unary.Negation),

            Category("Application –– Application operator")
                .add("<-", Operators.Binary.Application),

            Category("Construct –– List construction operator", "reverse-collapse")
                .add(":", Operators.Binary.Cons),

            Category("Mathematics.Arithmetic.Tertiary –– High precedence operators")
                .add("**", Operators.Binary.Mathematics.Arithmetic.Tertiary.Exponentiation),

            Category("Mathematics.Arithmetic.Secondary –– Medium precedence operators")
                .add("*", Operators.Binary.Mathematics.Arithmetic.Secondary.Multiplication)
                .add("/", Operators.Binary.Mathematics.Arithmetic.Secondary.Division)
                .add("%", Operators.Binary.Mathematics.Arithmetic.Secondary.Modulo),

            Category("Mathematics.Arithmetic.Primary –– Low precedence operators")
                .add("+", Operators.Binary.Mathematics.Arithmetic.Primary.Addition)
                .add("-", Operators.Binary.Mathematics.Arithmetic.Primary.Subtraction),

            Category("Boolean.Bitwise –– Bitwise boolean operators"),

            Category("Boolean.Tests –– Predicate tests"),

            Category("Boolean.Comparisions –– Boolean comparision operators")
                .add("<", Operators.Binary.Boolean.Comparisions.LessThan)
                .add("<=", Operators.Binary.Boolean.Comparisions.LessThanOrEqualTo)
                .add(">", Operators.Binary.Boolean.Comparisions.GreaterThan)
                .add(">=", Operators.Binary.Boolean.Comparisions.GreaterThanOrEqualTo)
                .add("==", Operators.Binary.Boolean.Comparisions.EqualTo)
                .add("!=", Operators.Binary.Boolean.Comparisions.NotEqualTo),

            Category("Boolean.Operators –– Boolean logic operators"),

            Category("Lambda –– Lambda function operator", "reverse-collapse")
                .add("=>", Operators.Binary.Lambda),

            Category("Binding –– Binding operator", "reverse-collapse")
                .add("=", Operators.Binary.Binding),

            Category("Sequention –– Sequention operator", "reverse-collapse")
                .add(";", Operators.Binary.Sequention)
        ]

std_ops = module(OPERATORS)

info = package_info(std_ops, "std.ops@v2.1 –– the standard operators", [exp_category, exp_error, exp_category, exp_variable, exp_info, std_lib])

if __name__ == "__main__": info()