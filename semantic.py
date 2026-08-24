class Simbolo:
    def __init__(self, nome, endereco, tipo, escopo):
        self.nome = nome
        self.endereco = endereco
        self.tipo = tipo
        self.escopo = escopo

    def __repr__(self):
        return (
            f"Simbolo(nome='{self.nome}', "
            f"endereco={self.endereco}, "
            f"tipo='{self.tipo}', "
            f"escopo='{self.escopo}')"
        )


class AnalisadorSemantico:
    def __init__(self):
        self.tabela = {}
        self.proximo_endereco = 0

    def analisar(self, arvore):
        self.visitar(arvore)

        return self.tabela

    def visitar(self, no):

        # BEGIN
        if no.__class__.__name__ == "Begin":

            for expressao in no.expressoes:
                self.visitar(expressao)

        # SET
        elif no.__class__.__name__ == "Set":

            # Primeiro analisa o valor
            # que será atribuído.
            self.visitar(no.expressao)

            # Se a variável ainda não existe,
            # cria um novo símbolo.
            if no.nome not in self.tabela:

                simbolo = Simbolo(
                    nome=no.nome,
                    endereco=self.proximo_endereco,
                    tipo=self.obter_tipo(no.expressao),
                    escopo="Global"
                )

                self.tabela[no.nome] = simbolo

                self.proximo_endereco += 1

            else:
                # Se já existe, apenas atualiza
                # o tipo presumido.
                self.tabela[no.nome].tipo = (
                    self.obter_tipo(no.expressao)
                )

        # VARIÁVEL
        elif no.__class__.__name__ == "Variavel":

            if no.nome not in self.tabela:
                raise Exception(
                    f"Erro Semântico: Variável "
                    f"'{no.nome}' não foi inicializada."
                )

        # NÚMERO
        elif no.__class__.__name__ == "Numero":

            pass

        # PRINT
        elif no.__class__.__name__ == "Print":

            self.visitar(no.expressao)

        # OPERAÇÃO
        elif no.__class__.__name__ == "Operacao":

            self.visitar(no.esquerda)
            self.visitar(no.direita)

        # IF
        elif no.__class__.__name__ == "If":

            self.visitar(no.condicao)
            self.visitar(no.entao)
            self.visitar(no.senao)

        # WHILE
        elif no.__class__.__name__ == "While":

            self.visitar(no.condicao)
            self.visitar(no.corpo)

    def obter_tipo(self, no):

        if no.__class__.__name__ == "Numero":

            if isinstance(no.valor, int):
                return "Inteiro"

            return "Float"

        if no.__class__.__name__ == "Variavel":

            if no.nome in self.tabela:
                return self.tabela[no.nome].tipo

        if no.__class__.__name__ == "Operacao":

            tipo_esquerda = self.obter_tipo(no.esquerda)
            tipo_direita = self.obter_tipo(no.direita)

            if tipo_esquerda == "Float" or tipo_direita == "Float":
                return "Float"

            return "Inteiro"

        return "Desconhecido"