from exp_info import *

class NODE_LIST:
    def __init__(self):
        self.nodes = []
        
    def __setitem__(self, index, value):
        self.nodes[index] = value

    def __getitem__(self, index):
        return self.nodes[index]

    def display(self, buffer=0):
        for node in self.nodes:
            node.display(depth=0, buffer=buffer)

    def append(self, token):
        self.nodes.append(token)

    def pop(self, index):
        self.nodes.pop(index)

    def length(self):
        return len(self.nodes)

class NODE:
    def __init__(self, value, node_type, span_left, span_right):
        self.value = value
        self.node_type = node_type

        self.is_op = False
        self.in_sub = False

        self.left = None
        self.right = None

        self.span_left = span_left
        self.span_right = span_right

        self.span = self.span_left, self.span_right

    def uberspan(self):
        return self.left_span(), self.right_span()

    def __repr__(self):
        return f"Node: {self.node_type}, Span: {self.span_left}+{self.span_right}, Is_Op: {self.is_op}, Value: {self.value}"

    def display(self, depth=0, buffer=0):
        print(' ' * buffer * 3 + (' ' * (depth-1) * 3 + '|- ' if depth != 0 else '') + str(self))
        if self.left : self.left .display(depth + 1, buffer)
        if self.right: self.right.display(depth + 1, buffer)

    def string(self, depth=0):
        result = ""

        if self.left: result += self.left.string(depth+1) + " "

        result += self.value

        if self.right: result += " " + self.right.string(depth+1)

        if depth and (self.left or self.right): result = f"({result})"

        return result

    def left_span(self):
        if self.left:
            return self.left.left_span() - self.in_sub
        return self.span_left

    def right_span(self):
        span_right = self.span_left + self.span_right
        if self.right:
            span_right = self.right.left_span() + self.right.right_span()
        return span_right - self.left_span() + self.in_sub

exp_node = module(NODE)

info = package_info(exp_node, "exp_node@v1 –– the built-in node package", [exp_info])

if __name__ == "__main__": info()