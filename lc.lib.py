from exp_package import *
from exp_error import *
from exp_interface import *
from exp_info import *

interface_init()

ext_lib = import_package(here("ext"), "lib")

class InvalidChurchBooleanError(InterpreterError):
    def __init__(self, context):
        super().__init__("Invalid church boolean!", *context.right.uberspan(), context.expr, "InvalidChurchBooleanError")

class InvalidChurchNumeralError(InterpreterError):
    def __init__(self, context):
        super().__init__("Invalid church numeral!", *context.right.uberspan(), context.expr, "InvalidChurchNumeralError")

class InvalidChurchPairError(InterpreterError):
    def __init__(self, context):
        super().__init__("Invalid church pair!", *context.right.uberspan(), context.expr, "InvalidChurchPairError")


class ChurchBoolean: pass

class ChurchNumeral(ext_lib.Function):
    def __init__(self, value):
        self.value = value
        self.name = str(value)
        self.type_req = ext_lib.req_expfuncl

    def call(self, right, _):
        if self.value == 0:
            return Identity, None
        if self.value == 1:
            return right, None

        if isinstance(right, ChurchNumeral):
            return ChurchNumeral(right.value ** self.value), None

        def fn_of_a(a, context):
            f = a
            for i in range(self.value):
                f, err = right(f, context)
                if err: return None, err
            return f, None
        name = right._name_() if isinstance(right, ext_lib.Function) else right.__name__
        return ext_lib.exp_function(fn_of_a, name=f"apply_{self.name}_times_{name}"), None

    def __repr__(self):
        if self.name != str(self.value): return super().__repr__()
        return str(self.value)

Identity = ChurchNumeral(1)
Identity.name = "Identity"
Identity.type_req = ext_lib.req_objl

def Mockingbird(f, context): # \f.f f
    if callable(f):
        return callback_wrapper(f(f, context), "in mockingbird") # f f
    return None, InterpreterError("Can't call given input on itself.", *context.right.span, context.expr, "MockingbirdError")

Mockingbird = ext_lib.exp_function(Mockingbird, type_req=ext_lib.req_expfuncl)       

def Successor(n, _): # \n.\f.\a.f (n f a)
    if isinstance(n, ChurchNumeral):
        return ChurchNumeral(n.value + 1), None
    succ, err = get_entry("lc_lib").genesis.get_var("succ")
    if err: return None, err
    return succ.curry_call(args=[n], contexts=[_])
Successor = ext_lib.exp_function(Successor, type_req=ext_lib.req_expfuncl)

def Addition(n, _): # \n.\k.n succ k
    def add_n(k, context): # \k.n succ k
        if isinstance(n, ChurchNumeral) and isinstance(k, ChurchNumeral):
            return ChurchNumeral(n.value + k.value), None

        add, err = get_entry("lc_lib").genesis.get_var("add")
        if err: return None, err
        return add.curry_call(args=[n, k], contexts=[_, context])
    return ext_lib.exp_function(add_n, name=f"add_{n.name}"), None 
Addition = ext_lib.exp_function(Addition, type_req=ext_lib.req_expfuncl)

def Multiplication(n, context): # \n.\k.\f. n (k f)
    def fn_of_k(k, context2): # \k.\f. n (k f)
        if isinstance(n, ChurchNumeral) and isinstance(k, ChurchNumeral):
            return ChurchNumeral(n.value * k.value), None

        B, err = get_entry("lc_lib").genesis.get_var("B")
        if err: return None, err

        return B.curry_call(args=[n, k], contexts=[context, context2])
    return ext_lib.exp_function(fn_of_k, name=f"mult_by_{n.name}"), None
Multiplication = ext_lib.exp_function(Multiplication, type_req=ext_lib.req_expfuncl)


        
def ExpriptBoolean(p, context): # \p.p true false
    return p.curry_call(args=[True, False], contexts=[context]*2) # , InvalidChurchBooleanError(context))
ExpriptBoolean = ext_lib.exp_function(ExpriptBoolean, type_req=ext_lib.req_expfuncl)

def ExpriptNumeral(f, context): # \n.n (\x.x+1) 0
    if isinstance(f, ChurchNumeral):
        return f.value, 
    result, err = f.curry_call(args=[ext_lib.exp_function(lambda x, _: (x + 1, None), name="increment", type_req=ext_lib.req_intl), 0], contexts=[context, context])
    if isinstance(result, int):
        return result, err
    return None, InvalidChurchNumeralError(context)
