from exp_category import *
from exp_error import *
from exp_type import *
from exp_info import *

class Operators:
    class Unary:
        class Positive(NumOp.R):
            def function(right, _):
                return +right, None
        class Negative(NumOp.R):
            def function(right, _):
                return -right, None
        class Negation(BoolOp.R):
            def function(right, _):
                return not right, None
    class Binary:
        class Radix(IntOp.L * -BoolOp.L, L):
            def function(left, _, context):
                if context.right.value.isdigit():
                    return eval(f"{left}.{context.right.value}"), None # decimals
                return None, InterpreterError("Illegal postradix, expected digits.", *context.right.uberspan(), context.expr, "IllegalPostradixError")

        class Mathematics:
            class Arithmetic(NumOp):
                class Primary:
                    class Addition(StrOp + TupOp):
                        def function(left, right, _):
                            return left + right, None
                    class Subtraction:
                        def function(left, right, _):
                            return left - right, None
                class Secondary:
                    class Multiplication(ArrOp.L * IntOp.R):
                        def function(left, right, _):
                            return left * right, None
                    class Division:
                        def function(left, right, _):
                            if right == 0:
                                return None, InterpreterError("Cannot divide by 0.", _.self.span_left, _.self.right.left_span() + _.self.right.right_span() - _.self.span_left, _.expr, "DivisionByZeroError")
                            return left / right, None
                    class Modulo(ONI):
                        pass
                    class Quotient(ONI):
                        pass
                class Tertiary:
                    class Exponentiation:
                        def function(left, right, _):
                            return left ** right, None
                    class Root(ONI):
                        pass

        class Boolean(NumOp):
            class Comparisions:
                class LessThan:
                    def function(left, right, _):
                        return left < right, None
                class LessThanOrEqualTo:
                    def function(left, right, _):
                        return left <= right, None
                class GreaterThan:
                    def function(left, right, _):
                        return left > right, None
                class GreaterThanOrEqualTo:
                    def function(left, right, _):
                        return left >= right, None
                class EqualTo(ObjOp):
                    def function(left, right, _):
                        return left == right, None
                class NotEqualTo(ObjOp):
                    def function(left, right, _):
                        return left != right, None
            class Bitwise:
                class And(ONI):
                    pass
                class Or(ONI):
                    pass
            class Operators:
                class And(ONI):
                    pass
                class Or(ONI):
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

info = package_info(std_ops, "std.ops@v2.3 –– the standard operators", [exp_category, exp_error, exp_info])

if __name__ == "__main__": info()