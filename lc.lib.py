from exp_error import *
from exp_package import *
from exp_info import *

std_lib = import_package(here("std"), "lib")

def Identity(f, _):
    return f, None

def Mockingbird(f, context):
    if callable(f):
        return f(f, context)
    return None, InterpreterError("Can't call given input on itself.", *context.right.span, context.expr, "MockingbirdError")

class LIBRARY:
    def __init__(self):
        std = std_lib.LIBRARY() 
        self.values = {**std.values,
            "I": Identity,
            "M": Mockingbird,
        }
        self.variables = {**std.variables,
            "K": "Kestrel = a => b => a; Kestrel",
            "Ki": "Kite = K <- I; Kite",
            "C": "Cardinal = f => a => b => f <- b <- a; Cardinal",
            "B": "Bluebird = f => g => b => f <- (g <- b); Bluebird",
            "Th": "Thrush = a => f => f <- a; Thrush",
            "V": "Vireo = B <- C <- Th; Vireo",
            "B1": "Blackbird = B <- B <- B; Blackbird",
            "S": "Sterling = a => b => c => a <- c <- (b <- c); Sterling",
            "Y": "f => (x => f <- (x <- x)) <- (x => f <- (x <- x))",

            "T": "True = K; True",
            "F": "False = Ki; False",

            "not": "Not = p => p <- F <- T; Not",
            "and": "And = p => q => p <- q <- p; And",
            "or": "Or = p => q => p <- p <- q; Or",
            "beq": "BooleanEquality = p => q => p <- q <- (not <- q); BooleanEquality",

            "exp_num": "ExpriptNumber = n => n <- (x => x + 1) <- 0; ExpriptNumber",
            "exp_bool": "ExpriptBoolean = b => b <- true <- false; ExpriptBoolean",

            "succ": "Successor = n => f => a => f <- (n <- f <- a); Successor",

            "n0": "Zero = f => a => a; Zero",
            "n1": "One = f => a => f <- a; One",
            "n2": "Two = f => a => f <- (f <- a); Two",
            "n3": "Three = f => a => f <- (f <- (f <- a)); Three",
            "n4": "Four = f => a => f <- (f <- (f <- (f <- a))); Four",

            "add": "Addition = n => k => n <- succ <- k; Addition",

            "n5": "Five = add <- n2 <- n3; Five",
            "n6": "Six = add <- n2 <- n4; Six",
            "n7": "Seven = add <- n3 <- n4; Seven",

            "mult": "Multiplication = B; Multiplication",

            "n8": "Eight = mult <- n2 <- n4; Eight",

            "pow": "Exponentiation = Th; Exponentiation",
            
            "n9": "Nine = pow <- n3 <- n2; Nine",
            "n10": "Ten = mult <- n2 <- n5; Ten",


            "is_zero": "IsZero = n => n <- (K <- F) <- T; IsZero",


            "pair": "Pair = a => b => f => f <- a <- b; Pair",

            "fst": "First = p => p <- K; First",
            "snd": "Second = p => p <- Ki; Second",

            "phi": "Phi = p => V <- (snd <- p) <- (B <- succ <- snd <- p); Phi",
            "pred": "Predecessor = n => fst <- (n <- phi <- (pair <- n0 <- n0)); Predecessor",
            "sub": "Subtraction = n => k => k <- pred <- n; Subtraction",

            "leq": "LessThanOrEqualTo = n => k => is_zero <- (sub <- n <- k); LessThanOrEqualTo",
            "eq": "Equality = n => k => and <- (leq <- n <- k) <- (leq <- k <- n); Equality",
            "gt": "GreaterThan = B1 <- not <- leq; GreaterThan",

            "div_inner": "c => n => m => f => x => (d => is_zero <- d <- (n0 <- f <- x) <- (f <- (c <- d <- m <- f <- x))) <- (sub <- n <- m)",
            "divide1": "Y <- div_inner",
            "div": "Division = n => divide1 <- (succ <- n); Division",


            "nil": "V <- T <- T",
            "is_nil": "IsNil = fst; IsNil",
            "cons": "Construct = h => t => V <- F <- (V <- h <- t); Construct",
            "head": "Head = p => B <- fst <- snd <- p; Head",
            "tail": "Tail = p => B <- snd <- snd <- p; Tail"
        }

lc_lib = module(LIBRARY)

info = package_info(lc_lib, "lc.lib@v1 –– the lambda calculus library", [exp_error, exp_package, exp_info, std_lib])

if __name__ == "__main__": info()