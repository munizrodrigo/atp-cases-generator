from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node
import math


class SurgeImpedance(Element):
    """
    Classe responsavel pela adicao de Impedancia de Surto da Torre a parametros concentrados.
    """

    def __init__(self, R, h, r, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A",h1=0, h2=0, r1=0, r2=0, r3=0, form="cilindrica", hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo de Impedancia de Surto da Torre repassado pela equipe de Modelagem.
        :param R: Resistencia em Ohm
        :type R: float
        :param h: Altura da torre
        :type h: float
        :param r: Raio da base da torre
        :type r: float
        :param h1: Altura do primeiro solido
        :type h1: float
        :param h2: Altura do segundo solido
        :type h2: float
        :param r1:Raio do tronco do primeiro solido
        :type r1: float
        :param r2:Raio da base de interseção de solidos
        :type r2: float
        :param r3: Raio da base do segundo solido
        :type r3: float
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
        :param form: Marcador de formato da torre(Cilindrica, Conical ou Combinacao de Solidos, com Cilindrica por padrão)
        :type form: int
        """
        super().__init__()
        self.length = h
        self.Rl = R / h
        self.tau = h / (0.85 * 299792458)  # velocidade da luz
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.hide_c = hide_c

        if form == "cilindrica":
            self.Z = 60 * (math.log(2*math.sqrt(2)*(h/r)) - 1)

        elif form == "conical":
            self.Z = 60 * math.log(math.sqrt(2) * (math.sqrt(r*r + h*h)/r))

        elif form == "combinacaosolidos":
            self.Z = 60 * math.log(math.cos(0.5 * math.atan((r1*h1 + r2*(h1+h2) + r3*h1)/math.pow(h1+h2, 2)))/math.sin(0.5* math.atan((r1*h1 + r2*(h1+h2) + r3*h1)/math.pow(h1+h2, 2))))

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C IMPEDANCIA DE SURTO DA TORRE - POS:" + self.bus_pos.name + "\n"
            else:
                self.branch = "C IMPEDANCIA DE SURTO DA TORRE - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        self.branch = Formatter.insertInteger(number=-1, leng_max=2, start_position=0, final_position=2)

        if self.phase_pos == "A":
            self.branch += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(self.branch), final_position=8)
        elif self.phase_pos == "B":
            self.branch += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(self.branch), final_position=8)
        elif self.phase_pos == "C":
            self.branch += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(self.branch), final_position=8)
        elif self.phase_pos == "N":
            self.branch += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(self.branch), final_position=8)
        if self.bus_neg is not None:
            if self.phase_neg == "A":
                self.branch += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(self.branch), final_position=14)
            elif self.phase_neg == "B":
                self.branch += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(self.branch), final_position=14)
            elif self.phase_neg == "C":
                self.branch += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(self.branch), final_position=14)
            elif self.phase_neg == "N":
                self.branch += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(self.branch), final_position=14)

        self.branch += Formatter.insertFloat(number=self.Rl, leng_max=6, start_position=len(self.branch), final_position=32)
        self.branch += Formatter.insertFloat(number=self.Z, leng_max=6, start_position=len(self.branch), final_position=38)
        self.branch += Formatter.insertFloat(number=self.tau, leng_max=6, start_position=len(self.branch), final_position=44)
        self.branch += Formatter.insertFloat(number=self.length, leng_max=6, start_position=len(self.branch), final_position=50)

        if not self.hide_c:
            self.branch += "\nC /IMPEDANCIA DE SURTO DA TORRE"
