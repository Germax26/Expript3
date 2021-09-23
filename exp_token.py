from exp_info import *

class TOKEN_LIST:
    def __init__(self, buffer = 0):
        self.tokens = []
        self.buffer = buffer
        self.is_list = True

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

    def append(self, token):
        self.tokens.append(token)

    def pop(self, index):
        self.tokens.pop(index)

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