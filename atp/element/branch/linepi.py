from atp.element.element import Element
from atp.formatter.formatter import Formatter

class LinePi(Element):
    """
    Classe responsavel pela adicao de linhas de transmissao usando o modelo pi a parametros concentrados.
    """
    def __init__(self, R, L, C, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.4.4 do Guia Resumido do Atp.
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
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.R = R
        self.L = L
        self.C = C
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C LINE PI - POS:" + self.bus_pos.name + "\n"
            else:
                self.branch = "C LINE PI - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        linha = Formatter.insertInteger(number=1, leng_max=2, start_position=0, final_position=2)

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

        linha += Formatter.insertFloat(number=self.R, leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=self.L, leng_max=6, start_position=len(linha), final_position=38)
        linha += Formatter.insertFloat(number=self.C, leng_max=6, start_position=len(linha), final_position=44)

        self.branch += linha

        if not self.hide_c:
            self.branch += "\nC /LINE PI"

