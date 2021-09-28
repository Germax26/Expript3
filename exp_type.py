from exp_error import *
from exp_info import *
import sys

NoneType = type(None)

And = ["and", "&", "*"]
Or = ["or", "|", "+"]
Not = ["not", "!", "-"]

def stringify(klass, force_type=False):
    x = type(klass)
    if not force_type and x == type:
        x = klass
    return str(x)[8:-2].split('.')[-1]

class TypeRequirement:
    def __init__(self, req_type, value, left=False, right=False, extra={}):
        self.value = value
        self.req_type = req_type
        self.left = left
        self.right = right
        self.extra = extra

    def __repr__(self):
        return f"[{self.req_type} {self.value} {int(self.left) if type(self.left) == bool else self.left} {int(self.right) if type(self.right) == bool else self.right}]"

    def string(self):
        if self.req_type == "id":
            return ":" * self.right + self.value + ":" * self.left
        elif self.req_type in Or:
            return self.left.string() + " + " + self.right.string()
        elif self.req_type in And:
            left = self.left.string()
            right = self.right.string()
            return  (f"({left})" if self.left.req_type in And else left) + " * " + (f"({right})" if self.right.req_type in And else right)
        elif self.req_type in Not:
            right = self.right.string()
            return "!" + f"({right})" if self.right.req_type != "id" and self.right.req_type not in Not else right

    def __add__(self, other): return TypeRequirement("+", "", self, other, {**self.extra, **other.extra})
    def __mul__(self, other): return TypeRequirement("*", "", self, other, {**self.extra, **other.extra})
    def __neg__(self): return TypeRequirement("!", "", None, self)

    def check(self, types):
        if self.req_type == "id":
            try:
                allowed_types = {
                    "int": int,
                    "float": float,
                    "num": [float, int],
                    "obj": object,
                    "tup": tuple,
                    "str": str,
                    "bool": bool,
                    "func": FunctionType,
                    "none": NoneType,
                    "arr": [str, list, tuple],
                    **self.extra
                }[self.value]
            except KeyError:
                raise TypeRequirementError(self.value)

            def check_type(a):
                for _type in allowed_types if type(allowed_types) == list else [allowed_types]:
                    if isinstance(a, _type):
                        return True
                return False

            for_left = check_type(types[0])
            for_right = check_type(types[1])

            if self.left or self.right:
                return (not self.left or for_left) and (not self.right or for_right)
            return for_left or for_right

        if self.req_type in And:
            return self.left.check(types) and self.right.check(types)
        elif self.req_type in Or:
            return self.left.check(types) or self.right.check(types)
        elif self.req_type in Not:
            return not self.right.check(types)
        else:
            print("no", self.value, self.req_type)

def req(type_req, extra={}):
    err = TypeRequirementError(type_req)
    key = "(:)"
    is_at_end = False
    current_ix = -1
    current_char = None

    tokens = []

    def advance():
        nonlocal is_at_end, current_ix, current_char
        current_ix += 1
        is_at_end = current_ix >= len(type_req)
        current_char = type_req[current_ix] if not is_at_end else None

    advance()
    
    def next():
        return tokens.pop(0)

    def check(tt, val=None):
        return bool(tokens) and (tokens[0][0] == tt and (not val or tokens[0][1] in val))

    def take(tt):
        if check(tt): return next()
        raise err

    while not is_at_end:
        if current_char == " ": 
            advance()
        elif current_char in key: 
            tokens.append(({
                "(": "lp",
                ")": "rp",
                ":": "cl"
                }[current_char], current_char))
            advance()
        elif current_char in And + Or + Not:
            tokens.append(("id", current_char))
            advance()
        else:
            current = ""
            while not is_at_end and current_char not in key + " ":
                current += current_char
                advance()
            tokens.append(("id", current))
            
    def parse_req(tokens):
        if check("lp"):
            next()
            sub_expr = parse_expr(tokens)
            take("rp")
            return sub_expr

        if has_right:= check("cl"): next()
        id = take("id")
        if has_left:= check("cl"): next()

        return TypeRequirement(*id, has_left, has_right, extra) 

    def parse_not(tokens):
        if check("id", Not):
            op = next()  
            return TypeRequirement(op[1], "", None, parse_not(tokens))
        return parse_req(tokens)

    def parse(lower, *names):
        if len(names) > 1:
            return parse(parse(lower, *names[:-1]), names[-1])
        names = names[0]
        def do_parse(tokens):
            left = lower(tokens)
            while tokens and check("id", names):
                op = next()
                right = lower(tokens)
                left = TypeRequirement(op[1], "", left, right)
            
            return left
        return do_parse
        
    parse_expr = parse(parse_not, And, Or)

    result = parse_expr(tokens)
    if tokens: 
        print("pariahs!", tokens)
        sys.exit()
        raise err
    return result

