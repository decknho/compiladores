from lexer import lexer
from parser import Parser


codigo = "(print 10"

tokens = lexer(codigo)

parser = Parser(tokens)

arvore = parser.analisar()

print("AST:")
print(arvore)