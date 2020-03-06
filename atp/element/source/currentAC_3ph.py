from atp.element.element import Element
from atp.element.source.currentac import CurrentAC
from atp.node.node import Node


class CurrentAC_3ph(Element):
    """
    Classe responavel pela adicao de Fontes de Corrente AC Trifasicas.
    """
    def __init__(self, bus_pos, amp, freq=60, tstart=-1, tstop=100, bus_neg=None, hide_c=False):
        """
        Construtor da Classe.
        Baseado no modelo encontrado no topico 5.6.4 do Guia Resumido do ATP e generalizado por comparacoes com cartoes gerados pelo ATPDraw.
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param amp: Amplitude da fonte
        :type amp: float
        :param freq: Frequencia da Onda
        :type freq: float
        :param tstart: Tempo de Inicializacao da Fonte
        :type tstart: float
        :param tstop: Tempo de Finalizacao da Fonte
        :type tstop: float
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.bus_pos = bus_pos
        self.bus_neg = bus_neg
        self.amp = amp
        self.freq = freq
        self.tstart = tstart
        self.tstop = tstop
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.source = "C FONTE CORRENTE AC 3PH - POS:" + self.bus_pos.name + "\n"
            else:
                self.source = "C FONTE CORRENTE AC 3PH - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        if self.bus_neg is None:
            self.ia = CurrentAC(bus_pos=self.bus_pos, amp=self.amp, freq=self.freq, phase=0, tstart=self.tstart,
                                tstop=self.tstop, phase_pos="A", hide_c=True)
            self.ib = CurrentAC(bus_pos=self.bus_pos, amp=self.amp, freq=self.freq, phase=-120, tstart=self.tstart,
                                tstop=self.tstop, phase_pos="B", hide_c=True)
            self.ic = CurrentAC(bus_pos=self.bus_pos, amp=self.amp, freq=self.freq, phase=-240, tstart=self.tstart,
                                tstop=self.tstop, phase_pos="C", hide_c=True)
        else:
            self.ia = CurrentAC(bus_pos=self.bus_pos, amp=self.amp, freq=self.freq, phase=0, tstart=self.tstart,
                                tstop=self.tstop, phase_pos="A", bus_neg=self.bus_neg, phase_neg="A", hide_c=True)
            self.ib = CurrentAC(bus_pos=self.bus_pos, amp=self.amp, freq=self.freq, phase=-120, tstart=self.tstart,
                                tstop=self.tstop, phase_pos="B", bus_neg=self.bus_neg, phase_neg="B", hide_c=True)
            self.ic = CurrentAC(bus_pos=self.bus_pos, amp=self.amp, freq=self.freq, phase=-240, tstart=self.tstart,
                                tstop=self.tstop, phase_pos="C", bus_neg=self.bus_neg, phase_neg="C", hide_c=True)

        self.source += self.ia.source + "\n" + self.ib.source + "\n" + self.ic.source

        if not self.hide_c:
            self.source += "\nC /FONTE CORRENTE AC 3PH"