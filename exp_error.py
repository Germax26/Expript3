from exp_info import *

class Error(EnvironmentError):
    def __init__(self, msg, span_left, span_right, expr, name):
        self.msg = msg
        self.span_left, self.span_right = span_left, span_right
        self.expr = expr
        self.name = name
        self.error_scope = "idk_scope"
        self.callbacks = []
        super().__init__(msg)
    
    def display(self):
        line = 0
        mod = 0
        total = 0
        
        lines = self.expr.split("\n")
        for i, j in enumerate(lines):
            if self.span_left < total:
                line = i
                break
            mod = total
            total += len(j) + 1
            self.expr = j
        else:
            line = len(lines)
            self.expr=lines[-1]
        
        self.span_left -= mod

        print(f"The {self.error_scope} encountered an unhandled {self.name} on line {line}.")
        for callback in self.callbacks:
            print("  " + callback[0])
            if callback[2] > 1:
                print(f"  [previous line repeated {callback[2]-1} more times]")
        print(self.msg)

        print(self.expr)

        print(" " * self.span_left + "^" * self.span_right)

        if self.span_right > len(self.expr) - self.span_left:
            print("This error spans multiple lines")
    
    def in_scope(self, scope):
        self.error_scope = scope
        return self

    def add_callback(self, callback, _=None):
        if self.callbacks and self.callbacks[-1][0] == callback:
            self.callbacks[-1][2] += 1
        else:  
            self.callbacks.append([callback, _, 1])
        return self

class LexerError(Error):
    def __init__(self, msg, span_left, span_right, expr, name):
        super().__init__(msg, span_left, span_right, expr, name)
        self.error_scope = "lexer"

class ParserError(Error):
    def __init__(self, msg, span_left, span_right, expr, name):
        super().__init__(msg, span_left, span_right, expr, name)
        self.error_scope = "parser"

class InterpreterError(Error):
    def __init__(self, msg, span_left, span_right, expr, name):
        super().__init__(msg, span_left, span_right, expr, name)
        self.error_scope = "interpreter"

class OperatorError(Error):
    def __init__(self, msg, span_left, span_right, expr, name):
        super().__init__(msg, span_left, span_right, expr, name)
        self.error_scope = "operator"

class TypeRequirementError(Error):
    def __init__(self, type_req):
        super().__init__(f"Invalid type requirement: '{type_req}'", 0, 0, type_req, "InvalidTypeRequirementError")
        self.error_scope = "type checker"

def not_implemented(msg, span_left, span_right, expr, error_scope):
    return None, Error(msg, span_left, span_right, expr, "UnimplementedFeatureError").in_scope(error_scope)

class ONI:
    def function(_, __, context):
        return None, OperatorError(f"The '{context.self.value}' operator is not implemented yet.", *context.self.span, context.expr, "OperatorNotImplementedError")

exp_error = module(__name__)

info = exp_info.package_info(exp_error, "exp_error@v1.1 –– the built-in error package", [exp_info])

if __name__ == "__main__": info()
