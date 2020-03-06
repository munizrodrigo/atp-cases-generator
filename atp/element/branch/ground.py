from atp.element.element import Element
from atp.node.node import Node
from atp.element.branch.rlc import RLC
import math


class Ground(Element):
    """
    Classe responsavel pela adicao do modelo de sistema de aterramento para altas frequencias.
    """

    def __init__(self, bus_pos, r, l, ro, phase_pos="A", gndnumber=1, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo de Aterramento repassado pela equipe de modelagem.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param r: Raio do eletrodo
        :type r: float
        :param l: Comprimento do segmento elementar
        :type l: float
        :param ro: Resistividade elétrica
        :type ro: float
        :param gndnumber: Numero de identificacao do aterramento
        :type gndnumber: int
        """

        super().__init__()

        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.gndnumber = gndnumber
        self.hide_c = hide_c
        m0 = 4e-7 * math.pi #Permeabilidade magnética do vácuo
        e0 = 8.854187817e-12 #permissividade eletrica no vacuo
        self.R = ro / (2 * math.pi * l) * (math.log(4 * l / r) - 1)
        self.L = (m0 * l) / (2 * math.pi) * (math.log(4 * l / r) - 1)
        self.C = (2 * math.pi * e0 * l) * (math.log(4 * l / r) - 1)

        gr_bus = Node("G" + str(self.gndnumber), "Terra", self.phase_pos)
        self.r = RLC(R=self.R, L=0, C=0, bus_pos=gr_bus, phase_pos=self.phase_pos, hide_c=True)
        self.c = RLC(R=0, L=0, C=self.C, bus_pos=gr_bus, phase_pos=self.phase_pos, hide_c=True)
        self.l = RLC(R=0, L=self.L, C=0, bus_pos=self.bus_pos, phase_pos=self.phase_pos, bus_neg=gr_bus, phase_neg=self.phase_pos, hide_c=True)

        if not self.hide_c:
            self.branch = "C ATERRAMENTO " + str(self.gndnumber) + " - POS:" + self.bus_pos.name + "\n"

        self.branch += self.r.branch + "\n"
        self.branch += self.c.branch + "\n"
        self.branch += self.l.branch + "\n"

        if not self.hide_c:
            self.branch += "C /ATERRAMENTO " + str(self.gndnumber)