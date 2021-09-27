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

        def parse_value(tokens):
            if tokens[0].token_type == "value":
                return to_node(self, expr, tokens.pop(0), categories, depth)
            return None, ParserError(f"Expected value. Got {tokens[0].token_type} instead.", *tokens[0].span, expr, "ExpectedValueError")

        def parse_category(tokens, category_index):
            category = categories.categories[category_index]

            def parse_lower(drop=1):
                return parse_category(tokens, category_index - drop) if category_index - drop + 1 else parse_value(tokens)
            
            if "unary" in category.tags:
                if tokens[0].token_type == "operator":
                    operator, err = to_node(self, expr, tokens.pop(0), categories, depth)
                    if err: return None, err

                    for potential_category in categories.categories:
                        if "unary" in potential_category.tags:
                            if potential_category.contains(operator.value):
                                break
                    else:
                        return None, ParserError(f"Unknown unary operator '{operator.value}'.", *operator.span, expr, "UnknownUnaryOperatorError")

                    if not tokens.length():
                        return None, ParserError("Expected value after unary operator. Got EOF instead.", len(expr) + 1, 1, expr, "ExpectedValueAfterUnaryOperatorError")

                    right, err = parse_lower(0)
                    if err: return None, err

                    operator.right = right
                    operator.node_type = "value"
                    operator.is_op = True

                    return operator, None
                else:
                    return parse_lower()
            else:
                left, err = parse_lower()
                if err: return None, err
                
                series = [left]

                while tokens.length() and ((tokens[0].token_type == "operator" and category.contains(tokens[0].value)) or ("implied" in category.tags and tokens[0].token_type == "value")):
                    if tokens[0].token_type == "operator":
                        operator, err = to_node(self, expr, tokens.pop(0), categories, depth)
                    elif tokens[0].token_type == "value":
                        operator = NODE(list(category.operators)[0], "operator", tokens[0].span_left, 1)
                    if err: return None, err

                    series.append(operator)

                    if not tokens.length():
                        return None, ParserError("Expected value after binary operator.", operator.span_left + 1, 1, expr, "ExpectedValueAfterBinaryOperatorError")

                    right, err = parse_lower()
                    if err: return None, err

                    series.append(right)

                if len(series) == 1: return series[0], None

                while len(series) > 2:
                    index = len(series) - 2 if "reverse-collapse" in category.tags else 1
                    
                    series[index].left  = series[index - 1]
                    series[index].right = series[index + 1]
                    series[index].node_type = "value"
                    series[index].is_op = True

                    series.pop(index + 1)
                    series.pop(index - 1)
                
                if len(series) > 1:
                    return None, ParserError("Pariahs!", series[1].left_span(), series[-1].left_span() + series[-1].right_span() - series[1].left_span(), expr, "PariahNodesError")

                return series[0], None
    
        root, err = parse_category(tokens, len(categories.categories) - 1)
        if err: return None, err

        if tokens.length():
            if tokens[0].token_type == "value":
                return None, ParserError("Expected operator. Got value instead.", *tokens[0].span, expr, "ExpectedOperatorError")
            elif tokens[0].token_type == "operator":
                return None, ParserError(f"Unknown binary operator '{tokens[0].value}'.", *tokens[0].span, expr, "UnknownBinaryOperatorError")
            return None, ParserError("Überpariahs!", tokens[0].span_left, len(expr) - tokens[0].span_left, expr, "ÜberparaihNodesError")

        return root, None

std_psr = module(PARSER)

info = package_info(std_psr, "std.psr@v2 –– the standard parser", [exp_node, exp_error, exp_info])

if __name__ == "__main__": info()
