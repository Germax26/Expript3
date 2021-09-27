from exp_info import *

class REPRESENTER:
    def __init__(self):
        pass

    def represent(self, result):
        if type(result) == str:
            return f"'{result}'"
        elif type(result) == FunctionType:
            return f"<fn {str(result).split(' ')[1]}>"
        elif type(result) == tuple or type(result) == list:
            if len(result) == 0:
                return str(result)
            else:
                repr = ""
                for i, j in enumerate(result):
                    repr += ", " * (i != 0) + self.represent(j)
                return f"({repr})"
        else: return str(result)

std_rpr = module(REPRESENTER)

info = package_info(std_rpr, "std.rpr@v1 –– the standard representer", [exp_info])

if __name__ == "__main__": info()