def evaluate(source, lexer, parser, interpreter, operators, variables, debug=False):

    tokens, err = lexer.lex(source)
    if err: return None, err

    if debug:
        print("Tokens:")
        tokens.display()
        print()

    root, err = parser.parse(source, tokens, operators)
    if err: return None, err

    if debug:
        print("AST:")
        root.display()
        print()

    return interpreter.interpret(source, root, operators, variables)

if __name__ == "__main__":
    print(f"It looks like you tried to run {__file__}!")
    print("Try running the shell3.py file instead.")