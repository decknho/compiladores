class GeradorMEPA:

    def __init__(self, tabela_simbolos):
        self.tabela = tabela_simbolos
        self.codigo = []

    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    def gerar(self, no):
        """Gera o programa MEPA completo."""

        self.codigo = []

        # Início do programa
        self.emitir("INPP")

        # Gera as instruções da AST
        self.gerar_no(no)

        # Final do programa
        self.emitir("PARA")

        return self.codigo

    def gerar_no(self, no):

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

            self.gerar_no(no.esquerda)
            self.gerar_no(no.direita)

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

            self.gerar_no(no.expressao)
            self.emitir("IMPR")

        # BEGIN
        elif no.__class__.__name__ == "Begin":

            for expressao in no.expressoes:
                self.gerar_no(expressao)
