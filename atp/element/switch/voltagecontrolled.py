from atp.element.element import Element
from atp.formatter.formatter import Formatter
from atp.node.node import Node

class VoltageControlled(Element):
    """
    Classe responsavel pelo chaveamento do circuito controlado por tensão.
    """
    def __init__(self, vflash, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", tclose=0, tdelay= 0.001, Ie=0, type=0, output_value=None, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.5.2 do Guia Resumido no Atp.
        :param vflash: Tensão que deverá ser excedida para a chave fechar.
        :type vflash: float
        :param tclose: Instante antes do qual a chave é proibida de disparar (Aberta por padrão ou tclose = 0 )
        :type tclose: float
        :param tdelay: Instante decorrido depois da disrupção, antes do qual a chave não poderá abrir
        :type tdelay: float
        :param Ie: Corrente de margem
        :type Ie: float
        :param type: Tipo de Elemento Chave (Permanece branco ou type=0 por padrão para esse tipo de chave. Consultar tópico 5.5.2 do Guia Resumido do Atp)
        :type type: int
        :param output_value: Marcador de Variaveis de Saida do Atp(Verificar valores no topico 5.5.2 do Guia Resumido do Atp)
        :type output_value: int
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
        """
        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.vflash = vflash
        self.tclose = tclose
        self.tdelay = tdelay
        self.Ie = Ie
        self.type = type
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
                self.switch = "C CHAVE TENSÃO - POS:" + self.bus_pos.name + "\n"
            else:
                self.switch = "C CHAVE TENSÃO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        self.switch += Formatter.insertInteger(number=self.type, leng_max=2, start_position=0, final_position=2)
        
        if self.phase_pos == "A":
            self.switch += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(self.switch), final_position=8)
        elif self.phase_pos == "B":
            self.switch += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(self.switch), final_position=8)
        elif self.phase_pos == "C":
            self.switch += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(self.switch), final_position=8)
        elif self.phase_pos == "N":
            self.switch += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(self.switch), final_position=8)
        
        if self.bus_neg is not None:
            if self.phase_neg == "A":
                self.switch += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(self.switch), final_position=14)
            elif self.phase_neg == "B":
                self.switch += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(self.switch), final_position=14)
            elif self.phase_neg == "C":
                self.switch += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(self.switch), final_position=14)
            elif self.phase_neg == "N":
                self.switch += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(self.switch), final_position=14)
        
        self.switch += Formatter.insertFloat(number=self.tclose, leng_max=10, start_position=len(self.switch), final_position=24)
        self.switch += Formatter.insertFloat(number=self.tdelay, leng_max=10, start_position=len(self.switch), final_position=34)
        self.switch += Formatter.insertFloat(number=self.Ie, leng_max=10, start_position=len(self.switch), final_position=44)
        self.switch += Formatter.insertFloat(number=self.vflash, leng_max=10, start_position=len(self.switch), final_position=54)
        self.switch += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(self.switch), final_position=80)

        if not self.hide_c:
            self.switch += "\nC /CHAVE TENSÃO"
