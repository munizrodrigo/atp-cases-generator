from atp.element.element import Element
from atp.element.branch.rlc import RLC
from atp.node.node import Node


class RLC_3ph(Element):
    """
    Classe responsavel pela adicao de componentes RLC Trifasicos entre dois nos eletricos trifasicos, ramos lineares e linhas de transmissão simples.
    """
    def __init__(self, R1, L1, C1, bus_pos, phase_pos="A", R2=None, L2=None, C2=None, R3=None, L3=None, C3=None, bus_neg=None,
                 phase_neg="A", bus_ref_pos=None, bus_ref_neg=None, output_value=0, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado na comparacao com cartoes gerados pelo ATPDraw.
        :param R1: Resistencia da fase A em Ohm
        :type R1: float
        :param L1: Indutancia da fase A em mH se xopt = 0 ou Reatancia da fase A em Ohm na frequencia xopt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre xopt)
        :type L1: float
        :param C1: Capacitancia da fase A em uF se copt = 0 ou Susceptancia da fase A em uS na frequencia copt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre copt)
        :type C1: float
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param R2: Resistencia da fase B em Ohm (por padrao recebem o valor de R1, para se obter um sistema equilibrado)
        :type R2: float
        :param L2: Indutancia da fase B em mH se xopt = 0 ou Reatancia da fase B em Ohm na frequencia xopt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre xopt) (por padrao recebem o valor de L1, para se obter um sistema equilibrado)
        :type L2: float
        :param C2: Capacitancia da fase B em uF se copt = 0 ou Susceptancia da fase B em uS na frequencia copt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre copt) (por padrao recebem o valor de C1, para se obter um sistema equilibrado)
        :type C2: float
        :param R3: Resistencia da fase C em Ohm (por padrao recebem o valor de R1, para se obter um sistema equilibrado)
        :type R3: float
        :param L3: Indutancia da fase C em mH se xopt = 0 ou Reatancia da fase C em Ohm na frequencia xopt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre xopt) (por padrao recebem o valor de L1, para se obter um sistema equilibrado)
        :type L3: float
        :param C3: Capacitancia da fase C em uF se copt = 0 ou Susceptancia da fase C em uS na frequencia copt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre copt) (por padrao recebem o valor de C1, para se obter um sistema equilibrado)
        :type C3: float
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param bus_ref_pos: No eletrico de referencia na extremidade positiva do elemento
        :type bus_ref_pos: Node
        :param bus_ref_neg: No eletrico de referencia na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_ref_neg: Node
        :param output_value: Marcador de Variaveis de Saida do Atp (Verificar valores no topico 5.4.3 do Guia Resumido do Atp)
        :type output_value: int
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.R1 = R1
        self.L1 = L1
        self.C1 = C1
        self.R2 = R2 if (R2 is not None) else R1
        self.L2 = L2 if (L2 is not None) else L1
        self.C2 = C2 if (C2 is not None) else C1
        self.R3 = R3 if (R3 is not None) else R1
        self.L3 = L3 if (L3 is not None) else L1
        self.C3 = C3 if (C3 is not None) else C1
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.bus_ref_pos = bus_ref_pos
        self.bus_ref_neg = bus_ref_neg
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
                self.branch = "C RLC TRIFASICO - POS:" + self.bus_pos.name + "\n"
            else:
                if self.bus_ref_pos is None:
                    self.branch = "C RLC TRIFASICO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"
                else:
                    if self.bus_ref_neg is None:
                        self.branch = "C RLC TRIFASICO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos.name + "\n"
                    else:
                        self.branch = "C RLC TRIFASICO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos.name + " - REF_NEG: " + self.bus_ref_neg.name + "\n"

        self.rlca = RLC(R=self.R1, L=self.L1, C=self.C1, bus_pos=self.bus_pos, phase_pos="A", bus_neg=self.bus_neg, phase_neg="A", bus_ref_pos=self.bus_ref_pos, bus_ref_neg= self.bus_ref_neg, output_value=self.output_value)
        self.rlcb = RLC(R=self.R2, L=self.L2, C=self.C2, bus_pos=self.bus_pos, phase_pos="B", bus_neg=self.bus_neg, phase_neg="B", bus_ref_pos=self.bus_ref_pos, bus_ref_neg= self.bus_ref_neg, output_value=self.output_value)
        self.rlcc = RLC(R=self.R3, L=self.L3, C=self.C3, bus_pos=self.bus_pos, phase_pos="C", bus_neg=self.bus_neg, phase_neg="C", bus_ref_pos=self.bus_ref_pos, bus_ref_neg= self.bus_ref_neg, output_value=self.output_value)

        self.branch = self.rlca.branch + "\n" + self.rlcb.branch + "\n" + self.rlcc.branch

        if not self.hide_c:
            self.branch += "\nC /RLC TRIFASICO"
