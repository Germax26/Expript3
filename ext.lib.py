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
    def __init__(self, context, name=None, param=None, override=None, type_req=None):
        if context:
            self.param = context.left.value
        else:
            self.param = param
        self.context = context
        self.name = name
        if name and len(name) > 210:
            self.name = name[:200] + "..."
        self.override = override
        self.type_req = type_req

    def __call__(self, right, context):
        try:
            arg = right
            if self.type_req:
                param, err = (arg, None) if arg is not None else context.evaluate()
                if err: return None, err
                if not self.type_req.check([param, None]):
                    return None, InterpreterError(f"Unpermitted type '{stringify(type(param))}' for {str(self)}. Expected otherwise.", *context.right.uberspan(), context.expr, "UnpermittedTypeError")
            return self.call(arg, context)
        except RecursionError:
            return None, InterpreterError("Too much recursion.", *context.self.uberspan(), context.expr, "ExcessiveRecursionError")

    def call(self, right, context):
        arg = None

        def get_param():
            nonlocal arg
            if right is not None: return right, None
            if arg is not None: return arg, None
            arg, err = context.evaluate()
            if err: return None, err
            return arg, None

        if self.override:
            param, err = get_param()
            if err: return None, err
            return self.override(param, context)

        return self.context.evaluate(variables=self.context.variables.union(VARIABLE_LIST(VARIABLE(self.param, func=get_param))))     

    def __repr__(self):
        if self.name:
            to_print = self.name
            if len(self.name) > 60:
                to_print = self.name[:50] + "..."
            return f"<fn {to_print}>"
        if self.param:
            return f"<fn of {self.param}>"
        if self.override:
            return f"<fn {self.override.__name__}>"
        return f"<fn {self}>"

    def _name_(self):
        if self.name is None:
            return f"fn_of_{self.param}"
        return self.name

    def curry_call(self, args=[], contexts=[]):
        assert len(contexts) >= len(args), "need more contexts"
        f = self

        for arg, context in zip(args, contexts):
            if req_expfuncl.check([f, None]):
                f, err = f(arg, context)
                if err: return None, err
            else:
                return None, InterpreterError(f"Unperfmitted type '{stringify(type(arg))}' for {str(f)}. Expected otherwise.", *context.right.uberspan(), context.expr, "UnpermittedTypeError")
        return f, None
        
    def copy(self, new_name=None):
        return Function(self.context, new_name, self.override, self.type_req)

req_expfuncl, req_expfuncr, req_expfunc, ExpFuncOp = generate_req([Function, FunctionType])

def exp_function(call, name=None, param=None, type_req=None): return Function(None, name or call.__name__ if param is None else None, param, call, type_req)

def Length(x, _):
    return len(x), None

def Reverse(x, _):
    return x[::-1], None

def Evaluate(source, context):
    try:
        result, err = evaluate(source, context.int.lexer, context.int.parser, context.int, context.categories, context.variables)
        if err: return None, err.add_callback("in string")
        return result, None
    except RecursionError:
        return None, InterpreterError("String evaluation is too recursive!", *context.self.uberspan(), context.expr, "ExcessiveRecursionInStringEvaluationError").add_callback("in string")

class LIBRARY():
    def __init__(self):
        self.values = {**_std_lib_.values,
            "()": tuple(),
            "len": exp_function(Length, type_req=req_arrl),
            "rev": exp_function(Reverse, type_req=req_arrl),
            "eval": exp_function(Evaluate, type_req=req_strl)
        }
        self.variables = {}

ext_lib = module(LIBRARY)

info = package_info(ext_lib, "ext.lib@v1.1 –– the extended library", [exp_package, exp_error, exp_variable, exp_type, exp_info, std_lib])

if __name__ == "__main__": info()