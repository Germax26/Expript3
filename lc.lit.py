from exp_package import *

std_lit = import_package(here("std"), "lit")
_std_lit_ = std_lit.LITERALS()

lc_lib = import_package(here("lc"), "lib")


class LITERALS:
    def __init__(self):
        self.literals = [
            _std_lit_.literals[0],
            (
                lambda root, _: root.value.isnumeric(),
                lambda root, _: (lc_lib.ChurchNumeral(_std_lit_.literals[1][1](root, _)[0]), None)
            ),
            _std_lit_.literals[2]
        ]