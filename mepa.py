class GeradorMEPA:

    def __init__(self, tabela_simbolos):
        self.tabela = tabela_simbolos
        self.codigo = []
        self.rotulo = 1

    def novo_rotulo(self):
        rotulo = f"R{self.rotulo}"
        self.rotulo += 1
        return rotulo

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
                "/": "DIVI",

                ">": "CMMA",
                "<": "CMME",
                ">=": "CMEG",
                "<=": "CMLE",
                "==": "CMIG",
                "!=": "CMDG"
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

        # SET
        elif no.__class__.__name__ == "Set":

            # Gera o valor que será armazenado
            self.gerar_no(no.expressao)

            # Busca a variável na tabela
            simbolo = self.tabela[no.nome]

            # Armazena no endereço MEPA
            self.emitir(
                f"ARMZ {simbolo.endereco}"
            )

        # IF
        elif no.__class__.__name__ == "If":

            rotulo_else = self.novo_rotulo()
            rotulo_fim = self.novo_rotulo()

            # Gera a condição
            self.gerar_no(no.condicao)

            # Se falso, vai para ELSE
            self.emitir(
                f"DSVF {rotulo_else}"
            )

            # THEN
            self.gerar_no(no.entao)

            # Depois do THEN, pula o ELSE
            self.emitir(
                f"DSVS {rotulo_fim}"
            )

            # ELSE
            self.emitir(
                f"{rotulo_else}: NADA"
            )

            self.gerar_no(no.senao)

            # Fim do IF
            self.emitir(
                f"{rotulo_fim}: NADA"
            )

        # WHILE
        elif no.__class__.__name__ == "While":

            rotulo_inicio = self.novo_rotulo()
            rotulo_fim = self.novo_rotulo()

            # Início do loop
            self.emitir(
                f"{rotulo_inicio}: NADA"
            )

            # Condição
            self.gerar_no(no.condicao)

            # Se falso, sai do loop
            self.emitir(
                f"DSVF {rotulo_fim}"
            )

            # Corpo
            self.gerar_no(no.corpo)

            # Volta para o início
            self.emitir(
                f"DSVS {rotulo_inicio}"
            )

            # Fim
            self.emitir(
                f"{rotulo_fim}: NADA"
            )