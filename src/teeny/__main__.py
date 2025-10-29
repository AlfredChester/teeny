#!/usr/bin/env python3
import sys
from teeny.lexer import tokenize
from teeny.parser import parse
from teeny.processor import process
from teeny.interpreter import interpret
from teeny.exception import LexicalError, SyntaxError, RuntimeError
from teeny.value import makeObject

def run_file(path: str):
    try:
        src = open(path, "r", encoding="utf-8").read()
        tokens = tokenize(src)
        ast, _ = parse(tokens, 0)
        result = interpret(process(ast))
        if result is not None:
            print(makeObject(result))
    except FileNotFoundError:
        print(f"File not found: {path}")
    except (LexicalError, SyntaxError, RuntimeError) as e:
        print(e)

def main():
    if len(sys.argv) < 2:
        print("Usage: teeny <file.ty>")
        sys.exit(1)
    run_file(sys.argv[1])

if __name__ == "__main__":
    main()
