from exp_info import *

class LITERALS:
    def __init__(self):
        self.literals = [
            (
                lambda root, vars_: root.value in vars_, 
                lambda root, vars_: vars_[root.value]()),
            (
                lambda root, _: root.value.isnumeric(), 
                lambda root, _: (0, None) if root.value.count("0") == len(root.value) else (eval(root.value.lstrip("0")), None)),
            (
                lambda root, _: root.value[0] + root.value[-1] == '""', 
                lambda root, _: (root.value[1:-1], None))
        ]

std_lit = module(LITERALS)

info = package_info(std_lit, "std.lit@v1 –– the standard literals", [exp_info])

if __name__ == "__main__": info()