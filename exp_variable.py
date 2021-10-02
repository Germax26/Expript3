from exp_info import *

class VARIABLE_LIST:
    def __init__(self, *initital_vars):
        self.vars = {}
        self.vals = {}
        self.memo = {}
        self.var_memo = {}

        for var in initital_vars:
            self.add_val(var)

    def add_var(self, var):
        self.vars[var.name] = var.func

    def add_val(self, val):
        self.vals[val.name] = val.func

    def get_var(self, index):
        if index in self.var_memo:
            return self.var_memo[index]
        if index in self.vars:
            self.var_memo[index] = self.vars[index]()
            return self.get_var(index)
        print()
        print()
        err = LookupError(f"Variable '{index}' does not exist in this VARIABLE_LIST")
        raise err

    def __getitem__(self, index):
        if index in self.memo: 
            return self.memo[index]
        if index in self.var_memo:
            return self.var_memo[index]
        if index in self.vals:
            self.memo[index] = self.vals[index]()
            return self[index]
        if index in self.vars:
            self.var_memo[index] = self.vars[index]()
            return self[index]
        err = LookupError(f"Variable/Value '{index}' does not exist in this VARIABLE_LIST")
        raise err
        
    def __contains__(self, name):
        return name in self.vars or name in self.vals

    def display(self, lazy=False):
        for variable in self.vars:
            if variable in self.var_memo:
                to_print = str(self.var_memo[variable])
            elif not lazy:
                to_print = str(self[variable])
            else:
                to_print = f"[ {self.vars[variable]} ]"
            print(f"Variable: {variable} => {to_print}")

        for value in self.vals:
            if value in self.memo:
                to_print = str(self.memo[value])
            elif not lazy:
                to_print = str(self[value])
            else:
                to_print = f"[ {self.vals[value]} ]"
            print(f"Value: {value} => {to_print}")
    
    def union(self, other):
        new_list = VARIABLE_LIST()
        new_list.vars = {**self.vars, **other.vars}
        new_list.vals = {**self.vals, **other.vals}
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