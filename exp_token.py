from exp_info import *

class TOKEN_LIST:
    def __init__(self, expr, buffer = 0):
        self.tokens = []
        self.buffer = buffer
        self.is_list = True
        self.full = expr
        self.token_type = "value"
        self.span_left = None
        self.span_right = None
        self.span = None, None

    def __setitem__(self, index, value):
        self.tokens[index] = value

    def __getitem__(self, index):
        return self.tokens[index]

    def display(self, depth=0):
        for token in self.tokens:
            if token.is_list:
                token.display(depth + 1)
            else:
                print("  " * depth + str(token))

    def length(self):
        return len(self.tokens)

    def append(self, token):
        self.tokens.append(token)
        if self.length() == 1:
            self.span_left = token.span_left - 1
        self.span_right = token.span_right + token.span_left - self.span_left + 1
        self.span = self.span_left, self.span_right

    def __add__(self, other):
        new_tokens = TOKEN_LIST(self.full + other.full, buffer=self.buffer)
        new_tokens.tokens = self.tokens + other.tokens
        return new_tokens

    def pop(self, index):
        return self.tokens.pop(index)

class TOKEN:
    def __init__(self, value, token_type, span_left, span_right):
        self.value = value
        self.token_type = token_type

        self.span_left = span_left
        self.span_right = span_right

        self.span = self.span_left, self.span_right

        self.is_list = False
        
    def __repr__(self):
        return f"Token: {self.token_type}, Span: {self.span_left}+{self.span_right}, Value: {self.value} "

exp_token = module(__name__)

info = package_info(exp_token, "exp_token@v1 –– the built-in token package", [])

if __name__ == "__main__": info()