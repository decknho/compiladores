class Numero:
    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Numero({self.valor})"


class Operacao:
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

    def __repr__(self):
        return (
            f"Operacao('{self.operador}', "
            f"{self.esquerda}, {self.direita})"
        )


class Print:
    def __init__(self, expressao):
        self.expressao = expressao

    def __repr__(self):
        return f"Print({self.expressao})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def atual(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]

        return None

    def consumir(self):
        token = self.atual()

        if token is not None:
            self.posicao += 1

        return token

    def erro(self, mensagem):
        token = self.atual()

        if token:
            raise Exception(
                f"Erro Sintático na linha "
                f"{token['linha']}: {mensagem}"
            )

        raise Exception(f"Erro Sintático: {mensagem}")

    def analisar(self):
        arvore = self.expressao()

        if self.atual() is not None:
            self.erro(
                f"Token inesperado '{self.atual()['lexema']}'."
            )

        return arvore

    def expressao(self):
        token = self.atual()

        if token is None:
            self.erro("Expressão inesperadamente vazia.")

        if token["token"] == "INTEGER":
            self.consumir()
            return Numero(int(token["lexema"]))

        if token["token"] == "FLOAT":
            self.consumir()
            return Numero(float(token["lexema"]))

        if token["token"] == "LPAR":
            return self.lista()

        self.erro(
            f"Token '{token['lexema']}' não pode iniciar "
            f"uma expressão."
        )

    def lista(self):
        self.consumir()  # (

        token = self.atual()

        if token is None:
            self.erro(
                "Fim de arquivo inesperado. "
                "Esperava-se ')'."
            )

        # print
        if token["token"] == "PRINT":
            self.consumir()

            expressao = self.expressao()

            if self.atual() is None:
                self.erro(
                    "Fim de arquivo inesperado. "
                    "Esperava-se ')'."
                )

            if self.atual()["token"] != "RPAR":
                self.erro(
                    "Esperava-se ')' após o argumento de print."
                )

            self.consumir()

            return Print(expressao)

        # operações
        if token["token"] == "OP":
            operador = self.consumir()["lexema"]

            esquerda = self.expressao()
            direita = self.expressao()

            if self.atual() is None:
                self.erro(
                    "Fim de arquivo inesperado. "
                    "Esperava-se ')'."
                )

            if self.atual()["token"] != "RPAR":
                self.erro(
                    "Operação deve possuir exatamente "
                    "dois operandos."
                )

            self.consumir()

            return Operacao(
                operador,
                esquerda,
                direita
            )

        self.erro(
            f"Construção '{token['lexema']}' ainda "
            f"não é suportada pelo Parser."
        )