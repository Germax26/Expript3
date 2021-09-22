import sys, os
from types import ModuleType, FunctionType
from typing import List

exp_info = __import__(__name__)

def module(klass: type):
    """
    Returns the module of a klass.
    """
    try:
        return sys.modules[klass.__module__]
    except AttributeError:
        return sys.modules[klass]
    except KeyError:
        return klass.__module__

def unknown(depth, dep: int, fil: str):
    """
    Used to print undeterminable dependencies.
    """
    cwd = os.getcwd().split(os.path.sep)
    flp = fil.split(os.path.sep)

    if flp[0] != '': cwd = [] # for relative file paths in flp

    while cwd and flp and cwd[0] == flp[0]:
        flp.pop(0)
        cwd.pop(0)

    print("|  " * depth + f"|- [[ {dep} –– {('..' + os.path.sep) * len(cwd) + os.path.sep.join(flp)} ]]")

DependencyList = List[ModuleType]

def package_info(mod: ModuleType, msg: str, dependencies: DependencyList) -> FunctionType:
    """Generates the info function for a module, which includes it message (stored in msg) and a list of dependencies (stored in dependencies).

    Args:
        mod (ModuleType): The module for which to generate the info function for
        msg (str): The message to be displayed in the info for this module
        dependencies (DependencyList): A list of dependencies which all have their own info functions

    Returns:
        FunctionType: The info function for a module.
    """
    def get_package_info(depth=0):
        """
        Generic info function for a module. Calling this will print the message and recursivelly print the info for all dependencies.
        """
        if depth:
            print("|  " * (depth - 1) + "|- " + msg)
        else:
            print(msg)
        for dependency in dependencies:
            if dependency == exp_info: continue # comment this line to show the exp_info package in all dependency lists
            try:
                if dependency.info.__module__ != dependency.__name__:
                    unknown(depth, dependency.__name__, dependency.__file__)
                    dependency.info(depth + 2)
                else:
                    dependency.info(depth + 1)
            except AttributeError:
                try:
                    unknown(depth, dependency.__name__, dependency.__file__)
                except AttributeError:
                    unknown(depth, dependency, dependency.__file__)
    try:
        get_package_info.__module__ = mod.__name__
    except AttributeError:
        get_package_info.__module__ = mod
    return get_package_info

info = package_info(exp_info, "exp_info@v1 –– the built-in info package", [])

if __name__ == "__main__": info()