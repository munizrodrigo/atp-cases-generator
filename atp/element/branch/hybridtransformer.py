from atp.element.element import Element
from atp.node.node import Node
from atp.formatter.formatter import Formatter
from atp.element.branch.lnonlinear98 import LNonLinear98
from atp.element.branch.rlc import RLC
from atp.element.branch.rlccoupled import RLC_Coupled


class HybridTransformer(Element):
    """
    Classe responsavel pela adicao de Transformadores Hibridos.
    """
    def __init__(self, flux, curr, flux2, curr2, Io, rdamp, bus_core, bus_ref_core, bus_pos, bus_ref_pos, bus_neg, bus_ref_neg,
                 phase_core="A", phase_pos="A", phase_neg="A", zeroseq=0, omit=False, basefinal=False,
                 typecore="3leg_staked", databased="Typicalvalues", couplingp="Y", couplings="Y", listr=[], listL=[], listc=[], listcurrentflux=[[],[],[],[],[]]):

        """
        Metodo construtor da classe.
        Baseado no modelo encontrado em ATPDRAW Users' Manual version 5.6. e em Help Topics no ATPDraw.
        :param bus_core: Nome do no eletrico (trifasico) do nucleo
        :type bus_core: int ou basestring
        :param  phase_core: Fase na qual sera conectado no eletrico (trifasico) do nucleo
        :type  phase_core: int ou basestring
        :param bus_pos: Nome do no eletrico (trifasico) do lado primario
        :type bus_pos: int ou basestring
        :param  phase_pos: Fase na qual sera conectado o no eletrico (trifasico) do lado primario
        :type  phase_pos: int ou basestring
        :param bus_neg: Nome do no eletrico (trifasico) do lado secundario
        :type bus_neg: int ou basestring
        :param  phase_neg: Fase na qual sera conectado o no eletrico (trifasico) do lado secundario
        :type  phase_neg: int ou basestring
        :param bus_ref_core: Nome do no eletrico de referencia do nucleo
        :type bus_ref_core: int ou basestring
        :param bus_ref_pos: Nome do no eletrico de referencia do lado primario
        :type bus_ref_pos: int ou basestring
        :param bus_ref_neg: Nome do no eletrico de referencia do lado secundario
        :type bus_ref_neg: int ou basestring
        :param flux: Fluxo de magnetizacao nao linear em relacao ao no trifasico do nucleo
        :type flux: float
        :param curr: Corrente de magnetizacao nao linear em relacao ao no trifasico do nucleo
        :type curr: float
        :param flux2: Fluxo de magnetizacao nao linear em relacao ao no de referencia do nucleo
        :type flux2: float
        :param curr2: Corrente de magnetizacao nao linear em relacao ao no de referencia do nucleo
        :type curr2: float
        :param Io: Corrente de magnetizacao linear do nucleo
        :type Io: float
        :param zeroseq: Indutância constante de sequencia zero
        :type zeroseq: float
        :param omit: Omitir Indutância constante de sequencia zero
        :type omit: bool
        :param rdamp: Resistencia de amortecimento
        :type rdamp: float
        :param basefinal: Base no lugar da resistencia de amortecimento
        :type basefinal: bool
        :param typecore: Tipo de nucleo("triplex", "3leg_stacked" ou "5leg_stacked", com 3leg_stacked por padrao)
        :type typecore: basestring
        :param couplingp: Acoplamento do lado primario ("Y" ou "D")
        :type couplingp: basestring
        :param couplings: Acoplamento do lado secundario ("Y" ou "D")
        :type couplings: basestring
        :param listcurrentflux: Lista de listas de pares (corrente, fluxo) para a curva de saturacao
        :type listcurrentflux: list
        Exemplo:
        >> listcurrentflux = [[(1,2),(3,4)],[(5,6),(7,8)],[(9,10),(11,12)],[(13,14),(15,16)],[(17,18),(19,20)]]
        :param listr: Lista de resistencias de magneticazao
        :type listr: list
        :param listL: Lista de reatancias de magneticazao
        :type listL: list
        :param listc: Lista de capacitancias de magneticazao
        :type listc: list

        """
        super().__init__()
        self.bus_core = bus_core
        self.phase_core = phase_core
        self.bus_ref_core = bus_ref_core
        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_ref_pos = bus_ref_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.bus_ref_neg = bus_ref_neg
        self.flux = flux
        self.curr = curr
        self.flux2 = flux2
        self.curr2 = curr2
        self.Io = Io
        self.listr = listr
        self.listL = listL
        self.listc = listc
        self.listcurrentflux = listcurrentflux
        self.couplingp = couplingp
        self.couplings = couplings
        self.databased = databased

        if not omit and zeroseq != 0:
            self.zeroseq = zeroseq
        else:
            self.zeroseq = 0.001

        if not basefinal:
            self.rdamp = rdamp
        #else:
        #    self.rdamp =  dl/di/(w*100)

        hb_bus_core = Node("X" + self.bus_core, "Outro", self.phase_core) #Talvez ocorra erro
        hb_bus_core_fix = Node("T" + "0001", "Transformador Hibrido", None) #Talvez ocorra erro
        hb_bus_ref_core = Node("X" + self.bus_ref_core, "Outro", None) #Talvez ocorra erro

        self.branch = "C ----------------------------------------------------------------------" + "\n"
        self.branch += "C Nonlinear core representation" + "\n"
        self.branch += "C ----------------------------------------------------------------------" + "\n"
        if not listcurrentflux:
            self.n0 = LNonLinear98(flux=self.flux, curr=self.curr, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="A", bus_neg=hb_bus_core_fix, phase_neg="A", hide_c=True)
            self.n1 = LNonLinear98(flux=self.flux, curr=self.curr, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="B", bus_neg=hb_bus_core_fix, phase_neg="B", hide_c=True)
            self.n2 = LNonLinear98(flux=self.flux, curr=self.curr, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="C", bus_neg=hb_bus_core_fix, phase_neg="C", hide_c=True)
            self.branch += self.n0.branch + "\n"
            self.branch += self.n1.branch + "\n"
            self.branch += self.n2.branch + "\n"
            if not typecore == "triplex":
                self.n3 = LNonLinear98(flux=self.flux2, curr=self.curr2, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="B", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                self.n4 = LNonLinear98(flux=self.flux2, curr=self.curr2, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="C", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                self.branch += self.n3.branch + "\n"
                self.branch += self.n4.branch + "\n"
                if typecore == "3leg_staked":
                    self.n5 = LNonLinear98(flux=0, curr=0, zeroseq=self.zeroseq, rdamp=0, bus_pos=hb_bus_core, phase_pos="A", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                    self.n6 = LNonLinear98(flux=0, curr=0, zeroseq=self.zeroseq, rdamp=0, bus_pos=hb_bus_core_fix, phase_pos="C", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                    self.branch += self.n5.branch + "\n"
                    self.branch += self.n6.branch + "\n"
                # '''
                # elif typecore == "5leg_staked":
                #     #self.zeroseq =  (3*Pleg+2*Pyoke+2*Pout) == p*(3+2*Vry*(Uy/U)^2+2*Vro*(Uo/U)^2))
                #     self.n5 = LNonLinear98(flux=self.flux2, curr=self.zeroseq, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="A", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                #     self.n6 = LNonLinear98(flux=self.flux2, curr=self.zeroseq, zeroseq=0, rdamp=0, bus_pos=hb_bus_core_fix, phase_pos="C", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                #     self.branch += self.n5.branch + "\n"
                #     self.branch += self.n6.branch + "\n"
                # '''
        else: #Acrescimo de curva de saturacao #
            self.n0 = LNonLinear98(flux=self.flux, curr=self.curr, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="A", bus_neg=hb_bus_core_fix, phase_neg="A", currentflux=listcurrentflux[0], hide_c=True)
            self.n1 = LNonLinear98(flux=self.flux, curr=self.curr, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="B", bus_neg=hb_bus_core_fix, phase_neg="B", currentflux=listcurrentflux[1], hide_c=True)
            self.n2 = LNonLinear98(flux=self.flux, curr=self.curr, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="C", bus_neg=hb_bus_core_fix, phase_neg="C", currentflux=listcurrentflux[2], hide_c=True)
            self.branch += self.n0.branch + "\n"
            self.branch += self.n1.branch + "\n"
            self.branch += self.n2.branch + "\n"
            if not typecore == "triplex":
                self.n3 = LNonLinear98(flux=self.flux2, curr=self.curr2, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="B", bus_neg=hb_bus_ref_core, phase_neg=None, currentflux=listcurrentflux[3], hide_c=True)
                self.n4 = LNonLinear98(flux=self.flux2, curr=self.curr2, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="C", bus_neg=hb_bus_ref_core, phase_neg=None, currentflux=listcurrentflux[4], hide_c=True)
                self.branch += self.n3.branch + "\n"
                self.branch += self.n4.branch + "\n"
                if typecore == "3leg_staked":
                    self.n5 = LNonLinear98(flux=0, curr=0, zeroseq=self.zeroseq, rdamp=0, bus_pos=hb_bus_core, phase_pos="A", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                    self.n6 = LNonLinear98(flux=0, curr=0, zeroseq=self.zeroseq, rdamp=0, bus_pos=hb_bus_core_fix, phase_pos="C", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                    self.branch += self.n5.branch + "\n"
                    self.branch += self.n6.branch + "\n"
                # """
                # elif typecore == "5leg_staked":
                #     #self.zeroseq =  (3*Pleg+2*Pyoke+2*Pout) == p*(3+2*Vry*(Uy/U)^2+2*Vro*(Uo/U)^2))
                #     self.n5 = LNonLinear98(flux=self.flux2, curr=self.zeroseq, zeroseq=0, rdamp=0, bus_pos=hb_bus_core, phase_pos="A", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                #     self.n6 = LNonLinear98(flux=self.flux2, curr=self.zeroseq, zeroseq=0, rdamp=0, bus_pos=hb_bus_core_fix, phase_pos="C", bus_neg=hb_bus_ref_core, phase_neg=None, hide_c=True)
                #     self.branch += self.n5.branch + "\n"
                #     self.branch += self.n6.branch + "\n"
                # """
        self.n7 = LNonLinear98(flux=0, curr=0, zeroseq=0, rdamp=self.rdamp, bus_pos=hb_bus_core_fix, phase_pos="A", bus_neg=hb_bus_core, phase_neg="B", hide_c=True)
        self.n8 = LNonLinear98(flux=0, curr=0, zeroseq=0, rdamp=self.rdamp, bus_pos=hb_bus_core_fix, phase_pos="B", bus_neg=hb_bus_core, phase_neg="C", hide_c=True)
        self.branch += self.n7.branch + "\n"
        self.branch += self.n8.branch + "\n"

        ## Parte de Comportamento Linear do Núcleo#
        linha = Formatter.insertString(string="", start_position=0, final_position=2)
        linha += Formatter.insertString(string=hb_bus_core.phaseA, start_position=len(linha), final_position=8)
        linha += Formatter.insertFloat(number=self.Io, leng_max=6, start_position=len(linha), final_position=32)
        self.branch += linha + "\n"

        linha = Formatter.insertString(string="", start_position=0, final_position=2)
        linha += Formatter.insertString(string=hb_bus_core.phaseB, start_position=len(linha), final_position=8)
        linha += Formatter.insertFloat(number=self.Io, leng_max=6, start_position=len(linha), final_position=32)
        self.branch += linha + "\n"

        linha = Formatter.insertString(string="", start_position=0, final_position=2)
        linha += Formatter.insertString(string=hb_bus_core.phaseC, start_position=len(linha), final_position=8)
        linha += Formatter.insertFloat(number=self.Io, leng_max=6, start_position=len(linha), final_position=32)
        self.branch += linha + "\n"

        self.branch += "C ----------------------------------------------------------------------" + "\n"
        self.branch += "C [R] matrix" + "\n"
        self.branch += "C ----------------------------------------------------------------------" + "\n"
        self.r0 = RLC(R=self.listr[0], L=0, C=0, bus_pos=bus_pos, phase_pos="A", bus_neg=bus_pos, phase_neg="X", vintage=1, printvintage="cabecalho", hide_c=True)
        self.r1 = RLC(R=self.listr[0], L=0, C=0, bus_pos=bus_pos, phase_pos="B", bus_neg=bus_pos, phase_neg="Y", vintage=1, printvintage=None, hide_c=True)
        self.r2 = RLC(R=self.listr[0], L=0, C=0, bus_pos=bus_pos, phase_pos="C", bus_neg=bus_pos, phase_neg="Z", vintage=1, printvintage=None, hide_c=True)
        self.r3 = RLC(R=self.listr[1], L=0, C=0, bus_pos=bus_neg, phase_pos="A", bus_neg=bus_neg, phase_neg="X", vintage=1, printvintage=None, hide_c=True)
        self.r4 = RLC(R=self.listr[1], L=0, C=0, bus_pos=bus_neg, phase_pos="B", bus_neg=bus_neg, phase_neg="Y", vintage=1, printvintage=None, hide_c=True)
        self.r5 = RLC(R=self.listr[1], L=0, C=0, bus_pos=bus_neg, phase_pos="C", bus_neg=bus_neg, phase_neg="Z", vintage=1, printvintage=None, hide_c=True)
        self.branch += self.r0.branch + "\n"
        self.branch += self.r1.branch + "\n"
        self.branch += self.r2.branch + "\n"
        self.branch += self.r3.branch + "\n"
        self.branch += self.r4.branch + "\n"
        self.branch += self.r5.branch + "\n"

        self.branch += "C ----------------------------------------------------------------------" + "\n"
        self.branch += "C [A] matrix" + "\n"
        self.branch += "C ----------------------------------------------------------------------" + "\n"
        self.branch += "  USE AR" + "\n"
        self.l = []
        self.l.append(RLC_Coupled(R=self.listL[0], L=0, C=0,  bus_pos=self.bus_pos, phase_pos="X", bus_neg=("XX"+self.bus_ref_pos if self.couplingp == "Y" else self.bus_pos),
                                  phase_neg=("" if self.couplingp == "Y" else "C"), type=1, vintage=1, printvintage=None, precision=True, hide_c=True))
        self.l.append(RLC_Coupled(R=self.listL[1], L=0, C=0,  bus_pos=("XX"+self.bus_ref_neg if self.couplingp == "D" and self.couplings == "Y" else self.bus_neg), phase_pos=("" if self.couplingp == "D" and self.couplings == "Y" else "Y"),
                                  bus_neg=("XX"+bus_ref_neg if self.couplingp == "Y" and self.couplings == "Y" else bus_neg), phase_neg=("" if self.couplingp == "Y" and self.couplings == "Y" else "C"), type=2, vintage=1, printvintage=None, precision=True, hide_c=True))
        #equivalente.formatA6("X", "X", self.busrefs) if (self.couplingp == "Y" and self.couplings == "Y") or (self.couplingp == "D" and self.couplings == "Y") else equivalente.formatA6(self.buss, sigla="X", ph3="C"),
        self.l.append(RLC_Coupled(R=self.listL[2], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True, hide_c=True))
        self.l.append(RLC_Coupled(R=self.listL[3], L=0, C=0, bus_pos=hb_bus_core, phase_pos="A", bus_neg=hb_bus_core_fix, phase_neg="A", type=3, vintage=1, printvintage=None, precision=True, hide_c=True))
        for i in range(4, 6):
            self.l.append(RLC_Coupled(R=self.listL[i], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True))
        self.l.append(RLC_Coupled(R=self.listL[6], L=0, C=0, bus_pos=self.bus_pos, phase_pos="Y", bus_neg=("XX" + self.bus_ref_pos if self.couplingp == "Y" else self.bus_pos),
                                  phase_neg=("" if self.couplingp == "Y" else "A"), type=4, vintage=1, printvintage=None, precision=True, hide_c=True))
        for i in range(7, 10):
            self.l.append(RLC_Coupled(R=self.listL[i], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True))
        self.l.append(RLC_Coupled(R=self.listL[10], L=0, C=0, bus_pos=("XX" + self.bus_ref_neg if self.couplingp == "D" and self.couplings == "Y" else self.bus_neg), phase_pos=("" if self.couplingp == "D" and self.couplings == "Y" else "Z"),
                                  bus_neg=("XX" + bus_ref_neg if self.couplingp == "Y" and self.couplings == "Y" else bus_neg),phase_neg=("" if self.couplingp == "Y" and self.couplings == "Y" else "A"), type=5, vintage=1, printvintage=None, precision=True, hide_c=True))
        #equivalente.formatA6("X", "X", self.busrefs) if (self.couplingp == "Y" and self.couplings == "Y") or (self.couplingp == "D" and self.couplings== "Y") else equivalente.formatA6(self.buss, sigla="X", ph3="A"),#equivalente.formatA6(self.buss, sigla="X", ph3="B") em alguma combinacao
        for i in range(11, 15):
            self.l.append(RLC_Coupled(R=self.listL[i], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True))
        self.l.append(RLC_Coupled(R=self.listL[15], L=0, C=0, bus_pos=hb_bus_core, phase_pos="B", bus_neg=hb_bus_core_fix, phase_neg="B", type=6, vintage=1, printvintage=None, precision=True, hide_c=True))
        for i in range(16, 21):
            self.l.append(RLC_Coupled(R=self.listL[i], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True))
        self.l.append(RLC_Coupled(R=self.listL[21], L=0, C=0, bus_pos=self.bus_pos, phase_pos="Z", bus_neg=("XX"+self.bus_ref_pos if self.couplingp == "Y" else self.bus_pos),
                                  phase_neg=("" if self.couplingp == "Y" else "B"), type=7, vintage=1, printvintage=None, precision=True, hide_c=True))
        for i in range(22, 28):
            self.l.append(RLC_Coupled(R=self.listL[i], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True))
        self.l.append(RLC_Coupled(R=self.listL[28], L=0, C=0, bus_pos=("XX" + self.bus_ref_neg if self.couplingp == "D" and self.couplings == "Y" else self.bus_neg), phase_pos=("" if self.couplingp == "D" and self.couplings == "Y" else "X"),
                                  bus_neg=("XX" + bus_ref_neg if self.couplingp == "Y" and self.couplings == "Y" else bus_neg), phase_neg=("" if self.couplingp == "Y" and self.couplings == "Y" else "B"), type=8, vintage=1, printvintage=None, precision=True, hide_c=True))
        #equivalente.formatA6("X", "X", self.busrefs) if (self.couplingp == "Y" and self.couplings == "Y") or (self.couplingp=="D" and self.couplings=="Y") else equivalente.formatA6(self.buss, sigla="X", ph3="B"), #equivalente.formatA6(self.buss, sigla="X", ph3="C") em alguma combinacao # equivalente.formatA6(self.buss, sigla="X", ph3="C") em alguma combinacao
        for i in range(29, 36):
            self.l.append(RLC_Coupled(R=self.listL[i], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True))
        self.l.append(RLC_Coupled(R=self.listL[36], L=0, C=0, bus_pos=hb_bus_core, phase_pos="C", bus_neg=hb_bus_core_fix, phase_neg="C", type=9, vintage=1, printvintage=None, precision=True, hide_c=True))
        for i in range(37, 45):
            self.l.append(RLC_Coupled(R=self.listL[i], L=0, C=0, bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None, precision=True))

        for k in range(0, 45):
            self.branch += self.l[k].branch + "\n"

        self.branch += "  USE RL" + "\n"
        self.branch += "C ----------------------------------------------------------------------" + "\n"
        self.branch += "C [C] matrix" + "\n"
        self.branch += "C ----------------------------------------------------------------------" + "\n"
        self.branch += "C First half at the start of the windings" + "\n"
        self.c = []
        self.c.append(RLC_Coupled(R=100000000, L=0, C=self.listc[0], bus_pos=bus_pos, phase_pos="A", bus_neg=None, phase_neg=None, type=1, vintage=1, printvintage=None))  # em Y&Y
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[1], bus_pos=("XX"+self.bus_ref_neg if couplingp == "D" and couplings == "Y" else self.bus_neg), phase_pos=("" if couplingp == "D" and couplings == "Y" else "B" if couplingp == "D" and couplings == "D" else "A"),
                                  bus_neg=None, phase_neg=None, type=2, vintage=1, printvintage=None))#equivalente.formatA6(self.buss, sigla="X", ph3="B") em D&D
        self.c.append(RLC_Coupled(R=100000000, L=0, C=self.listc[2], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[3], bus_pos=bus_pos, phase_pos="B", bus_neg=None, phase_neg=None, type=3, vintage=1, printvintage=None))  # Y&Y e Y&D
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[4], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=100000000, L=0, C=self.listc[5], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[6], bus_pos=("XX" + self.bus_ref_neg if couplingp == "D" and couplings == "Y" else self.bus_neg), phase_pos=("" if couplingp == "D" and couplings == "Y" else "C" if couplingp == "D" and couplings == "D" else "B"),
                                  bus_neg=None, phase_neg=None, type=4, vintage=1, printvintage=None))#equivalente.formatA6(self.buss, sigla="X", ph3="C") em D&D
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[7], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[8], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=100000000, L=0, C=self.listc[9], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[10], bus_pos=bus_pos, phase_pos="C", bus_neg=None, phase_neg=None, type=5, vintage=1, printvintage=None)) #Y&Y
        for i in range(11, 14):
            self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[i], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=100000000, L=0, C=self.listc[14], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[15], bus_pos=("XX" + self.bus_ref_neg if couplingp == "D" and couplings == "Y" else self.bus_neg), phase_pos=("" if couplingp == "D" and couplings == "Y" else "A" if couplingp == "D" and couplings == "D" else "C"),
                                  bus_neg=None, phase_neg=None, type=6, vintage=1, printvintage=None)) #equivalente.formatA6(self.buss, sigla="X", ph3="A") em D&D
        for i in range(16, 20):
            self.c.append(RLC_Coupled(R=0, L=0, C=self.listc[i], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c.append(RLC_Coupled(R=100000000, L=0, C=self.listc[20], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        for j in range(0, 21):
            self.branch += self.c[j].branch + "\n"

        self.branch += "C Second half at the end of the windings" + "\n"
        self.c2 = []
        self.c2.append(RLC_Coupled(R=100000000, L=0, C=self.listc[0], bus_pos=(self.bus_pos if self.couplingp == "D" else "XX"+self.bus_ref_pos), phase_pos=("C" if self.couplingp == "D" else ""), bus_neg=None, phase_neg=None, type=1, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[1], bus_pos=("XX"+self.bus_ref_neg if self.couplingp == "Y" and self.couplings=="D" else self.bus_neg), phase_pos=("" if self.couplingp == "Y" and self.couplings=="D" else "C"), bus_neg=None, phase_neg=None, type=2, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=100000000, L=0, C=self.listc[2], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[3], bus_pos=(self.bus_pos if (self.couplingp == "D" and self.couplings == "Y") or (self.couplingp == "D" and self.couplings == "D") else "XX" + self.bus_ref_pos),
                                   phase_pos=("A" if (self.couplingp == "D" and self.couplings == "Y") or (self.couplingp == "D" and self.couplings == "D") else ""), bus_neg=None, phase_neg=None,type=3, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[4], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=100000000, L=0, C=self.listc[5], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[6], bus_pos=(self.bus_neg if self.couplingp == "Y" and self.couplings == "D" else "XX"+self.bus_ref_neg if self.couplingp == "Y" and self.couplings == "Y" else self.bus_neg),
                                   phase_pos=("C" if self.couplingp == "Y" and self.couplings == "D" else "" if self.couplingp == "Y" and self.couplings == "Y" else "A"), bus_neg=None, phase_neg=None, type=4, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[7], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[8], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=100000000, L=0, C=self.listc[9], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[10], bus_pos=(self.bus_pos if (self.couplingp == "D" and self.couplings == "Y") or (self.couplingp == "D" and self.couplings == "D") else "XX" + self.bus_ref_pos),
                                   phase_pos=("B" if (self.couplingp == "D" and self.couplings == "Y") or (self.couplingp == "D" and self.couplings == "D") else ""), bus_neg=None, phase_neg=None, type=5, vintage=1, printvintage=None))
        for i in range(11, 14):
            self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[i], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=100000000, L=0, C=self.listc[14], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[15], bus_pos=("XX" + self.bus_ref_pos if self.couplingp == "Y" and self.couplings == "Y" else self.bus_neg), phase_pos=("" if self.couplingp == "Y" and self.couplings == "Y" else "B"), bus_neg=None, phase_neg=None,
                                   type=6, vintage=1, printvintage=None))
        for i in range(16, 20):
            self.c2.append(RLC_Coupled(R=0, L=0, C=self.listc[i], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        self.c2.append(RLC_Coupled(R=100000000, L=0, C=self.listc[20], bus_pos=None, phase_pos=None, bus_neg=None, phase_neg=None, vintage=1, printvintage=None))
        for j in range(0, 21):
            if j == 20:
                self.branch += self.c2[j].branch
            else:
                self.branch += self.c2[j].branch + "\n"
