from lexer import lexer
from parser import Parser


codigo = "(+ 10 20)"

tokens = lexer(codigo)

parser = Parser(tokens)

arvore = parser.analisar()

print("AST:")
print(arvore)