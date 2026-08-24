from lexer import lexer
from parser import Parser
from semantic import AnalisadorSemantico
from mepa import GeradorMEPA


codigo = "(print (+ 10 20))"


# 1. Análise léxica
tokens = lexer(codigo)


# 2. Análise sintática
parser = Parser(tokens)
arvore = parser.analisar()


# 3. Análise semântica
semantico = AnalisadorSemantico()
tabela = semantico.analisar(arvore)


# 4. Geração MEPA
gerador = GeradorMEPA(tabela)

codigo_mepa = gerador.gerar(arvore)


print("\nCódigo MEPA:")
for instrucao in codigo_mepa:
    print(instrucao)