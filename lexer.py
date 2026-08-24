import re


def lexer(codigo):
    tokens = []

    padrao = r"""
        (?P<ESPACO>\s+)
        |(?P<NUMERO>\d+(?:\.\d+)?)
        |(?P<OPERADOR>==|!=|<=|>=|[+\-*/%<>])
        |(?P<LPAR>\()
        |(?P<RPAR>\))
        |(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)
        |(?P<INVALIDO>.)
    """

    for match in re.finditer(padrao, codigo, re.VERBOSE):
        tipo = match.lastgroup
        lexema = match.group()

        if tipo == "ESPACO":
            continue

        if tipo == "INVALIDO":
            raise Exception(
                f"Erro Léxico: caractere inválido '{lexema}'"
            )

        tokens.append((tipo, lexema))

    return tokens


codigo = "(print (+ 10 20))"

tokens = lexer(codigo)

for token, lexema in tokens:
    print(f"{token:<12} {lexema}")