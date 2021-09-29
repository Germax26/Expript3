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
    def __init__(self, req_type, value, left=False, right=False):
        self.req_type = req_type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"[{self.req_type} {self.value} {int(self.left) if type(self.left) == bool else self.left} {int(self.right) if type(self.right) == bool else self.right}]"

    def string(self, depth=0):
        if self.req_type == "type":
            return "(" + ":" * self.right + ", ".join([stringify(type_) for type_ in self.value]) + ":" * self.left + ")"
        elif self.req_type in Or:
            return self.left.string() + " + " + self.right.string()
        elif self.req_type in And:
            left = self.left.string()
            right = self.right.string()
            return  (f"({left})" if self.left.req_type in And else left) + " * " + (f"({right})" if self.right.req_type in And else right)
        elif self.req_type in Not:
            right = self.right.string()
            return "!" + f"({right})" if self.right.req_type != "type" and self.right.req_type not in Not else right

    def __add__(self, other): return TypeRequirement("|", "", self, other)
    def __mul__(self, other): return TypeRequirement("&", "", self, other)
    def __neg__(self): return TypeRequirement("!", "", None, self)

    def check(self, operands):
        if self.req_type == "type":
            def check_type(operand):
                for potential_type in self.value:
                    if isinstance(operand, potential_type):
                        return True
                return False

            left = check_type(operands[0])
            right = check_type(operands[1])

            if self.left or self.right:
                return (not self.left or left) and (not self.right or right)
            return left or right

        if self.left: left = self.left.check(operands)
        if self.right: right = self.right.check(operands)

        if self.req_type in And: return left and right
        if self.req_type in Or: return left or right
        if self.req_type in Not: return not right

        raise TypeRequirementError(f"Invalid type requirement '{self.value}'.")

def req(types, sides=0):
    return TypeRequirement("type", types if isinstance(types, list) else [types], sides//2, sides%2)

class L: tags = {"right"}
class R: tags = {"left"}
class N: tags = {"left", "right"}

def init_sub(lr):
    def init_cls(cls):
        should_add = None
        for a in cls.__dict__.keys():
            if isinstance(cls.__dict__[a], type):
                init_cls(cls.__dict__[a])
            elif a == "function":
                should_add = should_add is None
            elif a == "valid":
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

def generate(types, bases=()):
    types = types if isinstance(types, list) else [types]
    l = req(types, 2)
    r = req(types, 1)
    lr = l * r
    name = "(" * (len(types) != 1) + ", ".join([stringify(type_) for type_ in types]) + ")" * (len(types) != 1)
    return l, r, lr, MetaReq(name, bases, {
        "L": MetaReq(name + ".L", (L,), {"valid": l, "__init_subclass__": init_sub(l)}),
        "R": MetaReq(name + ".R", (R,), {"valid": r, "__init_subclass__": init_sub(r)}),
        "valid": lr, "__init_subclass__": init_sub(lr)
    })

req_numl, req_numr, req_num, NumOp = generate([int, float])
req_intl, req_intr, req_int, IntOp = generate(int)
req_strl, req_strr, req_str, StrOp = generate(str)
req_tupl, req_tupr, req_tup, TupOp = generate(tuple)
req_arrl, req_arrr, req_arr, ArrOp = generate([str, list, tuple])
req_booll, req_boolr, req_bool, BoolOp = generate(bool)
req_nonel, req_noner, req_none, NoneOp = generate(type(None), (N,))
req_funcl, req_funcr, req_func, FuncOp = generate(FunctionType)
req_objl, req_objr, req_obj, ObjOp = generate(object)

exp_type = module(TypeRequirement)

info = package_info(exp_type, "exp_type@v2 –– the type package", [exp_info])

if __name__ == "__main__": info()