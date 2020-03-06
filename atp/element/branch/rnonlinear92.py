from atp.formatter.formatter import Formatter
from atp.element.element import Element


class RNonLinear92(Element):
    """
    Classe responsavel pela adicao do resistor não linear do tipo 92.
    """
    def __init__(self, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", bus_ref_pos=None, phase_ref_pos="A", bus_ref_neg=None,
                 phase_ref_neg="A", nflash=0, rlin=0, vflash=-1, vzero=0, currentvoltage=[], output_value=None, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no arquivo RB-05a do Atp RuleBook.
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
        :param nflash: Flashover Gap (Ver arquivo RB-05a do Atp RuleBook)
        :type nflash: int
        :param rlin: Resistência Linear associada em serie
        :type rlin: float
        :param vflash: Tensao de Flashover (-1 se não houver)
        :type vflash: float
        :param vzero: Tensao Inicial
        :type vzero: float
        :param currentvoltage: Lista de pares [corrente, tensao] para a curva de nao linearidade
        :type currentvoltage: list
        :param output_value: Marcador de Variaveis de Saida do Atp (Verificar valores em)
        :type output_value: int
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()

        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.bus_ref_pos = bus_ref_pos
        self.phase_ref_pos = phase_ref_pos
        self.bus_ref_neg = bus_ref_neg
        self.phase_ref_neg = phase_ref_neg
        self.nflash = nflash
        self.rlin = rlin
        self.vflash = vflash
        self.vzero = vzero
        self.currentvoltage = currentvoltage
        if output_value is None:
            self.output_value = 0
        if output_value == "V":
            self.output_value = 1
        if output_value == "I":
            self.output_value = 2
        if output_value == "VI":
            self.output_value = 3
        if output_value == "PE":
            self.output_value = 4
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C RESISTOR NAO-LINEAR TIPO 92 - POS:" + self.bus_pos.name + "\n"
            else:
                if self.bus_ref_pos is None:
                    self.branch = "C RESISTOR NAO-LINEAR TIPO 92 - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"
                else:
                    if self.bus_ref_neg is None:
                        self.branch = "C RESISTOR NAO-LINEAR TIPO 92 - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos + "\n"
                    else:
                        self.branch = "C RESISTOR NAO-LINEAR TIPO 92 - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos + " - REF_NEG: " + self.phase_ref_neg + "\n"

        linha = Formatter.insertInteger(number=92, leng_max=2, start_position=0, final_position=2)

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

        linha += Formatter.insertFloat(number=self.nflash, leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertString(string="4444.", start_position=len(linha), final_position=44)
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertFloat(number=self.rlin, leng_max=25, start_position=0, final_position=25)
        linha += Formatter.insertFloat(number=self.vflash, leng_max=25, start_position=len(linha), final_position=50)
        linha += Formatter.insertFloat(number=self.vzero, leng_max=25, start_position=len(linha), final_position=75)
        self.branch += linha + "\n"

        for pair in self.currentvoltage:
            linha = Formatter.insertFloat(number=pair[0], leng_max=25, start_position=0, final_position=25)
            linha += Formatter.insertFloat(number=pair[1], leng_max=25, start_position=len(linha), final_position=50)
            self.branch += linha + "\n"

        self.branch += Formatter.insertString(string="9999", start_position=0, final_position=16)

        if not self.hide_c:
            self.branch += "\nC /RESISTOR NAO-LINEAR TIPO 92"