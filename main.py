from lexer import lexer
from parser import Parser
from semantic import AnalisadorSemantico


codigo = """
(begin
    (set idade 20)
    (set nota 80)
    (print idade)
)
"""

tokens = lexer(codigo)

parser = Parser(tokens)

arvore = parser.analisar()

analisador = AnalisadorSemantico()

tabela = analisador.analisar(arvore)

print("\nTabela de Símbolos:")
print("Identificador | Endereço MEPA | Tipo | Escopo")
print("-" * 50)

for simbolo in tabela.values():
    print(
        f"{simbolo.nome:<13} | "
        f"{simbolo.endereco:<13} | "
        f"{simbolo.tipo:<6} | "
        f"{simbolo.escopo}"
    )