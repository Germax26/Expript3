from exp_package import *
from exp_error import *
from exp_variable import *
from exp_type import *
from exp_info import *
from expript3 import *

std_lib = import_package(here("std"), "lib")
_std_lib_ = std_lib.LIBRARY()

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
    def __init__(self, context, name=None, override=None, types=[]):
        if context:
            self.param = context.left.value
        self.context = context
        self.name = name
        self.override = override
        self.types = types

    def __call__(self, _, context):
        right = {}

        def get_param():
            # nonlocal right
            if right: return right["_"]
            right["_"] = context.evaluate()
            return get_param()

        if self.types:
            argument, err = get_param()
            if err: return None, err
            argument_type = type(argument)
            for _type in self.types:
                if issubclass(argument_type, _type):
                    break
            else:
                return None, InterpreterError(f"Unpermitted type '{stringify(argument_type)}' for {str(self)}. Expected otherwise.", *context.self.uberspan(), context.expr, "UnpermittedTypeError")

        try:
            if self.override:
                if right: param = get_param()
                return self.override(self, param, context)

            return self.context.evaluate(variables=self.context.variables.union(VARIABLE_LIST(VARIABLE(self.param, func=get_param))))
        except RecursionError:
            return None, InterpreterError("Too much recursion.", *context.self.uberspan(), context.expr, "ExcessiveRecursionError")
            
    def __repr__(self):
        if self.name:
            return f"<fn {self.name}>"
        return f"<fn of {self.param}>"

    def copy(self, new_name=None):
        return Function(self.context, new_name, self.override, self.types)


def exp_function(name, call, types=[]): return Function(None, name, call, types)

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

class LIBRARY():
    def __init__(self):
        self.values = {**_std_lib_.values,
            "()": tuple(),
            "len": exp_function("Length", Length, [str, tuple, list]),
            "rev": exp_function("Reverse", Reverse, [str, tuple, list]),
            "eval": exp_function("Evaluate", Evaluate, [str])
        }
        self.variables = {}

ext_lib = module(LIBRARY)

info = package_info(ext_lib, "ext.lib@v1 –– the extended library", [exp_package, exp_error, exp_variable, exp_type, exp_info, std_lib])

if __name__ == "__main__": info()