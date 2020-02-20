from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node


class VoltageAC(Element):
    """
    Classe responavel pela adicao de Fontes de Tensao AC.
    """
    def __init__(self, bus_pos, amp, freq=60, phase=0, phase_type=True, tstart=-1, tstop=100, phase_pos="A",
                 bus_neg=None, phase_neg="A", hide_c=False):
        """
        Construtor da Classe.
        Baseado no modelo encontrado no topico 5.6.4 do Guia Resumido do ATP.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param amp: Amplitude da fonte
        :type amp: float
        :param freq: Frequencia da Onda
        :type freq: float
        :param phase: Fase da Onda (em graus ou segundos dependendo do valor de phase_type)
        :type phase: float
        :param phase_type: Tipo do dado de Fase (se phase_type = True a fase e dada em graus, se phase_type = False a
        fase e dada em segundos)
        :type phase_type: bool
        :param tstart: Tempo de Inicializacao da Fonte
        :type tstart: float
        :param tstop: Tempo de Finalizacao da Fonte
        :type tstop: float
        :param phase_pos: Fase na qual sera conectado o terminal positivo da fonte
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo da fonte
        :type phase_neg: basestring
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.amp = amp
        self.freq = freq
        self.phase = phase
        self.phase_type = phase_type
        self.tstart = tstart
        self.tstop = tstop
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.source = "C FONTE TENSAO AC - POS:" + self.bus_pos.name + "\n"
            else:
                self.source = "C FONTE TENSAO AC - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        linha = Formatter.insertInteger(number=14, leng_max=2, start_position=0, final_position=2) # Variavel ITYPE no topico 5.6.4 do Guia Resumido do ATP

        if self.phase_pos == "A":
            linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
        elif self.phase_pos == "B":
            linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
        elif self.phase_pos == "C":
            linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
        elif self.phase_pos == "N":
            linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

        linha += Formatter.insertInteger(number=0, leng_max=2, start_position=len(linha), final_position=10)
        # Variavel ST no topico 5.6.4 do Guia Resumido do ATP

        linha += Formatter.insertFloat(number=self.amp, leng_max=10, start_position=len(linha), final_position=20)

        linha += Formatter.insertFloat(number=self.freq, leng_max=10, start_position=len(linha), final_position=30)

        linha += Formatter.insertFloat(number=self.phase, leng_max=10, start_position=len(linha), final_position=40)

        if self.phase_type: # Variavel A1 do topico 5.6.4 do Guia Resumido do ATP
            linha += Formatter.insertFloat(number=0, leng_max=10, start_position=len(linha), final_position=50)
        else:
            linha += Formatter.insertFloat(number=1, leng_max=10, start_position=len(linha), final_position=50)

        linha += Formatter.insertFloat(number=self.tstart, leng_max=10, start_position=len(linha), final_position=70)

        linha += Formatter.insertFloat(number=self.tstop, leng_max=10, start_position=len(linha), final_position=80)

        self.source += linha

        if self.bus_neg is not None:
            linha = Formatter.insertInteger(number=18, leng_max=2, start_position=0, final_position=2)

            if self.phase_neg == "A":
                linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=8)
            elif self.phase_neg == "B":
                linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=8)
            elif self.phase_neg == "C":
                linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=8)
            elif self.phase_neg == "N":
                linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=8)

            linha += Formatter.insertInteger(number=0, leng_max=2, start_position=len(linha), final_position=10)

            linha += Formatter.insertFloat(number=1, leng_max=10, start_position=len(linha), final_position=20)

            self.source += "\n" + linha

        if not self.hide_c:
            self.source += "\nC /FONTE TENSAO AC"