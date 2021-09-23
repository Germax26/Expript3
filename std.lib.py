from exp_error import *
from exp_info import *
 
class LIBRARY:
    def __init__(self):
        self.values = {
            "true": True,
            "false": False,
            "()": tuple()
        }
        self.variables = {}

std_lib = module(LIBRARY)

info = package_info(std_lib, "std.lib@v1 –– the built-in library package", [exp_error, exp_info])

if __name__ == "__main__": info()
