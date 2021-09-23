from exp_category import *
from exp_error import *
from exp_variable import *
from exp_info import *

import string
from types import FunctionType

class Binding:
    def __init__(self, context):
        self.name = context.left.value
        self.context = context

        def get_val():
            result, err = self.context.evaluate()
            if err: return None, err
            if type(result) == Function:
                return result.copy(self.name), None
            return result, None

        self.var = VARIABLE(self.name, func=get_val)
    
    def __repr__(self): return ""

class Function:
    def __init__(self, context, name=None):
        self.param = context.left.value
        self.context = context
        self.name = name

    def __call__(self, _, context):
        right = {}
        def get_param():
            # nonlocal right
            if right: return right["right"]
            right["right"] = context.evaluate()
            result = get_param()
            return result

        return self.context.evaluate(variables=self.context.variables.union(VARIABLE_LIST(VARIABLE(self.param, func=get_param))))
        
    def __repr__(self):
        if self.name:
            return f"<fn {self.name}>"
        return f"<fn of {self.param}>"

    def copy(self, new_name=None):
        return Function(self.context, new_name)

class Operators:
    class Unary: # [$]
        class Positive: # [x]
            valid = [int, float] 
            def function(right, _):
                return +right, None
        class Negative: # [x]
            valid = [int, float]
            def function(right, _):
                return -right, None
        class Negation: # [x]
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
    class Binary: # [$]
        class Cons:
            valid = [[object, tuple]]
            def function(left, right, context):
                return (left,) + right, None

        class Special: # [-]
            class Radix: # [x]
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
                    
            class Application: # [-]
                tags = ["right"]
                valid = [[Function], [FunctionType]]
                def function(left, _, context):
                    if context.type_left == Function:
                        return left(None, context)

                    right, err = context.evaluate()
                    if err: return None, err

                    return left(right, context)


        class Mathematics: # [-]
            class Arithmetic: # [-]
                class Primary: # [x]
                    class Addition: # [x]
                        valid = [[int, int], [float, float], [int, float], [float, int], [str, str], [tuple, tuple]]
                        def function(left, right, _):
                            return left + right, None
                    class Subtraction: # [x]
                        valid = [[int, int], [float, float], [int, float], [float, int]]
                        def function(left, right, _):
                            return left - right, None
                class Secondary: # [-]
                    class Multiplication: # [x]
                        valid = [[int, int], [float, float], [int, float], [float, int], [str, int], [tuple, int]]
                        def function(left, right, _):
                            return left * right, None
                    class Division: # [x]
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
                    class Exponentiation: # [x]
                        valid = [[int, int], [float, float], [int, float], [float, int]]
                        def function(left, right, _):
                            return left ** right, None
            class Trigenometry: # [.]
                pass

        class Boolean: # [-]
            class Comparisions: # [x]
                class LessThan: # [x]
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left < right, None
                class LessThanOrEqualTo: # [x]
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left <= right, None
                class GreaterThan: # [x]
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left > right, None
                class GreaterThanOrEqualTo: # [x]
                    valid = [[int, int], [float, float], [int, float], [float, int]]
                    def function(left, right, _):
                        return left >= right, None
                class EqualTo: # [x]
                    valid = [[object, object]]
                    def function(left, right, _):
                        return left == right, None
                class NotEqualTo: # [x]
                    valid = [[object, object]]
                    def function(left, right, _):
                        return left != right, None
            class Bitwise: # [.]
                class And: # [ ]
                    pass
                class Or: # [ ]
                    pass
            class Operators: # [.]
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
                if context.left.is_op:
                    return None, InterpreterError("An expression cannot be the parameter of a function.", *context.left.uberspan(), context.expr, "ExpressionParameterError")
                return Function(context), None

        class Binding: # [x]
            tags = ["left", "right"]
            valid = []
            def function(_, __, context):
                if context.left.is_op:
                    return None, InterpreterError("Cannot bind value to expression.", *context.left.uberspan(), context.expr, "CannotAssignToExpressionError")
                return Binding(context), None

        class Sequention: # [x]
            tags = ["right"]
            valid = [[object]]
            def function(left, _, context):
                if context.type_left == Binding:
                    return context.evaluate(variables=context.variables.union(VARIABLE_LIST(left.var)))
                return context.evaluate()

class OPERATORS:
    def __init__(self):
        self.unary = [
            Category("unary")
                .add('+', Operators.Unary.Positive)
                .add("-", Operators.Unary.Negative)
                .add("!", Operators.Unary.Negation)
                .add("len", Operators.Unary.Length)
                .add("rev", Operators.Unary.Reverse)
        ][0]
        self.binary = [
            Category("Construct", "reverse-collapse")
                .add(":", Operators.Binary.Cons), 

            Category("Special")
                .add(".", Operators.Binary.Special.Radix)
                .add("<-", Operators.Binary.Special.Application),

            Category("Mathematics.Arithmetic.Tertiary")
                .add("**", Operators.Binary.Mathematics.Arithmetic.Tertiary.Exponentiation),

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

            Category("Boolean.Operators"),

            Category("Lambda", "reverse-collapse")
                .add("=>", Operators.Binary.Lambda),

            Category("Binding")
                .add("=", Operators.Binary.Binding),

            Category("Sequention", "reverse-collapse")
                .add(";", Operators.Binary.Sequention)
        ]
        self.alpha = []
        for operator in self.unary.operators:
            for char in operator:
                if char in string.ascii_letters+string.digits + "_":
                    self.alpha.append(operator)
                    break

std_ops = module(OPERATORS)

info = package_info(std_ops, "std.ops@v2 –– the standard operators", [exp_category, exp_error, exp_variable, exp_info])

if __name__ == "__main__": info()