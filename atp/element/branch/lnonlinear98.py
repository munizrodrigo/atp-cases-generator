from atp.element.element import Element
from atp.formatter.formatter import Formatter

class LNonLinear98(Element):
    """
    Classe responsavel pela adicao do indutor nao linear tipo 98 modificado.
    """
    def __init__(self, flux, curr, zeroseq, rdamp, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", currentflux=[], hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no arquivo RB-05a V.B. do Atp RuleBook com acrescimo de indutancia zero e
         resistencia de amortecimento obtidos pelos cartoes de nucleo do transformador hibrido.
        :param flux: fluxo
        :type flux: float
        :param curr: Corrente
        :type curr: float
        :param zeroseq: Indutância de sequencia zero
        :type zeroseq: float
        :param rdamp: Resistencia de amortecimento
        :type rdamp: float
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param currentflux: Lista de pares [corrente, fluxo] para a curva de saturacao
        :type currentflux: list
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """

        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.flux = flux
        self.curr = curr
        self.zeroseq = zeroseq
        self.rdamp = rdamp
        self.currentflux = currentflux
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C INDUTOR NAO-LINEAR TIPO 98 - POS:" + self.bus_pos.name + "\n"
            else:
                self.branch = "C INDUTOR NAO-LINEAR TIPO 98 - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        if self.flux != 0 and self.curr != 0:
            if not self.currentflux:
                linha = Formatter.insertInteger(number=0, leng_max=2, start_position=0, final_position=2) #verificar se e necessario
            else:
                linha = Formatter.insertInteger(number=98, leng_max=2, start_position=0, final_position=2)

            if self.phase_pos == "A":
                linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
            elif self.phase_pos == "B":
                linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
            elif self.phase_pos == "C":
                linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
            elif self.phase_pos == "N":
                linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

            if self.bus_neg is not None:
                if self.phase_neg == "A":
                    linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
                elif self.phase_neg == "B":
                    linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
                elif self.phase_neg == "C":
                    linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
                elif self.phase_neg == "N":
                    linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=14)
            linha += Formatter.insertFloat(number=self.flux, leng_max=6, start_position=len(linha), final_position=38)
            self.branch += linha + "\n"

            if self.currentflux:
                for pair in self.currentflux:
                    linha = Formatter.insertInteger(number=0, leng_max=2, start_position=0, final_position=2)
                    linha += Formatter.insertFloat(number=pair[0], leng_max=16, start_position=len(linha), final_position=16)
                    linha += Formatter.insertFloat(number=pair[1], leng_max=16, start_position=len(linha), final_position=32)
                    self.branch += linha + "\n"
                self.branch += Formatter.insertString(string="9999", start_position=0, final_position=16)

            linha = Formatter.insertInteger(number=0, leng_max=2, start_position=0, final_position=2)
            if self.phase_pos == "A":
                linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
            elif self.phase_pos == "B":
                linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
            elif self.phase_pos == "C":
                linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
            elif self.phase_pos == "N":
                linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

            if self.bus_neg is not None:
                if self.phase_neg == "A":
                    linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
                elif self.phase_neg == "B":
                    linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
                elif self.phase_neg == "C":
                    linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
                elif self.phase_neg == "N":
                    linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=14)
            linha += Formatter.insertFloat(number=self.curr, leng_max=6, start_position=len(linha), final_position=32)
            self.branch += linha

        elif self.zeroseq != 0 or rdamp != 0:
            linha = Formatter.insertInteger(number=0, leng_max=2, start_position=0, final_position=2)
            if self.phase_pos == "A":
                linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
            elif self.phase_pos == "B":
                linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
            elif self.phase_pos == "C":
                linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
            elif self.phase_pos == "N":
                linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

            if self.bus_neg is not None:
                if self.phase_neg == "A":
                    linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
                elif self.phase_neg == "B":
                    linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
                elif self.phase_neg == "C":
                    linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
                elif self.phase_neg == "N":
                    linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=14)

            if self.zeroseq:
                linha += Formatter.insertFloat(number=self.zeroseq, leng_max=6, start_position=len(linha), final_position=38)
            elif self.rdamp:
                linha += Formatter.insertFloat(number=self.rdamp, leng_max=6, start_position=len(linha), final_position=32)
            self.branch += linha

        if not self.hide_c:
            self.branch += "\nC /INDUTOR NAO-LINEAR TIPO 98"
