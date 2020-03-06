from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node


class CurrentCIGRE(Element):
    """
    Classe responavel pela adicao de Fontes de Corrente CIGRE.
    """
    def __init__(self, bus_pos, amp, tfront=3e-6, ttail=7.5e-5, smax=26e9, risefactor=-8888, tstart=-1, tstop=100,
                 phase_pos="A", hide_c=False):
        """
        Construtor da Classe.
        Baseado no modelo encontrado no topico 5 do ATP Rulebook.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param amp: Amplitude da fonte
        :type amp: float
        :param tfront: Tempo de Frente
        :type tfront: float
        :param ttail: Tempo de Cauda
        :type ttail: float
        :param smax: Potencia Maxima
        :type smax: float
        :param risefactor: Fator de Subida (Padrao Cigre = -8888)
        :type risefactor: float
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
        self.ttail = ttail
        self.smax = smax
        self.risefactor = risefactor
        self.tstart = tstart
        self.tstop = tstop
        self.hide_c = hide_c

        if not self.hide_c:
            self.source = "C FONTE DE CORRENTE CIGRE - POS:" + self.bus_pos.name + "\n"

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

        linha += Formatter.insertInteger(number=-1, leng_max=2, start_position=len(linha), final_position=10)
        # Variavel ST do Guia Resumido do ATP

        linha += Formatter.insertFloat(number=self.amp, leng_max=10, start_position=len(linha), final_position=20)

        linha += Formatter.insertFloat(number=self.tfront, leng_max=10, start_position=len(linha), final_position=30)

        linha += Formatter.insertFloat(number=self.ttail, leng_max=10, start_position=len(linha), final_position=40)

        linha += Formatter.insertFloat(number=self.risefactor, leng_max=10, start_position=len(linha), final_position=50)

        linha += Formatter.insertFloat(number=self.smax, leng_max=10, start_position=len(linha), final_position=60)

        linha += Formatter.insertFloat(number=self.tstart, leng_max=10, start_position=len(linha), final_position=70)

        linha += Formatter.insertFloat(number=self.tstop, leng_max=10, start_position=len(linha), final_position=80)

        self.source += linha

        if not self.hide_c:
            self.source += "\nC /FONTE DE CORRENTE CIGRE"