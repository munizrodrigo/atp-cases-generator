from atp.element.element import Element
from atp.element.switch.timecontrolled import TimeControlled
from atp.node.node import Node

class TimeControlled_3ph(Element):
    """
    Classe responsavel pela adicao de componentes STC Trifasicos entre dois nos eletricos trifasicos.
    """
    def __init__(self, tclose_1, topen_1, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", tclose_2=None, topen_2=None, tclose_3=None, topen_3=None, Ie=0, output_value=None, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.5.1 do Guia Resumido no Atp.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param tclose_1: Instante para fechar a chave da Fase A(Fechado para tclose_1 = -1 )
        :type tclose_1: float
        :param topen_1: Instante o qual antes a chave não poderá abrir
        :type topen_1: float
        :param tclose_2: Instante para fechar a chave da Fase B(Fechado para tclose_2 = -1, por padrão recebe o mesmo valor de tclose_1)
        :type tclose_2: float
        :param topen_2: Instante o qual antes a chave não poderá abrir
        :type topen_2: float
        :param tclose_3: Instante para fechar a chave da Fase C(Fechado para tclose_3 = -1, por padrão recebe o mesmo valor de tclose_1)
        :type tclose_3: float
        :param topen_3: Instante o qual antes a chave não poderá abrir
        :type topen_3: float
        :param Ie: Corrente de margem
        :type Ie: float
        :param output_value: Marcador de Variaveis de Saida do Atp(Verificar valores no topico 5.4.3 do Guia Resumido do Atp)
        :type output_value: int
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """

        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.tclose_1 = tclose_1
        self.topen_1 = topen_1
        self.tclose_2 = tclose_2 if (tclose_2 is not None) else tclose_1
        self.topen_2 = topen_2 if (topen_2 is not None) else topen_1
        self.tclose_3 = tclose_3 if (tclose_3 is not None) else tclose_1
        self.topen_3 = topen_3 if (topen_3 is not None) else topen_1
        self.Ie = Ie
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
                self.switch = "C CHAVE CONTROLADA POR TEMPO TRIFASICA - POS:" + self.bus_pos.name + "\n"
            else:
                self.switch = "C CHAVE CONTROLADA POR TEMPO TRIFASICA - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        self.tca = TimeControlled(bus_pos=self.bus_pos, bus_neg=self.bus_neg, topen= self.topen_1, tclose=self.tclose_1, Ie=self.Ie, output_value=self.output_value, hide_c=True)
        self.tcb = TimeControlled(bus_pos=self.bus_pos, bus_neg=self.bus_neg, topen=self.topen_2, tclose=self.tclose_2, Ie=self.Ie, output_value=self.output_value, hide_c=True)
        self.tcc = TimeControlled(bus_pos=self.bus_pos, bus_neg=self.bus_neg, topen=self.topen_3, tclose=self.tclose_3, Ie=self.Ie, output_value=self.output_value, hide_c=True)

        self.switch += self.tca.switch + "\n" + self.tcb.switch + "\n" + self.tcc.switch

        if not self.hide_c:
            self.switch += "\nC /CHAVE CONTROLADA POR TEMPO TRIFASICA"