def sides(type_req): return TypeRequirement("id", type_req, 1, 0), TypeRequirement("id", type_req, 0, 1)

req_numl, req_numr = sides("num")
req_num = req_numl * req_numr

req_strl, req_strr = sides("str")
req_str = req_strl * req_strr

req_tupl, req_tupr = sides("tup")
req_str = req_tupl * req_tupr

req_arrl, req_arrr = sides("arr")
req_arr = req_arrl * req_arrr

req_booll, req_boolr = sides("bool")
req_bool = req_booll * req_boolr

req_nonel, req_noner = sides("none")
req_none = req_nonel * req_noner

req_objl, req_objr = sides("obj")
req_obj = req_objl * req_objr

class L: tags = {"right"}
class R: tags = {"left"}
class N: tags = {"left", "right"}

def init_sub(lr):
    def init_cls(cls):
        should_add = None
        for a in cls.__dict__.keys():
            if isinstance(cls.__dict__[a], type):
                init_cls(cls.__dict__[a])
            if a == "function":
                should_add = should_add is None
            if a == "valid":
                should_add = False
        if should_add:
            setattr(cls, "valid", lr)
        elif should_add is not None:
            cls.valid = lr + cls.valid
    return init_cls

class MetaReq(type):
    def __add__(self, other): return MetaReq(f"({self.__name__} + {other.__name__})", (), {"valid": (lr := self.valid + other.valid), "__init_subclass__": init_sub(lr)})
    def __mul__(self, other): return MetaReq(f"({self.__name__} * {other.__name__})", (), {"valid": (lr := self.valid * other.valid), "__init_subclass__": init_sub(lr)})
    def __neg__(self): return MetaReq(f"-{self.__name__}", (), {"valid": (nr:=-self.valid), "__init_subclass__": init_sub(nr)})

def M(type_req, *_):
    return MetaReq(type_req.string(), tuple(_), {"valid": type_req, "__init_subclass__": init_sub(type_req)})

def Mreq(*_): return M(req(*_))

def Req(_req, _l=None, _r=None, bases=()):
    name = _req.capitalize() + "Op"
    l = _l or req(_req + ":")
    r = _r or req(":" + _req)
    lr = l * r
    return MetaReq(name, bases, {
        "L": MetaReq(name + ".L", (L,), {"valid": l}),
        "R": MetaReq(name + ".R", (R,), {"valid": r}),
        "valid": lr,
        "__init_subclass__": init_sub(lr)
    })

NumOp = Req("num", req_numl, req_numr)
StrOp = Req("str", req_strl, req_strr)
TupOp = Req("tup", req_tupl, req_tupr)
ArrOp = Req("arr", req_arrl, req_arrr)
BoolOp = Req("bool", req_booll, req_boolr)
NoneOp = Req("none", req_nonel, req_noner, (N,))
ObjOp = Req("obj", req_objl, req_objr)

exp_type = module(TypeRequirement)

info = package_info(exp_type, "exp_type@v2 –– the type package", [exp_info])

if __name__ == "__main__": info()