ExpriptNumeral = ext_lib.exp_function(ExpriptNumeral, type_req=ext_lib.req_expfuncl)

def ExpriptTuple(v, context): 
    elements = []
    def absorb_(x, _):
        elements.append(x)
        return absorb, None
    absorb = ext_lib.exp_function(absorb_, name="absorb")
    result, err = v(absorb, context)
    if err: return None, err
    len_elements = len(elements)
    result, err = result(0, context)
    if err: return None, err
    if len(elements) == len_elements or elements[-1] != 0:
        return None, InvalidChurchPairError(context)
    return tuple(elements[:-1]), None

ExpriptTuple = ext_lib.exp_function(ExpriptTuple, type_req=ext_lib.req_expfuncl)
    
class LIBRARY(InterfaceEntry):
    def __new__(cls): return super().__new__(cls, "lc_lib")
    def __init__(self):
        super().__init__()
        self.values = {
            "I": Identity,
            "M": Mockingbird,

            "succ":  Successor,
            "add": Addition,
            "mult": Multiplication,

            "exp_bool": ExpriptBoolean,
            "exp_num": ExpriptNumeral,
            "exp_tup": ExpriptTuple
        }
        self.variables = {
            "I": "Identity = \\a.a\n;Identity",
            "K": "Kestrel = \\a. \\b.a\n;Kestrel",
            "Ki": "Kite = \\a. \\b.b\n;Kite",
            "C": "Cardinal = \\f. \\a. \\b.f b a\n;Cardinal",
            "B": "Bluebird = \\f. \\g. \\b.f (g b)\n;Bluebird",
            "Th": "Thrush = \\a. \\f.f a\n;Thrush",
            "V": "Vireo = \\a. \\b. \\f.f a b\n;Vireo",
            "B1": "Blackbird = B B B\n;Blackbird",
            "S": "Sterling = \\a. \\b. \\c.a c (b c)\n;Sterling",
            "Y": "\\f.(\\x.f(x x))(\\x.f(x x))",
            "T": "True = K\n;True",
            "F": "False = Ki\n;False",

            "not": "Not = \\p.p F T\n;Not",
            "and": "And = \\p. \\q.p q p\n;And",
            "or": "Or = \\p. \\q.p p q\n;Or",
            "beq": "BooleanEquality = \\p. \\q.p q (not q)\n;BooleanEquality",

            "succ": "\\n. \\f. \\a.f (n f a)",

            "add": "Addition = \\n. \\k.n succ k\n;Addition",

            # "mult": "Multiplication = B; Multiplication",

            # "pow": "Exponentiation = Th; Exponentiation",

            "is_zero": "IsZero = \\n. n (K F) T\n;IsZero",


            "pair": "Pair = \\a. \\b. \\f.f a b\n;Pair",

            "fst": "First = \\p.p K\n;First",
            "snd": "Second = \\p.p Ki\n;Second",

            "phi": "Phi = \\p.V(snd p)(B succ snd p)\n;Phi",
            "pred": "Predecessor = \\n.fst(n phi(V 0 0))\n;Predecessor",
            "sub": "Subtraction = \\n. \\k.k pred n\n;Subtraction",

            "leq": "LessThanOrEqualTo = \\n. \\k.is_zero(sub n k)\n;LessThanOrEqualTo",
            "eq": "Equality = \\n. \\k.and(leq n k)(leq k n)\n;Equality",
            "gt": "GreaterThan = B1 not leq\n;GreaterThan",

            "div_inner": "\\c. \\n. \\m. \\f. \\x.(\\d.is_zero d(0 f x)(f(c d m f x)))(sub n m)",
            "divide1": "Y div_inner",
            "div": "Division = \\n.divide1(succ n)\n;Division",


            "nil": "Nil = V T T\n;Nil",
            "is_nil": "IsNil = fst\n;IsNil",
            "cons": "Construct = \\h. \\t.V F(V h t)\n;Construct",
            "head": "Head = \\p.B fst snd p\n;Head",
            "tail": "Tail = \\p.B snd snd p\n;Tail"
        }

lc_lib = module(LIBRARY)

info = package_info(lc_lib, "lc.lib@v1 –– the lambda calculus library", [exp_error, exp_package, exp_info, ext_lib])

# if __name__ == "__main__": info()