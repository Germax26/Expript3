from exp_node import *
from exp_error import *
from exp_info import *

def to_node(parser, expr, token, categories, depth):
    if token.is_list:
        root, err = parser.parse(expr, token, categories, depth+1)
        if err: return None, err
        root.in_sub = True
        return root, None
    return NODE(token.value, token.token_type, *token.span), None

class PARSER:
    def __init__(self, lexer):
        self.debug = False
        self.lexer = lexer

    def parse(self, expr, tokens, categories, depth=0):

        nodes = NODE_LIST()

        for i, token in enumerate(tokens.tokens):
            if not token.is_list and token.token_type not in ["value", "operator"]:
                return None, ParserError(f"Invalid token. Got token type '{token.token_type}'.", token.span_left, token.span_right, expr, "InvalidTokenError")
            
            if token.is_list:
                root, err = self.parse(expr, token, categories, depth + 1)
                if err: return None, err
                root.in_sub = True
                nodes.append(root)
            else:
                nodes.append(NODE(token.value, token.token_type, *token.span))

        if self.debug:
            print("Nodes:")
            nodes.display(depth)
            print()

        for category in categories.categories:
            changed = False
            if "unary" in category.tags:

                changed = self.apply_unary_category(nodes, category, categories, False, depth)

            else:
                step = -1 if "reverse-collapse" in category.tags else 1
                current_ix = nodes.length() - 1 if step == -1 else 0

                while (0 <= current_ix) and (current_ix < nodes.length()):
                    if nodes[current_ix].node_type == "operator" and category.contains(nodes[current_ix].value):
                        nodes[current_ix].left = nodes[current_ix - 1]
                        nodes[current_ix].right = nodes[current_ix + 1]
                        nodes[current_ix].node_type = "value"
                        nodes[current_ix].is_op = True
                        nodes.pop(current_ix - 1)
                        nodes.pop(current_ix)
                        current_ix -= 1
                        changed = True

                    current_ix += step

                if self.debug and changed: self.display_nodes(nodes, category.name, True, depth)
        
        self.apply_unary_category(nodes, "unary", categories, True, depth)

        len_nodes = nodes.length()

        while nodes.length() > 2:
            nodes[1].left = nodes[0]
            nodes[1].right = nodes[2]
            nodes[1].node_type = "value"
            nodes[1].is_op = True
            
            nodes.pop(0)
            nodes.pop(1)

        if len_nodes != nodes.length(): self.display_nodes(nodes, "binary", False, depth)

        if nodes.length() > 1:
            return None, ParserError("Paraihs!", nodes[1].left_span(), len(expr) - nodes[1].left_span(), expr, "ParaihNodeError")

        return nodes[0], None

    def display_nodes(self, nodes, name, is_category, depth):
        if is_category:
            print(f"{depth*'   '}After category \"{name}\"\n")
        else:
            print(f"{depth*'   '}After unknown {name} operators\n")
        nodes.display(depth)
        print()

    def apply_unary_category(self, nodes, category, categories, force_contain, depth):
        changed = False

        current_ix = nodes.length() - 1

        while current_ix + 1:
            current_type = nodes[current_ix].node_type

            if current_type == "operator":
                if force_contain or category.contains(nodes[current_ix].value):

                    next_type = "operator"
                    if current_ix:
                        next_type = nodes[current_ix - 1].node_type
                    
                    if current_type == next_type:
                        if nodes[current_ix + 1].node_type == 'operator':
                            current_ix -= 1
                            continue
                        if current_ix + 1 == nodes.length():
                            return None, ParserError(f"Unexpected EOF '{nodes[current_ix + (plus_one := current_ix + 1 != nodes.length())].value}'.", nodes[current_ix + plus_one].span_left + nodes[current_ix + plus_one].span_right, 1, expr, "UnexpectedEOFError")

                        nodes[current_ix].right = nodes[current_ix + 1]
                        nodes[current_ix].node_type = "value"
                        nodes[current_ix].is_op = True

                        nodes.pop(current_ix + 1)

                        changed = True

            current_ix -= 1

        if changed:
            if self.debug:
                self.display_nodes(nodes, category if force_contain else category.name, not force_contain, depth)
            for prev_category in categories.categories:
                self.apply_unary_category(nodes, prev_category, categories, False, depth)
    
        return changed

std_psr = module(PARSER)

info = package_info(std_psr, "std.psr@v1 –– the standard parser", [exp_node, exp_error, exp_info])

if __name__ == "__main__": info()
