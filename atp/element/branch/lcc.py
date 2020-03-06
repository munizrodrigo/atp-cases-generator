import subprocess
import os

from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node
from os.path import isfile as file_exist


class LCC(Element):
    """
    Classe responsavel pela adicao de linhas de transmissao usando a rotina LINE CONSTANTS, assim como a execucao do
    ATP para a criacao do arquivo .lib necessario para a inclusao de elementos desse tipo.
    """
    def __init__(self, cond, dist, dat_name, bus_pos, bus_neg, run_cmd, rho=80, freq=60, fcar=0, icpr=100000,
                 icap=0, izpr=100000, modal=1, itrnsf=-9, metric=True, single=True, hidden_icpr_izpr=True,
                 simulation_path="", jmarti=True, freq_matrix=60000, freq_ss=60, decades=8, points_decade=10,
                 hide_c=False, overwrite=False):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no tópico 6 do Guia Resumido do Atp e na secao RB-210 do Atp RuleBook.
        :param cond: Lista de dicionarios contendo as informacoes de todos os condutores da linha de transmissao
        :type cond: list
        Exemplo:
        >> cond1 = {'ip': 1, 'skin': 0.25, 'resis': 1, 'ix': 4, 'react': 0,
        'diam': 4, 'horiz': 1, 'vtower': 1, 'vmid': 1, 'bus_in': 'B0000',
        'bus_out': 'B0001', 'fase': 'A'}
        >> cond2 = {'ip': 2, 'skin': 0.25, 'resis': 1, 'ix': 4, 'react': 0,
        'diam': 4, 'horiz': 1, 'vtower': 1.5, 'vmid': 1.5, 'bus_in': 'B0000', 'bus_out': 'B0001', 'fase': 'B'}
        >> cond3 = {'ip': 3, 'skin': 0.25, 'resis': 1, 'ix': 4, 'react': 0,
        'diam': 4, 'horiz': 1, 'vtower': 2, 'vmid': 2, 'bus_in': 'B0000', 'bus_out': 'B0001', 'fase': 'C'}
        >> cond = [cond1, cond2,cond3]
        :param dist: Distancia da linha de transmissao (em km se metric = True e em milhas caso contrario)
        :type dist: float
        :param dat_name: Nome do arquivo .dat a ser gerado com as configuracoes da linha
        :type dat_name: basestring
        :param bus_pos: No eletrico na extremidade positiva do elemento
        :type bus_pos: Node
        :param bus_neg: No eletrico na segunda extremidade do elemento (Aterrado por padrao)
        :type bus_neg: Node
        :param run_cmd: Objeto de configuracao ATP
        :type run_cmd: ATPConfiguration
        :param rho: Resistencia de terra homogenea de Carson
        :type rho: float
        :param freq: Frequencia para o calculo das constantes da linha
        :type freq: float
        :param fcar: Quantidade de termos na formula de Carson (0 nenhum termo, 1 calculo usando todos os termos da formula)
        :type fcar: int
        :param icpr: Tipo de impressao para a matriz de capacitancias de linha
        :type icpr: int
        :param icap: Opcoes para uso de icpr
        :type icap: int
        :param izpr: Tipo de impressao para a matriz de impedancias de linha
        :type izpr: int
        :param modal: Transposicao da linha (0 para linha transposta, 1 para linha não transposta)
        :type modal: int
        :param itrnsf: Requisicao da matriz de transformacao
        :type itrnsf: int
        :param metric: Uso do padrao metrico para os calculos (True para uso do padrao metrico, False para o padrao ingles)
        :type metric: bool
        :param single: Condutores solidos ou condutores multiplos (True para c solido, False para condutores geminados)
        :type single: bool
        :param hidden_icpr_izpr: Flag para a inclusao das variaveis icpr e izpr no arquivo .dat
        :type hidden_icpr_izpr: bool
        :param simulation_path: Caminho da simulacao
        :type simulation_path: basestring
        :param jmarti: Flag para o uso do modelo de JMarti
        :type jmarti: bool
        :param freq_matrix: Frequencia Matrix HZ
        :type freq_matrix: float
        :param freq_ss: Frequencia SS HZ
        :type freq_ss: float
        :param decades: Decadas
        :type decades: int
        :param points_decade: Pontos por decada
        :type points_decade: int
        :param hide_c: Definicao da visibilidade da linha inicial e final com comentario (Se True, a linha e omitida)
        :type hide_c: bool
        """
        super().__init__()
        self.cond = cond
        self.dist = dist
        self.dat_name = dat_name
        self.bus_pos = bus_pos
        self.bus_neg = bus_neg
        self.run_cmd = run_cmd
        self.rho = rho
        self.freq = freq
        self.fcar = fcar
        self.icpr = icpr
        self.icap = icap
        self.izpr = izpr
        self.modal = modal
        self.itrnsf = itrnsf
        self.metric = metric
        self.single = single
        self.hidden_icpr_izpr = hidden_icpr_izpr
        self.simulation_path = simulation_path
        self.jmarti = jmarti
        self.freq_matrix = freq_matrix
        self.freq_ss = freq_ss
        self.decades = decades
        self.points_decades = points_decade
        self.hide_c = hide_c

        self.dat_linhas = "BEGIN NEW DATA CASE\n"

        if self.jmarti:
            self.dat_linhas += "JMARTI SETUP\n" # Verificar topico 6 do Guia Resumido do ATP
        else:
            self.dat_linhas += "LINE CONSTANTS\n"  # Verificar topico 6 do Guia Resumido do ATP
        self.dat_linhas += "$ERASE\n"  # Obtido pela comparacao com o arquivo gerado pelo ATPDraw
        self.dat_linhas += "BRANCH  "
        for c in self.cond:
            self.dat_linhas += "IN___" + c["fase"] + "OUT__" + c["fase"]
        self.dat_linhas += "\n"
        if self.jmarti:
            self.dat_linhas += "LINE CONSTANTS\n"
        self.dat_linhas += "METRIC\n" if self.metric else "ENGLISH\n"
        if self.single: # Caso de condutores solidos
            for c in self.cond:
                linha = Formatter.insertInteger(number=c['ip'], leng_max=3, start_position=0, final_position=3)
                linha += Formatter.insertFloat(number=c['skin'], leng_max=5, start_position=len(linha), final_position=8)
                linha += Formatter.insertFloat(number=c['resis'], leng_max=8, start_position=len(linha), final_position=16)
                linha += Formatter.insertInteger(number=c['ix'], leng_max=2, start_position=len(linha), final_position=18)
                linha += Formatter.insertFloat(number=c['react'], leng_max=8, start_position=len(linha), final_position=26)
                linha += Formatter.insertFloat(number=c['diam'], leng_max=8, start_position=len(linha), final_position=34)
                linha += Formatter.insertFloat(number=c['horiz'], leng_max=8, start_position=len(linha), final_position=42)
                linha += Formatter.insertFloat(number=c['vtower'], leng_max=8, start_position=len(linha), final_position=50)
                linha += Formatter.insertFloat(number=c['vmid'], leng_max=8, start_position=len(linha), final_position=58)
                self.dat_linhas += linha + "\n"
        else: # Caso de condutores multiplos
            for c in self.cond:
                linha = Formatter.insertInteger(number=c['ip'], leng_max=3, start_position=0, final_position=3)
                linha += Formatter.insertFloat(number=c['skin'], leng_max=5, start_position=len(linha), final_position=8)
                linha += Formatter.insertFloat(number=c['resis'], leng_max=8, start_position=len(linha), final_position=16)
                linha += Formatter.insertInteger(number=c['ix'], leng_max=2, start_position=len(linha), final_position=18)
                linha += Formatter.insertFloat(number=c['react'], leng_max=8, start_position=len(linha), final_position=26)
                linha += Formatter.insertFloat(number=c['diam'], leng_max=8, start_position=len(linha), final_position=34)
                linha += Formatter.insertFloat(number=c['horiz'], leng_max=8, start_position=len(linha), final_position=42)
                linha += Formatter.insertFloat(number=c['vtower'], leng_max=8, start_position=len(linha), final_position=50)
                linha += Formatter.insertFloat(number=c['vmid'], leng_max=8, start_position=len(linha), final_position=58)
                linha += Formatter.insertFloat(number=c['separ'], leng_max=8, start_position=len(linha), final_position=66)
                linha += Formatter.insertFloat(number=c['alpha'], leng_max=6, start_position=len(linha), final_position=72)
                linha += Formatter.insertInteger(number=c['nb'], leng_max=2, start_position=len(linha), final_position=80)
                self.dat_linhas += linha + "\n"
        self.dat_linhas += "BLANK CARD ENDING CONDUCTOR CARDS" + "\n"
        if self.jmarti:
            linha = Formatter.insertFloat(number=self.rho, leng_max=8, start_position=0, final_position=8)
            linha += Formatter.insertFloat(number=self.freq_matrix, leng_max=8, start_position=len(linha), final_position=18)
            linha += Formatter.insertFloat(number=self.dist, leng_max=8, start_position=len(linha), final_position=52)
            linha += Formatter.insertInteger(number=self.modal, leng_max=2, start_position=len(linha), final_position=70)
            linha += Formatter.insertInteger(number=self.itrnsf, leng_max=2, start_position=len(linha), final_position=72)
            self.dat_linhas += linha + "\n"
            linha = Formatter.insertFloat(number=self.rho, leng_max=8, start_position=0, final_position=8)
            linha += Formatter.insertFloat(number=self.freq_ss, leng_max=8, start_position=len(linha), final_position=18)
            linha += Formatter.insertFloat(number=self.dist, leng_max=8, start_position=len(linha), final_position=52)
            linha += Formatter.insertInteger(number=self.modal, leng_max=2, start_position=len(linha), final_position=70)
            linha += Formatter.insertInteger(number=self.itrnsf, leng_max=2, start_position=len(linha), final_position=72)
            self.dat_linhas += linha + "\n"
            linha = Formatter.insertFloat(number=self.rho, leng_max=8, start_position=0, final_position=8)
            linha += Formatter.insertFloat(number=self.freq, leng_max=8, start_position=len(linha), final_position=18)
            linha += Formatter.insertFloat(number=self.dist, leng_max=8, start_position=len(linha), final_position=52)
            linha += Formatter.insertInteger(number=self.decades, leng_max=2, start_position=len(linha), final_position=62)
            linha += Formatter.insertInteger(number=self.points_decades, leng_max=2, start_position=len(linha), final_position=65)
            linha += Formatter.insertInteger(number=self.modal, leng_max=2, start_position=len(linha), final_position=70)
            linha += Formatter.insertInteger(number=self.itrnsf, leng_max=2, start_position=len(linha), final_position=72)
            self.dat_linhas += linha + "\n"
        else:
            linha = Formatter.insertFloat(number=self.rho, leng_max=8, start_position=0, final_position=8)
            linha += Formatter.insertFloat(number=self.freq, leng_max=10, start_position=len(linha), final_position=18)
            linha += Formatter.insertFloat(number=self.fcar, leng_max=10, start_position=len(linha), final_position=28)
            if not self.hidden_icpr_izpr:
                position = 30
                for n in list(map(int, list(str(self.icpr)))):
                    linha += Formatter.insertInteger(number=n, leng_max=1, start_position=len(linha), final_position=position)
                    position = position + 1
                position = 37
                for n in list(map(int, list(str(self.izpr)))):
                    linha += Formatter.insertInteger(number=n, leng_max=1, start_position=len(linha), final_position=position)
                    position = position + 1
            linha += Formatter.insertInteger(number=self.icap, leng_max=1, start_position=len(linha), final_position=44)
            linha += Formatter.insertFloat(number=self.dist, leng_max=8, start_position=len(linha), final_position=52)
            linha += Formatter.insertInteger(number=self.modal, leng_max=2, start_position=len(linha), final_position=70)
            linha += Formatter.insertInteger(number=self.itrnsf, leng_max=2, start_position=len(linha), final_position=72)
            self.dat_linhas += linha + "\n"

        self.dat_linhas += "BLANK CARD ENDING FREQUENCY CARDS\n"

        if self.jmarti:
            self.dat_linhas += "BLANK CARD ENDING LINE CONSTANT\n"
            self.dat_linhas += "DEFAULT\n"
            self.dat_linhas += "$PUNCH\n"
            self.dat_linhas += "BLANK CARD ENDING JMARTI SETUP\n"
        else:
            self.dat_linhas += "$PUNCH, " + self.dat_name + ".pch\n"  # Obtido pela comparacao com o arquivo gerado pelo ATPDraw
            self.dat_linhas += "BLANK CARD ENDING LINE CONSTANT\n"

        self.dat_linhas += "BEGIN NEW DATA CASE\n"
        self.dat_linhas += "BLANK CARD\n"

        complete_dat = os.path.join(self.simulation_path, self.dat_name + ".dat")

        try:
            arquivo_dat = open(complete_dat, 'r+')
            arquivo_dat.close()
            arquivo_dat = open(complete_dat, 'w+')
        except FileNotFoundError:
            arquivo_dat = open(complete_dat, 'w+')

        arquivo_dat.write(self.dat_linhas)
        arquivo_dat.close()

        # Execucao do arquivo .dat no ATP para a criacao do arquivo .pch, usado na geracao do arquivo .lib
        try:
            arquivo_pch = open(os.path.join(self.simulation_path, self.dat_name + ".pch"), 'r+')
            arquivo_pch.close()
            if overwrite:
                work = False
                while work is not True:
                    complete_command = [
                        self.run_cmd,
                        os.path.join(self.simulation_path, self.dat_name + ".dat"),
                        ">nul"
                    ]
                    subprocess.call(complete_command, shell=True)
                    work = file_exist(os.path.join(self.simulation_path,self.dat_name+".pch"))
        except FileNotFoundError:
            work = False
            while work is not True:
                complete_command = [
                    self.run_cmd,
                    os.path.join(self.simulation_path, self.dat_name + ".dat"),
                    ">nul"
                ]
                subprocess.call(complete_command, shell=True)
                work = file_exist(os.path.join(self.simulation_path, self.dat_name + ".pch"))

        arquivo_pch = open(os.path.join(self.simulation_path, self.dat_name + ".pch"), 'r+')
        pch_linhas = arquivo_pch.readlines()
        linhas_sel = []
        linha_cond = []
        n = 0
        for l in pch_linhas:
            if not l[0] == "C":
                n += 1
                linhas_sel.append(l)
                if l[0] == "-":
                    linha_cond.append(str(n + 1))
        arquivo_pch.close()

        complete_lib = os.path.join(self.simulation_path, self.dat_name + ".lib")  # Criacao do arquivo .lib

        try:
            arquivo_lib = open(complete_lib, 'r+')
            arquivo_lib.close()
            arquivo_lib = open(complete_lib, 'w+')
        except FileNotFoundError:
            arquivo_lib = open(complete_lib, 'w+')

        if self.jmarti:
            if len(self.cond) == 1:
                linha = "KARD"
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=7)
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=10)
                linha += "\n"
                linha += "KARG  1  2\n"
                linha += "KBEG  3  9\n"
                linha += "KEND  8 14\n"
                linha += "KTEX  1  1\n"
            elif len(self.cond) == 2:
                linha = "KARD"
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=7)
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=10)
                linha += Formatter.insertString(string=linha_cond[1], start_position=len(linha), final_position=13)
                linha += Formatter.insertString(string=linha_cond[1], start_position=len(linha), final_position=16)
                linha += "\n"
                linha += "KARG  1  3  2  4\n"
                linha += "KBEG  3  9  3  9\n"
                linha += "KEND  8 14  8 14\n"
                linha += "KTEX  1  1  1  1\n"
            elif len(self.cond) == 3:
                linha = "KARD"
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=7)
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=10)
                linha += Formatter.insertString(string=linha_cond[1], start_position=len(linha), final_position=13)
                linha += Formatter.insertString(string=linha_cond[1], start_position=len(linha), final_position=16)
                linha += Formatter.insertString(string=linha_cond[2], start_position=len(linha), final_position=19)
                linha += Formatter.insertString(string=linha_cond[2], start_position=len(linha), final_position=22)
                linha += "\n"
                linha += "KARG  1  4  2  5  3  6\n"
                linha += "KBEG  3  9  3  9  3  9\n"
                linha += "KEND  8 14  8 14  8 14\n"
                linha += "KTEX  1  1  1  1  1  1\n"
            elif len(self.cond) == 4:
                linha = "KARD"
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=7)
                linha += Formatter.insertString(string=linha_cond[0], start_position=len(linha), final_position=10)
                linha += Formatter.insertString(string=linha_cond[1], start_position=len(linha), final_position=13)
                linha += Formatter.insertString(string=linha_cond[1], start_position=len(linha), final_position=16)
                linha += Formatter.insertString(string=linha_cond[2], start_position=len(linha), final_position=19)
                linha += Formatter.insertString(string=linha_cond[2], start_position=len(linha), final_position=22)
                linha += Formatter.insertString(string=linha_cond[3], start_position=len(linha), final_position=25)
                linha += Formatter.insertString(string=linha_cond[3], start_position=len(linha), final_position=28)
                linha += "\n"
                linha += "KARG  1  5  2  6  3  7  4  8\n"
                linha += "KBEG  3  9  3  9  3  9  3  9\n"
                linha += "KEND  8 14  8 14  8 14  8 14\n"
                linha += "KTEX  1  1  1  1  1  1  1  1\n"
        else:
            if len(self.cond) == 1:
                linha = "KARD  3  3\n"
                linha += "KARG  1  2\n"
                linha += "KBEG  3  9\n"
                linha += "KEND  8 14\n"
                linha += "KTEX  1  1\n"
            elif len(self.cond) == 2:
                linha = "KARD  3  3  4  4\n"
                linha += "KARG  1  3  2  4\n"
                linha += "KBEG  3  9  3  9\n"
                linha += "KEND  8 14  8 14\n"
                linha += "KTEX  1  1  1  1\n"
            elif len(self.cond) == 3:
                linha = "KARD  3  3  4  4  5  5\n"
                linha += "KARG  1  4  2  5  3  6\n"
                linha += "KBEG  3  9  3  9  3  9\n"
                linha += "KEND  8 14  8 14  8 14\n"
                linha += "KTEX  1  1  1  1  1  1\n"
            elif len(self.cond) == 4:
                linha = "KARD  3  3  4  4  5  5  6  6\n"
                linha += "KARG  1  5  2  6  3  7  4  8\n"
                linha += "KBEG  3  9  3  9  3  9  3  9\n"
                linha += "KEND  8 14  8 14  8 14  8 14\n"
                linha += "KTEX  1  1  1  1  1  1  1  1\n"

        linha += "/BRANCH\n"

        name_in = []
        name_out = []

        i = 0
        for l in linhas_sel:
            if self.jmarti:
                if l[0] == "-":
                    name_in.append(l[2:8])
                    name_out.append(l[8:14])
            else:
                if "$VINTAGE, 1" in l:
                    begin = i + 1
                if "$VINTAGE, 0" in l:
                    end = i
            linha += l
            i = i + 1

        linha += "$EOF\n"
        linha += "ARG, "

        if not self.jmarti:
            for i in range(begin, end):
                name_in.append(linhas_sel[i][2:8])
                name_out.append(linhas_sel[i][8:14])

        for name in name_in:
            linha += name + ", "

        for name in name_out:
            if name == name_out[len(name_out) - 1]:
                linha += name + "\n"
            else:
                linha += name + ", "

        arquivo_lib.write(linha)
        arquivo_lib.close()

        if not self.hide_c:
            if self.bus_neg is None:
                self.branch = "C LCC - POS: " + self.bus_pos.name + "\n"
            else:
                self.branch = "C LCC - POS: " + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        linha = "$INCLUDE, " + complete_lib
        for cond in self.cond:
            if len(linha + ", " + cond['bus_in'] + cond["fase"]) <= 77:
                linha += ", " + cond['bus_in'] + cond["fase"]
            else:
                linha += " $$\n"
                self.branch += linha
                linha = "  , " + cond['bus_in'] + cond["fase"]

        for cond in self.cond:
            if len(linha + ", " + cond['bus_out'] + cond["fase"]) <= 77:
                linha += ", " + cond['bus_out'] + cond["fase"]
            else:
                linha += " $$\n"
                self.branch += linha
                linha = "  , " + cond['bus_out'] + cond["fase"]

        self.branch += linha

        if not self.hide_c:
            self.branch += "\nC /LCC"