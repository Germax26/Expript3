from exp_info import *

class LIBRARY:
    def __init__(self):
        self.values = {
            "true": True,
            "false": False
        }
        self.variables = {}

std_lib = module(LIBRARY)

info = package_info(std_lib, "std.lib@v2 –– the standard library", [exp_info])

if __name__ == "__main__": info()