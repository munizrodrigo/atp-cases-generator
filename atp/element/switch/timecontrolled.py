from atp.element.element import Element
from atp.formatter.formatter import Formatter


class TimeControlled(Element):
    """
    Classe responsavel pelo chaveamento do circuito controlado por tempo.
    """
    def __init__(self, bus_pos, tclose, topen, phase_pos="A", bus_neg=None, phase_neg="A", Ie=0, output_value=None, hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.5.1 do Guia Resumido no Atp.
        :param tclose: Instante para fechar a(s) chave(s)(Fechado por padrão ou tclose = -1 )
        type tclose: float
        :param topen: Instante o qual antes a chave não poderá abrir(Fechado por padrão ou topen = 1000)
        type topen: float
        :param Ie: Corrente de margem
        type Ie: float
        :param output_value: Marcador de Variaveis de Saida do Atp((Verificar valores no topico 5.4.3 do Guia Resumido do Atp)
        type output_value: int
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.tclose = tclose
        self.topen = topen
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
                self.switch = "C CHAVE CONTROLADA POR TEMPO - POS:" + self.bus_pos.name + "\n"
            else:
                self.switch = "C CHAVE CONTROLADA POR TEMPO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        if self.phase_pos == "A":
            linha = Formatter.insertString(string=self.bus_pos.phaseA, start_position=0, final_position=8)
        elif self.phase_pos == "B":
            linha = Formatter.insertString(string=self.bus_pos.phaseB, start_position=0, final_position=8)
        elif self.phase_pos == "C":
            linha = Formatter.insertString(string=self.bus_pos.phaseC, start_position=0, final_position=8)
        elif self.phase_pos == "N":
            linha = Formatter.insertString(string=self.bus_pos.phaseN, start_position=0, final_position=8)

        if self.bus_neg is not None:
            if self.phase_neg == "A":
                linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
            elif self.phase_neg == "B":
                linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
            elif self.phase_neg == "C":
                linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
            elif self.phase_neg == "N":
                linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=14)

        linha += Formatter.insertFloat(number=self.tclose, leng_max=10, start_position=len(linha), final_position=24)
        linha += Formatter.insertFloat(number=self.topen, leng_max=10, start_position=len(linha), final_position=34)
        linha += Formatter.insertFloat(number=self.Ie, leng_max=10, start_position=len(linha), final_position=44)
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)

        self.switch += linha

        if not self.hide_c:
            self.switch += "\nC /CHAVE CONTROLADA POR TEMPO"

