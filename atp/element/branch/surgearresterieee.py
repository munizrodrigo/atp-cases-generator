from atp.element.element import Element
from atp.node.node import Node
from atp.element.branch.rnonlinear92 import RNonLinear92
from atp.element.branch.rlc import RLC


class SurgeArresterIEEE(Element):
    """
    Classe responsavel pela adicao de para-raios do modelo IEEE.
    """
    def __init__(self, bus_pos, currentvoltageA0, currentvoltageA1, phase_pos="A", bus_neg=None, phase_neg="A", d=1, n=1, prnumber=1, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo IEEE de Para-Raio repassado pela equipe de modelagem.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param d: Altura do para-raio
        :type d: float
        :param n: Numero de colunas paralelas do disco de NIO do Para-Raio
        :type n: int ou basestring
        :param prnumber: Numero de identificacao do para raio
        :type prnumber: int
        :param currentvoltageA0: Lista de listas referentes ao Resistor A0
        :type currentvoltageA0: list
        Exemplo:
        >> currentvoltageA0 = [ [0.01, 1.4], [0.1, 1.54], [1, 1.68], [2, 1.74], [4, 1.8], [6, 1.82], [8, 1.87], [10, 1.9], [12, 1.93], [14, 1.97], [16, 2], [18, 2.05], [20, 2.1]]
        :param currentvoltageA1: Lista de listas referentes ao Resistor A1
        :type currentvoltageA1: list
        Exemplo:
        >> currentvoltageA1 = [ [0.1, 1.23], [1, 1.36], [2, 1.43], [4, 1.48], [6, 1.5], [8, 1.53], [10, 1.55], [12, 1.56], [14, 1.58], [16, 1.59], [18, 1.6], [20, 1.61]]
        """

        super().__init__()

        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.d = d
        self.n = n
        self.prnumber = prnumber
        self.hide_c = hide_c

        self.currentvoltageA0 = currentvoltageA0
        self.currentvoltageA1 = currentvoltageA1

        pr_bus_1 = Node("P" + str(self.prnumber) + "1", "Para-Raio", self.phase_pos)
        pr_bus_2 = Node("P" + str(self.prnumber) + "2", "Para-Raio", self.phase_pos)

        self.R0 = 100 * (self.d / self.n)
        self.L0 = 0.2 * (self.d / self.n) * (1e-3)
        self.R1 = 65 * (self.d / self.n)
        self.L1 = 15 * (self.d / self.n) * (1e-3)
        self.C = 100 * (self.n / self.d) * (1e-6)
        self.r0 = RLC(R=self.R0, L=0, C=0, bus_pos=self.bus_pos, phase_pos=self.phase_pos, bus_neg=pr_bus_1, phase_neg=self.phase_pos, hide_c=True)
        self.l0 = RLC(R=0, L=self.L0, C=0, bus_pos=self.bus_pos, phase_pos=self.phase_pos, bus_neg=pr_bus_1, phase_neg=self.phase_pos, hide_c=True)
        self.r1 = RLC(R=self.R1, L=0, C=0, bus_pos=pr_bus_1, phase_pos=self.phase_pos, bus_neg=pr_bus_2, phase_neg=self.phase_pos, hide_c=True)
        self.l1 = RLC(R=0, L=self.L1, C=0, bus_pos=pr_bus_1, phase_pos=self.phase_pos, bus_neg=pr_bus_2, phase_neg=self.phase_pos, hide_c=True)
        self.c = RLC(R=0, L=0, C=self.C, bus_pos=pr_bus_1, phase_pos=self.phase_pos, bus_neg=self.bus_neg, phase_neg=self.phase_neg, hide_c=True)

        self.a0 = RNonLinear92(bus_pos=pr_bus_1, phase_pos=self.phase_pos, bus_neg=self.bus_neg, phase_neg=self.phase_neg, currentvoltage=self.currentvoltageA0, hide_c=True)
        self.a1 = RNonLinear92(bus_pos=pr_bus_2, phase_pos=self.phase_pos, bus_neg=self.bus_neg, phase_neg=self.phase_neg, currentvoltage=self.currentvoltageA1, hide_c=True)

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C PARA-RAIO IEEE - POS: " + self.bus_pos.name + "\n"
            else:
                self.branch = "C PARA-RAIO IEEE - POS: " + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        self.branch += self.r0.branch + "\n"
        self.branch += self.l0.branch + "\n"
        self.branch += self.r1.branch + "\n"
        self.branch += self.l1.branch + "\n"
        self.branch += self.c.branch + "\n"
        self.branch += self.a0.branch + "\n"
        self.branch += self.a1.branch

        if not self.hide_c:
            self.branch += "\nC /PARA-RAIO IEEE"