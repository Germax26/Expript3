import importlib.util, sys, os

from exp_info import *

def import_packages(packages):
    """
    To import that packages specified in the packages argument.
    """
    ok = True

    modules = {}

    for package in packages:
        package_name = packages[package].split("/")[-1]
        try:
            spec = importlib.util.spec_from_file_location(f"{package_name}_{package}", f"{package_name}.{package}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[package] = module

        except FileNotFoundError:
            print(f"Package {package_name}.{package} could not be loaded.")
            ok = False

    if not ok: sys.exit()

    return modules

def path(name):
    """
    To get the path of packages that are stored in the expript3 directory.
    """
    return os.path.sep.join(__file__.split(os.path.sep)[:-1]) + os.path.sep + name

exp_package = module(__name__)

info = package_info(exp_package, "exp_package@v1 –– the built-in package package", [exp_info])

if __name__ == "__main__": info()