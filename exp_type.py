from exp_info import *

def stringify(klass, force_type=False):
    x = type(klass)
    if not force_type and x == type:
        x = klass
    return str(x)[8:-2].split('.')[-1]

exp_type = module(__name__)

info = package_info(exp_type, "exp_type@v1 –– the type package", [exp_info])

if __name__ == "__main__": info()