import importlib.util, sys, os

from exp_info import *

def packages_init():
    global modules
    modules = {}

def import_package(package_name, package_type):
    """
    To import the package specified by package_type and package_name.
    """

    module_name = package_name.split("/")[-1] + "_" + package_type

    if module_name in modules:
        return modules[module_name]

    try:

        spec = importlib.util.spec_from_file_location(module_name, f"{package_name}.{package_type}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[module_name] = module
        return module

    except FileNotFoundError:
        print(f"Package {package_name}.{package_type} could not be loaded.")
        sys.exit()

def here(name):
    """
    To get the path of packages that are stored in the expript3 directory.
    """
    return os.path.sep.join(__file__.split(os.path.sep)[:-1]) + os.path.sep + name

exp_package = module(__name__)

info = package_info(exp_package, "exp_package@v1.1 –– the built-in package package", [exp_info])

if __name__ == "__main__": info()