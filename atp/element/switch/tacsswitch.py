from atp.element.element import Element
from atp.formatter.formatter import Formatter
from atp.node.node import Node

class TACSSwitch(Element):
    """
    Classe responsavel pelo chaveamento do circuito controlado por TACS.
    """
    def __init__(self, bus_tacs, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", phase_tacs="A", output_value=0, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado nos cartões gerados pelo ATPDraw.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param bus_tacs: No eletrico de controle.
        :type bus_tacs: float
        :param phase_tacs: Fase na qual sera conectado o no eletrico de controle
        :type phase_tacs: basestring
        :param output_value: Marcador de Variaveis de Saida do Atp(Verificar valores no topico 5.5.2 do Guia Resumido do Atp)
        :type output_value: int
        :param hide_c: Definicao da visibilidade da self.switch inicial e final com comentario (Se True, a self.switch e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.bus_tacs = bus_tacs
        self.phase_tacs = phase_tacs
        self.output_value = output_value
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.switch = "C CHAVE TACS - POS:" + self.bus_pos.name + "\n"
            else:
                self.switch = "C CHAVE TACS - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        self.switch += Formatter.insertInteger(number=13, leng_max=2, start_position=0, final_position=2)

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

        if self.phase_tacs == "A":
            self.switch += Formatter.insertString(string=self.bus_tacs.phaseA, start_position=len(self.switch), final_position=76)
        elif self.phase_tacs == "B":
            self.switch += Formatter.insertString(string=self.bus_tacs.phaseB, start_position=len(self.switch), final_position=76)
        elif self.phase_tacs == "C":
            self.switch += Formatter.insertString(string=self.bus_tacs.phaseC, start_position=len(self.switch), final_position=76)
        elif self.phase_tacs == "N":
            self.switch += Formatter.insertString(string=self.bus_tacs.phaseN, start_position=len(self.switch), final_position=76)

        self.switch += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(self.switch), final_position=80)

        if not self.hide_c:
            self.switch += "\nC /CHAVE TACS"