class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def atual(self):
        """Retorna o token atual sem avançar."""
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]

        return None

    def consumir(self):
        """Consome o token atual e avança para o próximo."""
        token = self.atual()

        if token is not None:
            self.posicao += 1

        return token

    def analisar(self):
        """Inicia a análise sintática do programa."""
        arvore = self.expressao()

        # Se ainda existem tokens, significa que
        # encontramos mais de uma expressão no programa.
        if self.atual() is not None:
            token = self.atual()

            raise Exception(
                f"Erro Sintático: token inesperado "
                f"'{token['lexema']}' na linha {token['linha']}."
            )

        return arvore

    def expressao(self):
        """Analisa uma expressão."""

        token = self.atual()

        if token is None:
            raise Exception(
                "Erro Sintático: expressão inesperadamente vazia."
            )

        # Se começar com (, temos uma lista.
        if token["token"] == "LPAR":
            return self.lista()

        # Caso contrário, temos um átomo.
        if token["token"] in [
            "INTEGER",
            "FLOAT",
            "ID",
            "OP",
            "IF",
            "WHILE",
            "BEGIN",
            "SET",
            "PRINT"
        ]:
            return self.consumir()

        raise Exception(
            f"Erro Sintático: token inesperado "
            f"'{token['lexema']}' na linha {token['linha']}."
        )

    def lista(self):
        """Analisa uma expressão entre parênteses."""

        # Consome o '('
        self.consumir()

        elementos = []

        while True:
            token = self.atual()

            # Acabou o arquivo antes do ')'
            if token is None:
                raise Exception(
                    "Erro Sintático: Fim de arquivo inesperado. "
                    "Esperava-se ')'."
                )

            # Encontrou o ')'
            if token["token"] == "RPAR":
                self.consumir()
                break

            # Analisa o próximo elemento
            elementos.append(self.expressao())

        return elementos


class Numero:
    def __init__(self, valor):
        self.valor = valor


class Operacao:
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita


class Print:
    def __init__(self, expressao):
        self.expressao = expressao