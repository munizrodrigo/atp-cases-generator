from atp.element.element import Element
from atp.element.switch.voltagecontrolled import VoltageControlled
from atp.node.node import Node

class VoltageControlled_3ph(Element):
    """
    Classe responsavel pelo pela adição de componentes VoltageControlled Trifasicos entre dois nós eletricos trifasicos.
    """
    def __init__(self, vflash_1, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", tclose_1=0, tdelay_1= 0.001, vflash_2=None, tclose_2=None, tdelay_2= None, vflash_3=None, tclose_3=None, tdelay_3= None, Ie=0, type=0, output_value=None, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.5.2 do Guia Resumido no Atp.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param hide_c: Definicao da visibilidade da self.switch inicial e final com comentario (Se True, a self.switch e omitida)
        :type hide_c: bool
        :param vflash_1: Tensão que deverá ser excedida para a chave da fase A fechar
        :type vflash_1: float
        :param tclose_1: Instante antes do qual a chave da fase A é proibida de disparar(s)(Aberta por padrão ou tclose = 0)
        :type tclose_1: float
        :param tdelay_1: Instante decorrido depois da disrupção, antes do qual a chave da fase A não poderá abrir
        :type tdelay_1: float
        :param vflash_2: Tensão que deverá ser excedida para a chave da fase B fechar (por pardrão igual a vflash_1)
        :type vflash_2: float
        :param tclose_2: Instante antes do qual a chave da fase B é proibida de disparar (por pardrão igual a tclose_1)
        :type tclose_2: float
        :param tdelay_2: Instante decorrido depois da disrupção, antes do qual a chave da fase B não poderá abrir (por pardrão igual a tdelay_1)
        :type tdelay_2: float
        :param vflash_3: Tensão que deverá ser excedida para a chave da fase C fechar (por pardrão igual a vflash_1)
        :type vflash_3: float
        :param tclose_3: Instante antes do qual a chave da fase C é proibida de disparar (por pardrão igual a tclose_1)
        :type tclose_3: float
        :param tdelay_3: Instante decorrido depois da disrupção, antes do qual a chave da fase C não poderá abrir (por pardrão igual a tdelay_1)
        :type tdelay_3: float
        :param Ie: Corrente de margem
        :type Ie: float
        :param type: Tipo de Elemento Chave (Permanece branco ou type=0 por padrão para esse tipo de chave. Consultar tópico 5.5.2 do Guia Resumido do Atp)
        :type type: int
        :param output_value: Marcador de Variaveis de Saida do Atp(Verificar valores no topico 5.5.2 do Guia Resumido do Atp)
        :type output_value: int
        """
        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.vflash_1 = vflash_1
        self.tclose_1 = tclose_1
        self.tdelay_1 = tdelay_1
        self.vflash_2= vflash_2 if (vflash_2 is not None) else vflash_1
        self.tclose_2= tclose_2 if (tclose_2 is not None) else tclose_1
        self.tdelay_2= tdelay_2 if (tdelay_2 is not None) else tdelay_1
        self.vflash_3 = vflash_3 if (vflash_3 is not None) else vflash_1
        self.tclose_3 = tclose_3 if (tclose_3 is not None) else tclose_1
        self.tdelay_3 = tdelay_3 if (tdelay_3 is not None) else tdelay_1
        self.Ie = Ie
        self.type = type
        self.output_value = output_value
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.switch = "C CHAVE TENSÃO 3PH - POS:" + self.bus_pos.name + "\n"
            else:
                self.switch = "C CHAVE TENSÃO 3PH - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        self.vca = VoltageControlled(bus_pos=self.bus_pos, bus_neg=self.bus_neg, vflash=self.vflash_1, tclose=self.tclose_1, tdelay=self.tdelay_1, Ie=self.Ie, output_value=self.output_value, hide_c=True)
        self.vcb = VoltageControlled(bus_pos=self.bus_pos, bus_neg=self.bus_neg, vflash=self.vflash_2, tclose=self.tclose_2, tdelay=self.tdelay_2, Ie=self.Ie, output_value=self.output_value, hide_c=True)
        self.vcc = VoltageControlled(bus_pos=self.bus_pos, bus_neg=self.bus_neg, vflash=self.vflash_3, tclose=self.tclose_3, tdelay=self.tdelay_3, Ie=self.Ie, output_value=self.output_value, hide_c=True)

        self.switch = self.vca.switch + "\n" + self.vcb.switch + "\n" + self.vcc.switch

        if not self.hide_c:
            self.switch += "\nC /CHAVE TENSÃO 3PH"