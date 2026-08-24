class Numero:
    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Numero({self.valor})"


class Variavel:
    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"Variavel('{self.nome}')"


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


class Set:
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

    def __repr__(self):
        return f"Set('{self.nome}', {self.expressao})"


class Begin:
    def __init__(self, expressoes):
        self.expressoes = expressoes

    def __repr__(self):
        return f"Begin({self.expressoes})"


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
        """Consome o token atual e avança."""
        token = self.atual()

        if token is not None:
            self.posicao += 1

        return token

    def erro(self, mensagem):
        """Gera uma mensagem de erro sintático."""
        token = self.atual()

        if token:
            raise Exception(
                f"Erro Sintático na linha "
                f"{token['linha']}: {mensagem}"
            )

        raise Exception(
            f"Erro Sintático: {mensagem}"
        )

    def analisar(self):
        """Inicia a análise sintática."""
        arvore = self.expressao()

        if self.atual() is not None:
            self.erro(
                f"Token inesperado "
                f"'{self.atual()['lexema']}'."
            )

        return arvore

    def expressao(self):
        """Analisa uma expressão."""

        token = self.atual()

        if token is None:
            self.erro(
                "Expressão inesperadamente vazia."
            )

        # Número inteiro
        if token["token"] == "INTEGER":
            self.consumir()
            return Numero(int(token["lexema"]))

        # Número decimal
        if token["token"] == "FLOAT":
            self.consumir()
            return Numero(float(token["lexema"]))

        # Variável
        if token["token"] == "ID":
            self.consumir()
            return Variavel(token["lexema"])

        # Lista entre parênteses
        if token["token"] == "LPAR":
            return self.lista()

        self.erro(
            f"Token '{token['lexema']}' "
            f"não pode iniciar uma expressão."
        )

    def lista(self):
        """Analisa uma estrutura entre parênteses."""

        # Consome '('
        self.consumir()

        token = self.atual()

        if token is None:
            self.erro(
                "Fim de arquivo inesperado. "
                "Esperava-se ')'."
            )

        # PRINT

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
                    "Esperava-se ')' após "
                    "o argumento de print."
                )

            self.consumir()

            return Print(expressao)

        # SET
        if token["token"] == "SET":
            self.consumir()

            identificador = self.atual()

            if identificador is None:
                self.erro(
                    "Esperava-se um identificador "
                    "após 'set'."
                )

            if identificador["token"] != "ID":
                self.erro(
                    "Esperava-se um identificador "
                    "após 'set'."
                )

            nome = identificador["lexema"]

            self.consumir()

            expressao = self.expressao()

            if self.atual() is None:
                self.erro(
                    "Fim de arquivo inesperado. "
                    "Esperava-se ')'."
                )

            if self.atual()["token"] != "RPAR":
                self.erro(
                    "Esperava-se ')' após "
                    "a atribuição."
                )

            self.consumir()

            return Set(nome, expressao)

        # BEGIN
        if token["token"] == "BEGIN":
            self.consumir()

            expressoes = []

            while self.atual() is not None:

                if self.atual()["token"] == "RPAR":
                    self.consumir()

                    return Begin(expressoes)

                expressoes.append(
                    self.expressao()
                )

            self.erro(
                "Fim de arquivo inesperado. "
                "Esperava-se ')'."
            )

        # OPERAÇÕES
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
                    "Operação deve possuir "
                    "exatamente dois operandos."
                )

            self.consumir()

            return Operacao(
                operador,
                esquerda,
                direita
            )

        # CONSTRUÇÃO NÃO RECONHECIDA
        self.erro(
            f"Construção '{token['lexema']}' "
            "ainda não é suportada pelo Parser."
        )