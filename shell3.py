#! /usr/bin/env python3

import string

from exp_package import *
from exp_info import *
from exp_variable import *

from expript3 import evaluate


std = path("std")

packages = {
    "lxr": std, 
    "psr": std, 
    "int": std, 
    "ops": std, 
    "lib": std,
    "rpr": std
}

src = None

debug = False
info = False

for arg in sys.argv:
    sarg = arg.split("=")
    if len(sarg) == 1:
        if arg == "--debug":
            debug = True
        if arg == "--info":
            info = True
    else:
        param = sarg[0]
        value = sarg[1]
        if param in packages:
            packages[param] = value
        elif param == "src":
            src = value


packs = import_packages(packages)

lxr = packs['lxr']
psr = packs['psr']
int = packs['int']
ops = packs['ops']
lib = packs['lib']
rpr = packs['rpr']

lexer = lxr.LEXER()
parser = psr.PARSER(lexer)
interpreter = int.INTERPRETER(lexer, parser)
operators = ops.OPERATORS()
library = lib.LIBRARY(ops)
representer = rpr.REPRESENTER()

lexer.operators = operators
parser.debug = debug
operators.alpha = []
for category in operators.categories:
    for operator in category.operators:
        if type(operator) != str:
            continue
        for char in operator:
            if char in string.ascii_letters+string.digits + "_":
                operators.alpha.append(operator)
                break

variables = VARIABLE_LIST()

for variable in library.values:
    variables.add(VARIABLE(variable, library.values[variable]))

def resolve_err(err):
    if err:
        try:
            err.display()
        except AttributeError:
            print("Internal error:", err)
    return err

def resolve(source):
    result, err = evaluate(source, lexer, parser, interpreter, operators, variables, debug)
    if resolve_err(err): return
    if print_str := representer.represent(result) : print(print_str)

for variable in library.variables:
    result, err = evaluate(library.variables[variable], lexer, parser, interpreter, operators, variables)
    if err: err.display(); sys.exit()
    variables.add(VARIABLE(variable, result))

if src:
    try:
        _file = open(src, "r")
        source = _file.read()
        _file.close()

        if source.lstrip(" "):
            resolve(source)

    except IOError:
        print(f"The source {src} could not be loaded.")

    sys.exit()

shell3 = __import__(__name__)

def get_info():
    package_info(shell3, "shell3@v1 –– the built-in expript3 shell", [exp_package, exp_info, exp_variable, lxr, psr, int, ops, lib])()

if info:
    get_info()
    sys.exit()

print("Use '^C' to enter the command palette.")

lexer.in_repl = True

while True:
    try:
        source = input("> ").strip(" ")

        if not source: continue

        resolve(source)

    except (KeyboardInterrupt, EOFError) as err:
        if type(err) == KeyboardInterrupt:
            print("\nEntering the command palette.")
            print("Enter 'help' to to get a list of commands.")

        while True:
            try:
                command = input("|> ").lower()
            except EOFError: print("\nBye."); sys.exit(1)
            except KeyboardInterrupt: break
            
            if not command: pass

            elif command == "h" or command == "help":
                print("'h' or 'help': the list of commands")
                print("'q' or 'quit': exit shell")
                print("'db' or 'debug': toggle debug info")
                print("'e' or 'exit': exit the command palette")
                print("'i' or 'info': the list of dependencies of shell3")
            
            elif command == "q" or command == "quit":
                print("Bye.")
                sys.exit(1)
            
            elif command == "db" or command == "debug":
                debug = not debug
                if debug:
                    print("Debug is now on.")
                else:
                    print("Debug is now off.")

                parser.debug = debug
                
            elif command == "e" or command == "exit":
                break

            elif command == "i" or command == "info":
                get_info()

            else:
                print("Unknown command. Please try something else.")

            if type(err) == EOFError: break

        if type(err) == KeyboardInterrupt: print("\nExiting the command palette.")