from exp_info import *

class Context:
    def __init__(self, interpreter, root, operands, variables, source, categories):
        self.int = interpreter
        self.self = root
        self.left = root.left
        self.right = root.right
        self.type_left = type(operands[0])
        self.type_right = type(operands[1])
        self.variables = variables
        self.expr = source
        self.categories = categories

exp_context = module(__name__)

info = package_info(exp_context, "exp_context@v2 –– the built-in context package", [exp_info])

if __name__ == "__main__": info()