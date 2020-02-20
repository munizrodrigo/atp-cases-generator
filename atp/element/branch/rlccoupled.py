from atp.formatter.formatter import Formatter
from atp.element.element import Element


class RLC_Coupled(Element):
    """
    Classe responsavel pela adicao de componentes RLC pseudo acoplado.
    """
    def __init__(self, R, L, C,  bus_pos, phase_pos="A", bus_neg=None, phase_neg="A", bus_ref_pos=None, phase_ref_pos="A",
                 bus_ref_neg=None, phase_ref_neg="A", type=0, vintage=0, printvintage=None, precision=False, hide_c= False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no arquivo RB-04a-lec do Atp RuleBook com alteracoes obtida pelo cartao de transformador hibrido.
        :param R: Resistencia em Ohm
        :type R: float
        :param L: Indutancia em mH se xopt = 0 ou Reatancia em Ohm na frequencia xopt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre xopt)
        :type L: float
        :param C: Capacitancia em uF se copt = 0 ou Susceptancia em uS na frequencia copt (consultar topico 5.2 do Guia Resumido do Atp para mais informacoes sobre copt)
        :type C: float
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param phase_pos: Fase na qual sera conectado o terminal positivo do elemento
        :type phase_pos: basestring
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param phase_neg: Fase na qual sera conectado o terminal negativo do elemento
        :type phase_neg: basestring
        :param bus_ref_pos: No eletrico de referencia na extremidade positiva do elemento
        :type bus_ref_pos: Node
        :param phase_ref_pos: Fase na qual sera conectado o terminal positivo de referencia do elemento
        :type phase_ref_pos: basestring
        :param bus_ref_neg: No eletrico de referencia na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_ref_neg: Node
        :param phase_ref_neg: Fase na qual sera conectado o terminal negativo de referencia do elemento
        :type phase_ref_neg: basestring
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        :param type: Tipo do Elemento RLC (Nao acoplado por padrao, com type = 0. Consultar topico 5.4 do Guia Resumido do Atp)
        :type type: int
        :param vintage: Precisao do Cartao (Consultar topico 5.4.1 do Guia Resumido do Atp)
        :type vintage: int
        :param printvintage: Marcador de formato de saída da string "$VINTAGE"
        :type printvintage: basestring
        """
        super().__init__()
        self.R = R
        self.L = L
        self.C = C
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.bus_ref_pos = bus_ref_pos
        self.phase_ref_pos = phase_ref_pos
        self.bus_ref_neg = bus_ref_neg
        self.phase_ref_neg = phase_ref_neg
        self.type = type
        self.vintage = vintage
        self.printvintage = printvintage
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C RLC MUTUALMENTE ACOPLADO - POS:" + self.bus_pos.name + "\n"
            else:
                if self.bus_ref_pos is None:
                    self.branch = "C RLC MUTUALMENTE ACOPLADO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"
                else:
                    if self.bus_ref_neg is None:
                        self.branch = "C RLC MUTUALMENTE ACOPLADO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos.name + "\n"
                    else:
                        self.branch = "C RLC MUTUALMENTE ACOPLADO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos.name + " - REF_NEG: " + self.bus_ref_neg.name + "\n"

        if vintage == 1:  # Modo de Alta Precisao
            if printvintage == "cabecalhorodape" or "cabecalho":
                self.branch = "$VINTAGE,1" + "\n"
            #self.branch = Formatter.insertString(string="USE AR", start_position=3, final_position=8)

            linha = Formatter.insertInteger(number=self.type, leng_max=2, start_position=0, final_position=2)
            if self.phase_pos == "A":
                linha += Formatter.insertString(string=self.bus_pos.phaseA, start_position=len(linha), final_position=8)
            elif self.phase_pos == "B":
                linha += Formatter.insertString(string=self.bus_pos.phaseB, start_position=len(linha), final_position=8)
            elif self.phase_pos == "C":
                linha += Formatter.insertString(string=self.bus_pos.phaseC, start_position=len(linha), final_position=8)
            elif self.phase_pos == "N":
                linha += Formatter.insertString(string=self.bus_pos.phaseN, start_position=len(linha), final_position=8)

            if self.bus_neg == -1: # Valor de bus_neg para configurar o auto-incremento
                if Formatter.isInt(self.bus_pos):
                    if self.phase_pos == "A":
                        linha += Formatter.insertString(string=self.bus_pos.phaseA + 1, start_position=len(linha), final_position=14)
                    elif self.phase_pos == "B":
                        linha += Formatter.insertString(string=self.bus_pos.phaseB + 1, start_position=len(linha), final_position=14)
                    elif self.phase_pos == "C":
                        linha += Formatter.insertString(string=self.bus_pos.phaseC + 1, start_position=len(linha), final_position=14)
                    elif self.phase_pos == "N":
                        linha += Formatter.insertString(string=self.bus_pos.phaseN + 1, start_position=len(linha), final_position=14)
                else:
                    raise Exception('O uso da auto locacao de bus2 deve ser feita somente para um bus1 inteiro')
            else:
                if self.phase_neg == "A":
                    linha += Formatter.insertString(string=self.bus_neg.phaseA, start_position=len(linha), final_position=14)
                elif self.phase_neg == "B":
                    linha += Formatter.insertString(string=self.bus_neg.phaseB, start_position=len(linha), final_position=14)
                elif self.phase_neg == "C":
                    linha += Formatter.insertString(string=self.bus_neg.phaseC, start_position=len(linha), final_position=14)
                elif self.phase_neg == "N":
                    linha += Formatter.insertString(string=self.bus_neg.phaseN, start_position=len(linha), final_position=14)

            if self.phase_ref_pos == "A":
                linha += Formatter.insertString(string=self.bus_ref_pos.phaseA, start_position=len(linha), final_position=20)
            elif self.phase_ref_pos == "B":
                linha += Formatter.insertString(string=self.bus_ref_pos.phaseB, start_position=len(linha), final_position=20)
            elif self.phase_ref_pos == "C":
                linha += Formatter.insertString(string=self.bus_ref_pos.phaseC, start_position=len(linha), final_position=20)
            elif self.phase_ref_pos == "N":
                linha += Formatter.insertString(string=self.bus_ref_pos.phaseN, start_position=len(linha), final_position=20)

            if self.phase_ref_neg == "A":
                linha += Formatter.insertString(string=self.bus_ref_neg.phaseA, start_position=len(linha), final_position=26)
            elif self.phase_ref_neg == "B":
                linha += Formatter.insertString(string=self.bus_ref_neg.phaseB, start_position=len(linha), final_position=26)
            elif self.phase_ref_neg == "C":
                linha += Formatter.insertString(string=self.bus_ref_neg.phaseC, start_position=len(linha), final_position=26)
            elif self.phase_ref_neg == "N":
                linha += Formatter.insertString(string=self.bus_ref_neg.phaseN, start_position=len(linha), final_position=26)

            if precision:
                linha += Formatter.insertFloat(number=self.R, leng_max=25, start_position=len(linha), final_position=42,
                                               blank=False) #Baseado em simulacoes para o cartao de Reatancias do transformador hibrido
            else:
                linha += Formatter.insertFloat(number=self.R, leng_max=6, start_position=len(linha), final_position=42, blank=False)
            linha += Formatter.insertFloat(number=self.L, leng_max=6, start_position=len(linha), final_position=58, blank=False)
            linha += Formatter.insertFloat(number=self.C, leng_max=16, start_position=len(linha), final_position=74)
            self.branch += linha

            if printvintage == "cabecalhorodape" or "rodape":
                self.branch += "\n" + "$VINTAGE,0"

            if not self.hide_c:
                self.branch += "\nC /RLC MUTUALMENTE ACOPLADO"

        #Sem necessidade modo de precisao padrao ate o momento
