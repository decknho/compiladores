from lexer import lexer
from parser import Parser


codigo = """
(begin
    (set contador 1)
    (while (<= contador 10)
        (begin
            (print contador)
            (set contador (+ contador 1))
        )
    )
)
"""

tokens = lexer(codigo)

parser = Parser(tokens)

arvore = parser.analisar()

print("AST:")
print(arvore)