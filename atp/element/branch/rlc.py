from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node


class RLC(Element):
    """
    Classe responsavel pela adicao de componentes RLC, ramos lineares e linhas de transmissão simples.
    """
    def __init__(self, R, L, C, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", bus_ref_pos=None, phase_ref_pos="A",
                 bus_ref_neg=None, phase_ref_neg="A", type=0, output_value=None, vintage=0, printvintage="cabecalhorodape", hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.4.3 do Guia Resumido do Atp.
        :param R: Resistencia em Ohm
        :type R: float
        :param L: Indutancia em mH se xopt = 0 ou Reatancia em Ohm na frequencia xopt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre xopt)
        :type L: float
        :param C: Capacitancia em uF se copt = 0 ou Susceptancia em uS na frequencia copt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre copt)
        :type C: float
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param bus_ref_pos: No eletrico de referencia na extremidade positiva do elemento
        :type bus_ref_pos: Node
        :param phase_ref_pos: Fase na qual sera conectado o terminal positivo de referencia do elemento
        :type phase_ref_pos: basestring
        :param bus_ref_neg: No eletrico de referencia na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_ref_neg: Node
        :param phase_ref_neg: Fase na qual sera conectado o terminal negativo de referencia do elemento
        :type phase_ref_neg: basestring
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        :param type: Tipo do Elemento RLC (Nao acoplado por padrao, com type = 0. Consultar topico 5.4 do Guia Resumido do Atp)
        :type type: int
        :param output_value: Marcador de Variaveis de Saida do Atp (Verificar valores no topico 5.4.3 do Guia Resumido do Atp)
        :type output_value: basestring
        :param vintage: Precisao do Cartao (Consultar topico 5.4.1 do Guia Resumido do Atp)
        :type vintage: int
        :param printvintage: Marcador de formato de saída da string "$VINTAGE"
        :type printvintage: basestring
        """
        super().__init__()
        self.R = R
        self.L = L
        self.C = C
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.bus_ref_pos = bus_ref_pos
        self.phase_ref_pos = phase_ref_pos
        self.bus_ref_neg = bus_ref_neg
        self.phase_ref_neg = phase_ref_neg
        self.type = type
        self.vintage = vintage
        self.printvintage = printvintage
        if output_value is None:
            self.output_value = 0
        if output_value == "I":
            self.output_value = 1
        if output_value == "V":
            self.output_value = 2
        if output_value == "IV":
            self.output_value = 3
        if output_value == "PE":
            self.output_value = 4
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C RLC MONOFASICO - POS:" + self.bus_pos.name + "\n"
            else:
                self.branch = "C RLC MONOFASICO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        if vintage == 1: # Modo de Alta Precisao
            if printvintage == "cabecalhorodape" or "cabecalho":
                self.branch += "$VINTAGE,1" + "\n"

            linha = Formatter.insertInteger(number=self.type, leng_max=2, start_position=0, final_position=2)

            if self.phase_pos == "A":
                linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
            elif self.phase_pos == "B":
                linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
            elif self.phase_pos == "C":
                linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
            elif self.phase_pos == "N":
                linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

            if self.bus_neg is not None:
                if self.phase_neg == "A":
                    linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
                elif self.phase_neg == "B":
                    linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
                elif self.phase_neg == "C":
                    linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
                elif self.phase_neg == "N":
                    linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=14)

            if self.bus_ref_pos is not None:
                if self.phase_ref_pos == "A":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseA, start_position=len(linha), final_position=20)
                elif self.phase_ref_pos == "B":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseB, start_position=len(linha), final_position=20)
                elif self.phase_ref_pos == "C":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseC, start_position=len(linha), final_position=20)
                elif self.phase_ref_pos == "N":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseN, start_position=len(linha), final_position=20)

            if self.bus_ref_neg is not None:
                if self.phase_ref_neg == "A":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseA, start_position=len(linha), final_position=26)
                elif self.phase_ref_neg == "B":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseB, start_position=len(linha), final_position=26)
                elif self.phase_ref_neg == "C":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseC, start_position=len(linha), final_position=26)
                elif self.phase_ref_neg == "N":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseN, start_position=len(linha), final_position=26)

            linha += Formatter.insertFloat(number=self.R, leng_max=16, start_position=len(linha), final_position=42)
            linha += Formatter.insertFloat(number=self.L, leng_max=16, start_position=len(linha), final_position=58)
            linha += Formatter.insertFloat(number=self.C, leng_max=16, start_position=len(linha), final_position=74)
            linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)

            self.branch += linha
            if printvintage == "cabecalhorodape" or "rodape":
                self.branch += "\n" + "$VINTAGE,0"

            if not self.hide_c:
                self.branch += "\nC /RLC MONOFASICO"

        else: # Modo de Precisao Padrao
            linha = Formatter.insertInteger(number=self.type, leng_max=2, start_position=0, final_position=2)

            if self.phase_pos == "A":
                linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
            elif self.phase_pos == "B":
                linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
            elif self.phase_pos == "C":
                linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
            elif self.phase_pos == "N":
                linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

            if self.bus_neg is not None:
                if self.phase_neg == "A":
                    linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
                elif self.phase_neg == "B":
                    linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
                elif self.phase_neg == "C":
                    linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
                elif self.phase_neg == "N":
                    linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=14)

            if self.bus_ref_pos is not None:
                if self.phase_ref_pos == "A":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseA, start_position=len(linha), final_position=20)
                elif self.phase_ref_pos == "B":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseB, start_position=len(linha), final_position=20)
                elif self.phase_ref_pos == "C":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseC, start_position=len(linha), final_position=20)
                elif self.phase_ref_pos == "N":
                    linha += Formatter.insertString(string=self.bus_ref_pos.phaseN, start_position=len(linha), final_position=20)

            if self.bus_ref_neg is not None:
                if self.phase_ref_neg == "A":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseA, start_position=len(linha), final_position=26)
                elif self.phase_ref_neg == "B":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseB, start_position=len(linha), final_position=26)
                elif self.phase_ref_neg == "C":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseC, start_position=len(linha), final_position=26)
                elif self.phase_ref_neg == "N":
                    linha += Formatter.insertString(string=self.bus_ref_neg.phaseN, start_position=len(linha), final_position=26)

            linha += Formatter.insertFloat(number=self.R, leng_max=6, start_position=len(linha), final_position=32)
            linha += Formatter.insertFloat(number=self.L, leng_max=6, start_position=len(linha), final_position=38)
            linha += Formatter.insertFloat(number=self.C, leng_max=6, start_position=len(linha), final_position=44)
            linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)

            self.branch += linha

            if not self.hide_c:
                self.branch += "\nC /RLC MONOFASICO"