from exp_info import *

class Context:
    def __init__(self, interpreter, root, operands, variables, source, categories):
        self.int = interpreter
        self.self = root
        self.left = root.left
        self.right = root.right
        self.operands = operands
        self.type_left = type(operands[0])
        self.type_right = type(operands[1])
        self.variables = variables
        self.expr = source
        self.categories = categories

    def evaluate(self, source=None, root=None, categories=None, variables=None) -> tuple:
        """Evaluate a node in the given context, with options for overriding.

        Args:
            source (str, optional): Overridable source of evaluation. Defaults to None.
            root (Node, optional): Overridable root node of evaluation. Defaults to None.
            categories (list[Category], optional): Overridable categories of evaluation. Defaults to None.
            variables (VARIABLE_LIST, optional): Overridable variables of evaluation. Defaults to None.

        Returns:
            tuple: (result, None) or (None, err)
        """
        return self.int.interpret(source or self.expr, root or self.right, categories or self.categories, variables or self.variables)

    def copy(self, int=None, root=None, operands=None, variables=None, source=None, categories=None):
        new_context = Context(int or self.int, root or self.self, operands or self.operands, variables or self.variables, source or self.expr, categories or self.categories)
        if root is None and self.left is not self.self.left: new_context.left = self.left
        if root is None and self.right is not self.self.right: new_context.right = self.right
        return new_context

exp_context = module(__name__)

info = package_info(exp_context, "exp_context@v2 –– the built-in context package", [exp_info])

if __name__ == "__main__": info()
