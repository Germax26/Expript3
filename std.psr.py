from exp_node import *
from exp_error import *
from exp_info import *

def to_node(parser, expr, token, operators, depth):
    if token.is_list:
        root, err = parser.parse(expr, token, operators, depth+1)
        if err: return None, err
        root.in_sub = True
        return root, None
    return NODE(token.value, token.token_type, *token.span), None

class PARSER:
    def __init__(self, lexer):
        self.debug = False
        self.lexer = lexer

    def parse(self, expr, tokens, operators, depth=0):

        nodes = NODE_LIST()

        for i, token in enumerate(tokens.tokens):
            if not token.is_list and token.token_type not in ["value", "operator"]:
                return None, ParserError(f"Invalid token. Got token type '{token.token_type}'.", token.span_left, token.span_right, expr, "InvalidTokenError").add_callback("in token conversion")
            new_node, err = to_node(self, expr, token, operators, depth)
            if err: return None, err
            nodes.append(new_node)

        if self.debug:
            print("Nodes:")
            nodes.display(depth)
            print()

        current_ix = nodes.length() - 1

        has_changed = False

        while current_ix + 1:
            current_type = nodes[current_ix].node_type

            next_type = "operator"
            if current_ix:
                next_type = nodes[current_ix - 1].node_type
            
            if current_type == next_type == "operator":
                if current_ix + 1 == nodes.length() or nodes[current_ix + 1].node_type == 'operator':
                    return None, ParserError(f"Unexpected operator '{nodes[current_ix + (plus_one := current_ix + 1 != nodes.length())].value}'.", *nodes[current_ix + plus_one].span, expr, "UnexpectedOperatorError")

                nodes[current_ix].right = nodes[current_ix+1]
                nodes[current_ix].node_type = 'value'
                nodes[current_ix].is_op = True

                nodes.pop(current_ix + 1)

                has_changed = True
            
            if current_type == next_type == "value":
                return None, ParserError(f"Unexpected value '{nodes[current_ix].value}''.", *nodes[current_ix].uberspan(), expr, "UnexpectedValueError")

            current_ix -= 1

        if self.debug and has_changed:
            print("After category \"Unary\"")
            nodes.display(depth)
            print()

        if nodes[-1].node_type == "operator":
            return None, ParserError(f"Unexpected operator '{nodes[-1].value}'", *nodes[-1].span, expr, "UnexpectedOperatorError")

        for category in operators.binary:
            step = -1 if "reverse-collapse" in category.tags else 1
            current_ix = nodes.length() -1 if step == -1 else 0

            has_changed = False

            while 0 <= current_ix < nodes.length():
                if nodes[current_ix].node_type == "operator" and category.contains(nodes[current_ix].value):
                    nodes[current_ix].left = nodes[current_ix - 1]
                    nodes[current_ix].right = nodes[current_ix + 1]
                    nodes[current_ix].node_type = "value"
                    nodes[current_ix].is_op = True
                    nodes.pop(current_ix - 1)
                    nodes.pop(current_ix)
                    current_ix -= 1
                    has_changed = True

                current_ix += step

            if self.debug and has_changed:
                print(f"After category \"{category.name}\"")
                nodes.display(depth)
                print()

        while nodes.length() > 2:
            nodes[1].left = nodes[0]
            nodes[1].right = nodes[2]
            nodes[1].node_type = "value"
            nodes[1].is_op = True

            nodes.pop(0)
            nodes.pop(1)

        if nodes.length() > 1:
            return None, ParserError("Paraihs!", nodes[1].left_span(), len(expr) - nodes[1].left_span(), expr, "ParaihNodeError").add_callback("after binary collapse")

        return nodes[0], None

std_psr = module(PARSER)

info = package_info(std_psr, "std.psr@v1 –– the standard parser", [exp_node, exp_error, exp_info])

if __name__ == "__main__": info()
