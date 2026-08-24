import re


PALAVRAS_RESERVADAS = {
    "if": "IF",
    "while": "WHILE",
    "begin": "BEGIN",
    "set": "SET",
    "print": "PRINT"
}


def lexer(codigo):
    tokens = []

    padrao = r"""
        (?P<ESPACO>\s+)
        |(?P<FLOAT>\d+\.\d+)
        |(?P<INTEGER>\d+)
        |(?P<OPERADOR>==|!=|<=|>=|[+\-*/%<>])
        |(?P<LPAR>\()
        |(?P<RPAR>\))
        |(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)
        |(?P<INVALIDO>.)
    """

    linha = 1

    for match in re.finditer(padrao, codigo, re.VERBOSE):
        tipo = match.lastgroup
        lexema = match.group()

        # Conta quantas linhas existem no trecho encontrado
        if tipo == "ESPACO":
            linha += lexema.count("\n")
            continue

        # Caractere que não pertence à linguagem
        if tipo == "INVALIDO":
            raise Exception(
                f"Erro Léxico: Caractere inválido "
                f"'{lexema}' na linha {linha}."
            )

        # Identifica palavras reservadas
        if tipo == "ID" and lexema in PALAVRAS_RESERVADAS:
            tipo = PALAVRAS_RESERVADAS[lexema]

        # Padroniza operadores
        if tipo == "OPERADOR":
            tipo = "OP"

        tokens.append({
            "token": tipo,
            "lexema": lexema,
            "linha": linha
        })

    return tokens

codigo = """
(begin
    (set idade 20)
    (print (+ idade 5))
)
"""

tokens = lexer(codigo)

for token in tokens:
    print(
        f"{token['token']:<10}"
        f"{token['lexema']:<10}"
        f"linha {token['linha']}"
    )