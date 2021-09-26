from exp_error import *
from exp_info import *
from exp_package import *
from expript3 import *

# std_ops = import_packages({"ops": path("std")})["ops"]

# import expript_ops as std_ops

def exp_function(operators, name, call, types=[]): return operators.Function(None, name, call, types)

def monad(f):
    def inner(self, _, context):
        argument, err = _ if _ else context.evaluate()
        if err: return None, err
        return f(argument, context)
    return inner

simple = lambda f: monad(lambda x, _: (f(x), None))

def Eval(source, context):
    try:
        result, err = evaluate(source, context.int.lexer, context.int.parser, context.int, context.categories, context.variables)
        if err: return None, err.add_callback("in string")
        return result, None
    except RecursionError:
        return None, InterpreterError("String evaluation is too recursive!", *context.self.uberspan(), context.expr, "ExcessiveRecursionInStringEvaluationError").add_callback("in string")

Length = simple(len)
Reverse = simple(lambda x: x[::-1])
Evaluate = monad(Eval)

class LIBRARY:
    def __init__(self, operators):
        self.values = {
            "true": True,
            "false": False,
            "()": tuple(),
            "len": exp_function(operators, "Length", Length, [str, tuple, list]),
            "rev": exp_function(operators, "Reverse", Reverse, [str, tuple, list]),
            "eval": exp_function(operators, "Evaluate", Evaluate, [str])
        }
        self.variables = {}

std_lib = module(LIBRARY)

info = package_info(std_lib, "std.lib@v1 –– the built-in library package", [exp_error, exp_info, exp_package])

if __name__ == "__main__": info()
