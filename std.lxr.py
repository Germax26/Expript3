import string, sys
from exp_error import *
from exp_token import *
from exp_info import *

class LEXER:
    def __init__(self):
        self.in_repl = False
        self.operators = None

    def lex(self, expr:str, buffer:int=0, depth:int=0) -> TOKEN_LIST:

        if expr.lstrip(" ") == "":
            return None, LexerError("Empty expression!", buffer, 1, expr, "EmptyExpressionError")

        is_at_end = False
        current_ix = -1
        current_char = None
        tokens = TOKEN_LIST(expr)

        def advance():
            nonlocal current_char, current_ix, is_at_end
            current_ix += 1
            is_at_end = current_ix >= len(expr)
            current_char = expr[current_ix] if not is_at_end else None

        def get_char_type(char:str):
            if char in " \n\t": return "white-space"
            if char == "(": return "left-paren"
            if char == ")": return "right-paren"
            if char == '"': return "quote"
            if char in string.ascii_letters+string.digits + "_": return "value"
            return "operator"

        advance() 

        while not is_at_end:
            char_type = get_char_type(current_char)
            if char_type == "quote":
                current_origin = current_ix
                current = ""
                advance()
                escape = False

                while not is_at_end and (escape or current_char != '"'):
                    if current_char == "\\":
                        escape = True
                    else:
                        current += current_char
                        escape = False
                    advance()

                if is_at_end:
                    return None, LexerError("Unterminated string.", current_origin + buffer, len(current) + 2, expr, "UnterminatedStringError")

                advance()

                tokens.append(TOKEN(f'"{current}"', "value", current_origin + buffer, len(current) + 2))

                # return exp_error.not_implemented("Strings are not implemented.", current_origin + buffer, len(current) + 2, expr, "lexer")
            
            elif char_type in ["value", "operator"]:
                current = ""
                current_origin = current_ix
                while not is_at_end and get_char_type(current_char) == char_type:
                    current += current_char
                    advance()
                if self.operators and char_type == "value" and current in self.operators.alpha:
                    char_type = "operator"
                tokens.append(TOKEN(current, char_type, current_origin + buffer, len(current)))

            elif char_type == "left-paren":
                current = ""
                current_origin = current_ix
                indent = 0
                advance()

                while not is_at_end and (current_char != ")" or indent):
                    if current_char == "(":
                        indent += 1
                    elif current_char == ")":
                        indent -= 1
                    current += current_char
                    advance()

                # return exp_error.not_implemented("Subexpressions are not implemented.", current_origin + buffer, current_ix - current_origin + 1, expr, "lexer")

                if is_at_end:
                    return None, LexerError("Unmatched left parenthesis!", current_origin + buffer, 1, expr, "UnmatchedLeftParenthesisError")
                
                if current_ix - current_origin == 1:
                    tokens.append(TOKEN("()", "value", current_origin, 2))
                    advance()
                    continue
                
                advance()    

                subtokens, err = self.lex(current, current_origin + buffer + 1, depth + 1)
                if err: return None, err
                tokens.append(subtokens)

            elif char_type == "right-paren":
                return None, LexerError("Unmatched right parenthesis!", current_ix + buffer, 1, expr, "UnmatchedRightParenthesisError")
            
            elif char_type == "white-space":
                # tokens.append(TOKEN(current_char, char_type, current_ix, 1))
                advance()

            else:
                return None, LexerError(f"Invalid character type! Got {char_type}.", current_ix + buffer,  1, expr, "InvalidCharacterTypeError")
        
        while not depth and self.in_repl and not tokens[-1].is_list and tokens[-1].token_type == "operator":
            new_source = ""
            while True:
                new_source = input("... ")
                if new_source.lstrip(" "):
                    new_source = "\n" + new_source
                    break
            new_tokens, err = self.lex(new_source, buffer + len(expr))
            if err: return None, err
            tokens += new_tokens
        return tokens, None

std_lxr = module(LEXER)

info = package_info(std_lxr, "std.lxr@v1 –– the standard lexer", [exp_error, exp_token, exp_info])

if __name__ == "__main__": info()
