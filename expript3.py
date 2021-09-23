def evaluate(source, lexer, parser, interpreter, operators, variables, debug=False):

    tokens, err = lexer.lex(source)
    if err: return None, err

    final_source = tokens.full

    if debug:
        print("Tokens:")
        tokens.display()
        print()

    root, err = parser.parse(final_source, tokens, operators)
    if err: return None, err

    if debug:
        print("AST:")
        root.display()
        print()

    return interpreter.interpret(final_source, root, operators, variables)

if __name__ == "__main__":
    print(f"It looks like you tried to run {__file__}!")
    print("Try running the shell3.py file instead.")