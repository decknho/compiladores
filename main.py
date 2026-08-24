from lexer import lexer
from parser import Parser


codigo = """
(if (> idade 18)
    (print 1)
)
"""

tokens = lexer(codigo)

parser = Parser(tokens)

arvore = parser.analisar()

print("AST:")
print(arvore)