from exp_category import *
from exp_package import *
from exp_error import *
from exp_type import *
from exp_info import *

ext_lib = import_package(here("ext"), "lib")
ext_ops = import_package(here("ext"), "ops")
_ext_ops_ = ext_ops.OPERATORS()

Application = ext_ops.Operators.Binary.Application

class Binding(NoneOp):
    def function(_, context):
        return None, InterpreterError("Cannot have have a lambda operator by itself without body.", *context.self.uberspan(), context.expr, "InvalidAbstractionError")

class Abstraction(NoneOp):
    def function(_, __, context):
        if context.left.is_op and context.left.value == "\\":
            context.left = context.left.right
            return ext_lib.Function(context), None

        return None, InterpreterError("Missing lambda ")

class OPERATORS:
    def __init__(self):
        self.categories = [
            Category("paramater-binding", "unary").add("\\", Binding),
            Category("application", "implied").add("", Application),
            Category("abstraction", "reverse-collapse").add(".", Abstraction),
            _ext_ops_.get("binding"),
            _ext_ops_.get("sequention")

        ]

lc_ops = module(OPERATORS)

info = package_info(lc_ops, "lc.ops@v1 –– the lambda calculus operators", [exp_category, exp_package, exp_error, exp_info, ext_lib, ext_ops])

if __name__ == "__main__": info()