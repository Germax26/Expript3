from exp_info import *

class VARIABLE_LIST:
    def __init__(self, *initital_vars):
        self.vars = {}

        for var in initital_vars:
            self.add(var)

    def add(self, var):
        self.vars[var.name] = var.func

    def __getitem__(self, index):
        return self.vars[index]

    def __contains__(self, name):
        return name in self.vars

    def display(self):
        for variable in self.vars:
            print(f"Variable: {variable} => {self[variable]()}")
    
    def union(self, other):
        new_list = VARIABLE_LIST()
        new_list.vars = {**self.vars, **other.vars}
        return new_list

class VARIABLE:
    def __init__(self, name, value=None, func=None):
        self.name = name
        self.value = value

        def get_val():
            return self.value, None
        
        self.func = func or get_val

exp_variable = module(__name__)

info = package_info(exp_variable, "exp_variable@v1 –– the built-in variable package", [exp_info])

if __name__ == "__main__": info()