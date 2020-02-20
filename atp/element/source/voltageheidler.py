from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node


class VoltageHEIDLER(Element):
    """
    Classe responavel pela adicao de Fontes de Tensao HEIDLER.
    """
    def __init__(self, bus_pos, amp, tfront=1.2e-6, tau=5e-5, n=2, tstart=-1, tstop=100, phase_pos="A",
                 hide_c=False):
        """
        Construtor da Classe.
        Baseado no modelo encontrado no topico 5 do ATP Rulebook.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param amp: Amplitude da fonte
        :type amp: float
        :param tfront: Tempo de Frente
        :type tfront: float
        :param tau: Equivalente ao Tempo de Cauda
        :type tau: float
        :param n: Fator de Subida
        :type n: float
        :param tstart: Tempo de Inicializacao da Fonte
        :type tstart: float
        :param tstop: Tempo de Finalizacao da Fonte
        :type tstop: float
        :param phase_pos: Fase na qual sera conectado o terminal positivo da fonte
        :type phase_pos: basestring
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.amp = amp
        self.tfront = tfront
        self.tau = tau
        self.n = n
        self.tstart = tstart
        self.tstop = tstop
        self.hide_c = hide_c

        if not self.hide_c:
            self.source = "C FONTE DE TENSAO HEIDLER - POS:" + self.bus_pos.name + "\n"

        linha = Formatter.insertInteger(number=15, leng_max=2, start_position=0, final_position=2) # Variavel ITYPE
        # do Guia Resumido do ATP e do Arquivo rb-070-lec do ATP Rulebook

        if self.phase_pos == "A":
            linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
        elif self.phase_pos == "B":
            linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
        elif self.phase_pos == "C":
            linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
        elif self.phase_pos == "N":
            linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

        linha += Formatter.insertInteger(number=0, leng_max=2, start_position=len(linha), final_position=10)
        # Variavel ST do Guia Resumido do ATP

        linha += Formatter.insertFloat(number=self.amp, leng_max=10, start_position=len(linha), final_position=20)

        linha += Formatter.insertFloat(number=self.tfront, leng_max=10, start_position=len(linha), final_position=30)

        linha += Formatter.insertFloat(number=self.tau, leng_max=10, start_position=len(linha), final_position=40)

        linha += Formatter.insertFloat(number=self.n, leng_max=10, start_position=len(linha), final_position=50)

        linha += Formatter.insertFloat(number=self.tstart, leng_max=10, start_position=len(linha), final_position=70)

        linha += Formatter.insertFloat(number=self.tstop, leng_max=10, start_position=len(linha), final_position=80)

        self.source += linha

        if not self.hide_c:
            self.source += "\nC /FONTE DE TENSAO HEIDLER"