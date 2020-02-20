from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node


class SaturableTransformer3ph(Element): #Verificar necessidade de phase_pos, phase_neg ...
    """
    Classe responsavel pela adicao de Transformadores Trifasicos com Saturacao.
    """
    def __init__(self, bus_ref,  bus_pos, bus_neg, Rp=1, Lp=1, Vp=1, Rs=1, Ls=1, Vs=1, bus_ref_pos=0, bus_ref_neg=0,
                 phase_ref="A", phase_pos="A", phase_ref_pos="A", phase_neg="A", phase_ref_neg="A", rmag=1000000, Io=0,
                 Fo=0, currentflux=[], magoutput=0, output_value=0, couplingp="Y", couplings="Y", hide_c=False):
        """
        Metodo construtor da classe.
        Baseado no modelo encontrado no arquivo RB-04e do Atp RuleBook.
        :param bus_ref: Nome do no eletrico de referencia do transformador
        :type bus_ref: int ou basestring
        :param phase_ref: Fase na qual sera conectado o eletrico de referencia do transformador
        :type phase_ref: int ou basestring
        :param bus_pos: Nome do no eletrico (trifasico) do lado primario
        :type bus_pos: int ou basestring
        :param phase_pos: Fase na qual sera conectado o eletrico (trifasico) do lado primario
        :type phase_pos: int ou basestring
        :param bus_neg: Nome do no eletrico (trifasico) do lado secundario
        :type bus_neg: int ou basestring
        :param phase_neg: Fase na qual sera conectado o eletrico (trifasico) do lado secundario
        :type phase_neg: int ou basestring
        :param Rp: Resistencia no lado primario
        :type Rp: float
        :param Lp: Indutancia no lado primario
        :type Lp: float
        :param Vp: Tensao no lado primario
        :type Vp: float
        :param Rs: Resistencia no lado secundario
        :type Rs: float
        :param Ls: Indutancia no lado secundario
        :type Ls: float
        :param Vs: Tensao no lado secundario
        :type Vs: float
        :param bus_ref_pos: Nome do no eletrico de referencia do lado primario
        :type bus_ref_pos: int ou basestring
        :param phase_ref_pos: Fase na qual sera conectado o no eletrico de referencia do lado primario
        :type phase_ref_pos: int ou basestring
        :param bus_ref_neg: Nome do no eletrico de referencia do lado secundario
        :type bus_ref_neg: int ou basestring
        :param phase_ref_neg: Fase na qual sera conectado o no eletrico de referencia do lado secundario
        :type phase_ref_neg: int ou basestring
        :param rmag: Resistencia de magnetizacao
        :type rmag: float
        :param Io: Corrente de magnetizacao
        :type Io: float
        :param Fo: Fluxo de magnetizacao
        :type Fo: float
        :param currentflux: Lista de pares [corrente, fluxo] para a curva de saturacao
        :type currentflux: list
        :param magoutput: Marcador de Variaveis de Saida do Atp para a magnetizacao
        :type magoutput: int
        :param output_value: Marcador de Variaveis de Saida do Atp
        :type output_value: int
        :param couplingp: Acoplamento do lado primario ("Y" ou "D")
        :type couplingp: basestring
        :param couplings: Acoplamento do lado secundario ("Y" ou "D")
        :type couplings: basestring
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.bus_ref = bus_ref
        self.phase_ref = phase_ref
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.Rp = Rp
        self.Lp = Lp
        self.Vp = Vp
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.Rs = Rs
        self.Ls = Ls
        self.Vs = Vs
        self.rmag = rmag
        self.bus_ref_pos = bus_ref_pos
        self.phase_ref_pos = phase_ref_pos
        self.bus_ref_neg = bus_ref_neg
        self.phase_ref_neg = phase_ref_neg
        self.Io = Io
        self.Fo = Fo
        self.currentflux = currentflux
        self.magoutput = magoutput
        self.output_value = output_value
        self.couplingp = couplingp
        self.couplings = couplings
        self.hide_c = hide_c

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C TRANSFORMADOR SATURAVEL TRIFASICO - POS:" + self.bus_pos.name + "\n"
            else:
                if self.bus_ref_pos is None:
                    self.branch = "C TRANSFORMADOR SATURAVEL TRIFASICO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"
                else:
                    if self.bus_ref_neg is None:
                        self.branch = "C TRANSFORMADOR SATURAVEL TRIFASICO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos + "\n"
                    else:
                        self.branch = "C TRANSFORMADOR SATURAVEL TRIFASICO - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + " - REF_POS: " + self.bus_ref_pos + " - REF_NEG: " + self.bus_ref_neg + "\n"

        linha = Formatter.insertString(string="TRANSFORMER", start_position=0, final_position=13) # Consultar RuleBook RB-04E
        linha += Formatter.insertFloat(number=self.Io, leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=self.Fo, leng_max=6, start_position=len(linha), final_position=38)
        linha += Formatter.insertString(string=Node(name=self.bus_ref, type="Transformador Saturavel", sequence="A"), start_position=len(linha), final_position=44)
        linha += Formatter.insertFloat(number=self.rmag, leng_max=6, start_position=len(linha), final_position=50)
        linha += Formatter.insertInteger(number=self.magoutput, leng_max=1, start_position=len(linha), final_position=80)
        self.branch = linha + "\n"

        for pair in self.currentflux:
            linha = Formatter.insertFloat(number=pair[0], leng_max=16, start_position=0, final_position=16)
            linha += Formatter.insertFloat(number=pair[1], leng_max=16, start_position=len(linha), final_position=32)
            self.branch += linha + "\n"
        self.branch += Formatter.insertString(string="9999", start_position=0, final_position=16) + "\n"

        linha = Formatter.insertInteger(number=1, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=Node(name=self.bus_pos, type="Transformador Saturavel", sequence="A"), start_position=len(linha), final_position=8)
        linha += Formatter.insertString(string=Node(name=self.bus_ref_pos, type="Transformador Saturavel", sequence=self.phase_ref_pos) if self.couplingp == "Y" else Node(name=self.bus_pos, type="Transformador Saturavel", sequence="C"), start_position=len(linha), final_position=14)
        linha += Formatter.insertFloat(number=self.Rp, leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=self.Lp, leng_max=6, start_position=len(linha), final_position=38)
        linha += Formatter.insertFloat(number=self.Vp, leng_max=6, start_position=len(linha), final_position=44)
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertInteger(number=2, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=Node(name=self.bus_neg, type="Transformador Saturavel", sequence="A"), start_position=len(linha), final_position=8)
        linha += Formatter.insertString(string=Node(name=self.bus_ref_neg, type="Transformador Saturavel", sequence=self.phase_ref_pos) if self.couplings == "Y" else Node(name=self.bus_neg, type="Transformador Saturavel", sequence="B") if self.couplingp == "Y" else Node(name=self.bus_neg, type="Transformador Saturavel", sequence="C"), start_position=len(linha), final_position=14) # Obtido pela comparacao com cartoes gerados pelo ATPDraw
        linha += Formatter.insertFloat(number=self.Rs, leng_max=6, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=self.Ls, leng_max=6, start_position=len(linha), final_position=38)
        linha += Formatter.insertFloat(number=self.Vs, leng_max=6, start_position=len(linha), final_position=44)
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertString(string="TRANSFORMER", start_position=0, final_position=13)  # Consultar RuleBook RB-04E
        linha += Formatter.insertString(string=Node(name=self.bus_ref, type="Transformador Saturavel", sequence="A"), start_position=len(linha), final_position=20)
        linha += Formatter.insertString(string=Node(name=self.bus_ref, type="Transformador Saturavel", sequence="B"), start_position=len(linha), final_position=44)
        linha += Formatter.insertInteger(number=self.magoutput, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertInteger(number=1, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=Node(name=self.bus_pos, type="Transformador Saturavel", sequence="B"), start_position=len(linha), final_position=8)
        linha += Formatter.insertString(string=Node(name=self.bus_ref_pos, type="Transformador Saturavel", sequence=self.phase_ref_pos) if self.couplingp == "Y" else Node(name=self.bus_pos, type="Transformador Saturavel", sequence="A"), start_position=len(linha), final_position=14)
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertInteger(number=2, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=Node(name=self.bus_neg, type="Transformador Saturavel", sequence="B"), start_position=len(linha), final_position=8)
        linha += Formatter.insertString(string=Node(name=self.bus_ref_neg, type="Transformador Saturavel", sequence=self.phase_ref_pos) if self.couplings == "Y" else Node(name=self.bus_neg, type="Transformador Saturavel", sequence="C") if self.couplingp == "Y" else Node(name=self.bus_neg, type="Transformador Saturavel", sequence="A"), start_position=len(linha), final_position=14)  # Obtido pela comparacao com cartoes gerados pelo ATPDraw
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertString(string="TRANSFORMER", start_position=0, final_position=13)  # Consultar RuleBook RB-04E
        linha += Formatter.insertString(string=Node(name=self.bus_ref, type="Transformador Saturavel", sequence="A"), start_position=len(linha), final_position=20)
        linha += Formatter.insertString(string=Node(name=self.bus_ref, type="Transformador Saturavel", sequence="C"), start_position=len(linha), final_position=44)
        linha += Formatter.insertInteger(number=self.magoutput, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertInteger(number=1, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=Node(name=self.bus_pos, type="Transformador Saturavel", sequence="C"), start_position=len(linha), final_position=8)
        linha += Formatter.insertString(string=Node(name=self.bus_ref_pos, type="Transformador Saturavel", sequence=self.phase_ref_pos) if self.couplingp == "Y" else Node(name=self.bus_pos, type="Transformador Saturavel", sequence="B"), start_position=len(linha), final_position=14)
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha + "\n"

        linha = Formatter.insertInteger(number=2, leng_max=2, start_position=0, final_position=2)
        linha += Formatter.insertString(string=Node(name=self.bus_neg, type="Transformador Saturavel", sequence="C"), start_position=len(linha), final_position=8)
        linha += Formatter.insertString(string=Node(name=self.bus_ref_neg, type="Transformador Saturavel", sequence=self.phase_ref_pos) if self.couplings == "Y" else Node(name=self.bus_neg, type="Transformador Saturavel", sequence="A") if self.couplingp == "Y" else Node(name=self.bus_neg, type="Transformador Saturavel", sequence="B"), start_position=len(linha), final_position=14)  # Obtido pela comparacao com cartoes gerados pelo ATPDraw
        linha += Formatter.insertInteger(number=self.output_value, leng_max=1, start_position=len(linha), final_position=80)
        self.branch += linha

        if not self.hide_c:
            self.branch += "\nC /TRANSFORMADOR SATURAVEL TRIFASICO"
