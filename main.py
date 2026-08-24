import sys

from lexer import lexer
from parser import Parser
from semantic import AnalisadorSemantico
from mepa import GeradorMEPA


def compilar(arquivo):
    try:
        # LEITURA DO ARQUIVO
        with open(arquivo, "r", encoding="utf-8") as f:
            codigo = f.read()

        # ANÁLISE LÉXICA
        tokens = lexer(codigo)

        print("\n=== TOKENS / LEXEMAS ===")

        for token in tokens:
            print(
                f"{token['token']:<10} "
                f"{token['lexema']:<10} "
                f"linha {token['linha']}"
            )

        # ANÁLISE SINTÁTICA
        parser = Parser(tokens)
        arvore = parser.analisar()

        # ANÁLISE SEMÂNTICA
        semantico = AnalisadorSemantico()
        tabela = semantico.analisar(arvore)

        print("\n=== TABELA DE SÍMBOLOS ===")

        if not tabela:
            print("Vazia")
        else:
            print(
                f"{'Identificador':<15}"
                f"{'Endereço':<12}"
                f"{'Tipo':<10}"
                f"{'Escopo'}"
            )

            for simbolo in tabela.values():
                print(
                    f"{simbolo.nome:<15}"
                    f"{simbolo.endereco:<12}"
                    f"{simbolo.tipo:<10}"
                    f"{simbolo.escopo}"
                )

        # GERAÇÃO MEPA
        gerador = GeradorMEPA(tabela)
        codigo_mepa = gerador.gerar(arvore)

        print("\n=== CÓDIGO MEPA ===")

        for instrucao in codigo_mepa:
            print(instrucao)

    except Exception as erro:
        print(f"\n{erro}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Uso: python main.py <arquivo.lisp>"
        )
        sys.exit(1)

    compilar(sys.argv[1])