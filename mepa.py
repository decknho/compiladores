class GeradorMEPA:

    def __init__(self, tabela_simbolos):
        self.tabela = tabela_simbolos
        self.codigo = []

    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    def gerar(self, no):
        """Gera código MEPA a partir da AST."""

        # NÚMERO
        if no.__class__.__name__ == "Numero":
            self.emitir(f"CRCT {no.valor}")

        # VARIÁVEL
        elif no.__class__.__name__ == "Variavel":

            simbolo = self.tabela[no.nome]

            self.emitir(
                f"CRVL {simbolo.endereco}"
            )

        # OPERAÇÃO
        elif no.__class__.__name__ == "Operacao":

            # Primeiro gera a expressão da esquerda
            self.gerar(no.esquerda)

            # Depois gera a expressão da direita
            self.gerar(no.direita)

            operadores = {
                "+": "SOMA",
                "-": "SUBT",
                "*": "MULT",
                "/": "DIVI"
            }

            instrucao = operadores.get(no.operador)

            if instrucao is None:
                raise Exception(
                    f"Operador '{no.operador}' "
                    "ainda não possui código MEPA."
                )

            self.emitir(instrucao)

        # PRINT
        elif no.__class__.__name__ == "Print":

            self.gerar(no.expressao)

            self.emitir("IMPR")

        # BEGIN
        elif no.__class__.__name__ == "Begin":

            for expressao in no.expressoes:
                self.gerar(expressao)

        return self.codigo