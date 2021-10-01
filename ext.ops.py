from exp_package import *
from exp_category import *
from exp_error import *
from exp_variable import *
from exp_type import *

from exp_info import *

ext_lib = import_package(here("ext"), "lib")
std_ops = import_package(here("std"), "ops")

_std_ops_ = std_ops.OPERATORS()

class Operators:
    class Binary:
        class Radix(IntOp.L * -BoolOp.L + ArrOp.L, L):
            def function(left, _, context):
                if isinstance(left, int):
                    return std_ops.Operators.Binary.Radix.function(left, _, context)

                right, err = context.evaluate()
                if err: return None, err

                type_right = type(right)

                if (type_right) != int: 
                    return None, InterpreterError("Illegal index, expected int.", *context.right.uberspan(), context.expr, "IllegalIndexError")
                
                len_left = len(left)
                if right + 1 and right < len_left:
                    return left[right], None

                return None, InterpreterError(f"Index out of range. List was {len_left} element{'s' if len_left != 1 else ''} long.", *context.self.uberspan(), context.expr, "IndexOutOfRangeError")

        class Application(Mreq(ext_lib.Function) + FuncOp.L, L):
            def function(left, _, context):
                if isinstance(left, ext_lib.Function):
                    argument = None
                    if left.type_req:
                        argument, err = context.evaluate()
                        if err: return None, err
                        if not left.type_req.check([argument, None]):
                            return None, InterpreterError(f"Unpermitted type '{stringify(type(argument))}' for {str(left)}. Expected otherwise.", *context.right.uberspan(), context.expr, "UnpermittedTypeError")
                        
                    return left(argument, context)

                right, err = context.evaluate()
                if err: return None, err

                try:
                    return left(right, context)
                except RecursionError:
                    return None, InterpreterError("Too much recursion.", *context.self.span, context.expr, "RecursionError")
        
        class Cons(ObjOp.L * TupOp.R):
            def function(left, right, context):
                return (left,) + right, None

        class Lambda(NoneOp):
            def function(_, __, context):
                if context.left.is_op:
                    return None, InterpreterError("An expression cannot be the parameter of a function.", *context.left.uberspan(), context.expr, "ExpressionParameterError")
                return ext_lib.Function(context), None

        class Binding(NoneOp):
            def function(_, __, context):
                if context.left.is_op:
                    return None, InterpreterError("Cannot bind value to expression.", *context.left.uberspan(), context.expr, "CannotAssignToExpressionError")
                return ext_lib.Binding(context), None

        class Sequention(ObjOp.L):
            def function(left, _, context):
                if context.type_left == ext_lib.Binding:
                    return context.evaluate(variables=context.variables.union(VARIABLE_LIST(left.var)))
                return context.evaluate()

class OPERATORS(CategoryList):
    def __init__(self):
        self.categories = [
            Category("radix")
                .add(".", Operators.Binary.Radix),

            _std_ops_.get("unary"),

            Category("application")
                .add("<-", Operators.Binary.Application),

            Category("construct", "reverse-collapse")
                .add(":", Operators.Binary.Cons),

            _std_ops_.get("mathematics.arithmetic.tertiary"),
            _std_ops_.get("mathematics.arithmetic.secondary"),
            _std_ops_.get("mathematics.arithmetic.primary"),

            Category("boolean.tests"),

            _std_ops_.get("boolean.comparisions"),
            _std_ops_.get("boolean.operators"),

            Category("lambda", "reverse-collapse")
                .add("=>", Operators.Binary.Lambda),

            Category("binding", "reverse-collapse")
                .add("=", Operators.Binary.Binding),

            Category("sequention", "reverse-collapse")
                .add(";", Operators.Binary.Sequention)
        ]

ext_ops = module(OPERATORS)

info = package_info(ext_ops, "ext.ops@v1.1 –– the extended operators", [exp_package, exp_category, exp_error, exp_variable, exp_info, std_ops])

if __name__ == "__main__": info()