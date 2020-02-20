from atp.element.element import Element
from atp.formatter.formatter import Formatter

class LinePi_3ph(Element):
    """
    Classe responsavel pela adicao de linhas de transmissao trifasicas usando o modelo pi a parametros concentrados.
    """
    def __init__(self, R, L, C, bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", hide_c=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.4.4 do Guia Resumido do Atp.
        :param R: Matriz de Resistencias em Ohm
        :type R: list
        Exemplo:
        R = [
             [R11, R12, R13],
             [R21, R22, R23],
             [R31, R32, R33]
            ]
        :param L: Matriz de Indutancias em mH se xopt = 0 ou Matriz de Reatancias em Ohm na frequencia xopt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre xopt)
        :type L: list
        Exemplo:
        L = [
             [L11, L12, L13],
             [L21, L22, L23],
             [L31, L32, L33]
            ]
        :param C: Matriz de Capacitancias em uF se copt = 0 ou Matriz de Susceptancias em uS na frequencia copt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre copt)
        :type C: list
        Exemplo:
        C = [
             [C11, C12, C13],
             [C21, C22, C23],
             [C31, C32, C33]
            ]
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
        self.R = R
        self.L = L
        self.C = C
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C LINE PI TRI PH - POS:" + self.bus_pos.name + "\n"
            else:
                self.branch = "C LINE PI TRI PH - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        linha = Formatter.insertInteger(number=1, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
        if self.bus_neg is not None:
            linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
        linha += Formatter.insertFloat(number=self.R[0][0], leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=self.L[0][0], leng_max=6, start_position=len(linha), final_position=38)
        linha += Formatter.insertFloat(number=self.C[0][0], leng_max=6, start_position=len(linha), final_position=44)

        self.branch += linha + "\n"

        linha = Formatter.insertInteger(number=2, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
        if self.bus_neg is not None:
            linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
        linha += Formatter.insertFloat(number=self.R[1][0], leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=self.L[1][0], leng_max=6, start_position=len(linha), final_position=38)
        linha += Formatter.insertFloat(number=self.C[1][0], leng_max=6, start_position=len(linha), final_position=44)
        linha += Formatter.insertFloat(number=self.R[1][1], leng_max=6, start_position=len(linha), final_position=50)
        linha += Formatter.insertFloat(number=self.L[1][1], leng_max=6, start_position=len(linha), final_position=56)
        linha += Formatter.insertFloat(number=self.C[1][1], leng_max=6, start_position=len(linha), final_position=62)

        self.branch += linha + "\n"

        linha = Formatter.insertInteger(number=2, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
        if self.bus_neg is not None:
            linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
        linha += Formatter.insertFloat(number=self.R[2][0], leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=self.L[2][0], leng_max=6, start_position=len(linha), final_position=38)
        linha += Formatter.insertFloat(number=self.C[2][0], leng_max=6, start_position=len(linha), final_position=44)
        linha += Formatter.insertFloat(number=self.R[2][1], leng_max=6, start_position=len(linha), final_position=50)
        linha += Formatter.insertFloat(number=self.L[2][1], leng_max=6, start_position=len(linha), final_position=56)
        linha += Formatter.insertFloat(number=self.C[2][1], leng_max=6, start_position=len(linha), final_position=62)
        linha += Formatter.insertFloat(number=self.R[2][2], leng_max=6, start_position=len(linha), final_position=68)
        linha += Formatter.insertFloat(number=self.L[2][2], leng_max=6, start_position=len(linha), final_position=74)
        linha += Formatter.insertFloat(number=self.C[2][2], leng_max=6, start_position=len(linha), final_position=80)

        self.branch += linha

        if not self.hide_c:
            self.branch += "\nC /LINE PI TRI PH"