from datetime import date
from atp.formatter.formatter import Formatter


class ATPCard(object): #Verificar linhas relacionadas a Models, caso continuem nesta mesma classe
    """
    Classe responsavel pela estruturacao e criacao de cartoes Atp.
    A separacao dos metodos desta classe foi baseada na separacao dos tipos de cartoes presentes no Guia Resumido do Atp nas paginas 7 e 8.
    """

    def __init__(self):
        """
        Metodo Construtor da Classe
        """
        self.cartao = ""
        self.gerar_models = False

    def generate_card(self):
        """
        Metodo para inicializacao do cartao Atp.
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        self.cartao += "BEGIN NEW DATA CASE" + "\n"  # Retirado do Topico 5.1 do Guia Resumido do Atp

    def end_card(self):
        """
        Metodo para finalizacao do cartao Atp.
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        if self.gerar_models:
            self.cartao += "BLANK MODELS" + "\n"
        self.cartao += "BLANK BRANCH" + "\n"
        self.cartao += "BLANK SWITCH" + "\n"
        self.cartao += "BLANK SOURCE" + "\n"
        self.cartao += "BLANK OUTPUT" + "\n"
        self.cartao += "BLANK PLOT" + "\n"
        self.cartao += "BEGIN NEW DATA CASE" + "\n"
        self.cartao += "BLANK"

    def mark_surge_arrester_position(self):
        """
        Classe que posiciona um comentario na regiao do cartao onde os para-raios devem ser inseridos.
        """
        self.cartao += "C INSERIR PARA RAIOS AQUI" + "\n"

    def mark_surge_position(self):
        """
        Classe que posiciona um comentario na regiao do cartao onde os raios devem ser inseridos.
        """
        self.cartao += "C INSERIR RAIOS AQUI" + "\n"

    def generate_header(self):
        """
        Metodo para a criacao do cabecalho do cartao Atp com comentarios contendo informacoes sobre data de geracao e individuo gerador.
        Metodo opcional visto que os comentarios serao ignorados pelo Atp.
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        cabecalho = "C --------------------------------------------------------" + "\n"  # Estrutura do comentário retirada do Guia Resumido do Atp na página 7
        cabecalho += "C Gerado por GRUPO EQUATORIAL em " + str(date.today().day) + "/" + str(date.today().month) + "/" + str(
            date.today().year) + "\n"
        cabecalho += "C CEAMAZON" + "\n"
        cabecalho += "C 2018-2019" + "\n"
        cabecalho += "C --------------------------------------------------------" + "\n"
        self.cartao += cabecalho

    def generate_miscellaneous_float(self, deltat, tmax, xopt, copt, epsiln):
        """
        Metodo para a criacao da area de dados miscelaneos float do cartao Atp.
        Todos os argumentos são do tipo float.
        :param deltat: Intervalo de integracao em segundos (passo)
        :param tmax: Tempo total de simulacao em segundos
        :param xopt: Opcoes de Indutancias e Reatancias Indutivas, ver Topico 5.2 do Guia Resumido do Atp
        :param copt: Opcoes de Capacitancias e Reatancias Capacitivas, ver Topico 5.2 do Guia Resumido do Atp
        :param epsiln: Tolerancia proxima de zero para testar singularidade de matrizes
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        miscfloat = "C  dT  >< Tmax >< Xopt >< Copt ><Epsiln>" + "\n"  # Retirado do Topico 5.2 do Guia Resumido do Atp
        linha = Formatter.insertFloat(number=deltat, leng_max=8, start_position=0, final_position=8)
        linha += Formatter.insertFloat(number=tmax, leng_max=8, start_position=len(linha), final_position=16)
        linha += Formatter.insertFloat(number=xopt, leng_max=8, start_position=len(linha), final_position=24)
        linha += Formatter.insertFloat(number=copt, leng_max=8, start_position=len(linha), final_position=32)
        linha += Formatter.insertFloat(number=epsiln, leng_max=8, start_position=len(linha), final_position=40)
        miscfloat += linha + "\n"
        self.cartao += miscfloat

    def generate_miscellaneous_int(self, iout, iplot, idoubl, kssout, maxout, ipun, mensav, icat, nenerg, iprsup):
        """
        Metodo para a criacao da area de dados miscelaneos inteiros do cartao Atp.
        Todos os argumentos são do tipo inteiro.
        :param iout: Quantidade de pontos de impressao, ver Topico 5.3 do Guia Resumido do Atp
        :param iplot: Quantidade de pontos para graficos
        :param idoubl: flag para impressao da tabela conexoes na rede
        :param kssout: flag para impressao dos fluxos nos equivalentes_ramos da rede
        :param maxout: flag para impressao dos valores maximos das variaveis
        :param ipun: flag para as mudanças de frequencia de impressao
        :param mensav: flag para controle de gravacao da memoria do Atp em disco
        :param icat: flag para gravacao permanente de pontos para posterior plotagem
        :param nenerg: flag do numero de energizacao em casos de chaves estatisticas ou sistematicas
        :param iprsup: flag de controle de saída da impressão por parâmetros do arquivo STARTUP
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        iout = iout if iout > 0 and iout <= 57599 else 57599  # Limites do parametro iout. Obtido por comparacao de cartoes gerados pelo ATPDraw.
        linha = Formatter.insertInteger(number=iout, leng_max=8, start_position=0, final_position=8, blank=False) # Retirado do Topico 5.3 do Guia Resumido do Atp
        linha += Formatter.insertInteger(number=iplot, leng_max=8, start_position=len(linha), final_position=16, blank=False)
        linha += Formatter.insertInteger(number=idoubl, leng_max=8, start_position=len(linha), final_position=24, blank=False)
        linha += Formatter.insertInteger(number=kssout, leng_max=8, start_position=len(linha), final_position=32, blank=False)
        linha += Formatter.insertInteger(number=maxout, leng_max=8, start_position=len(linha), final_position=40, blank=False)
        linha += Formatter.insertInteger(number=ipun, leng_max=8, start_position=len(linha), final_position=48, blank=False)
        linha += Formatter.insertInteger(number=mensav, leng_max=8, start_position=len(linha), final_position=56, blank=False)
        linha += Formatter.insertInteger(number=icat, leng_max=8, start_position=len(linha), final_position=64, blank=False)
        linha += Formatter.insertInteger(number=nenerg, leng_max=8, start_position=len(linha), final_position=72, blank=False)
        linha += Formatter.insertInteger(number=iprsup, leng_max=8, start_position=len(linha), final_position=80)
        miscint = linha + "\n"
        miscint += "C        1         2         3         4         5         6         7         8" + "\n"  # Linha para auxiliar a visualizacao das colunas, visto que os dados precisam estar em colunas especificas do cartao Atp
        miscint += "C 345678901234567890123456789012345678901234567890123456789012345678901234567890" + "\n"
        self.cartao += miscint

    def generate_models(self, elements=[]):
        """
        Metodo para a criacao da area Models do cartao Atp.
        Exemplo:
        >> from Element.Mixed.Isolador import Isolador # Importando a Classe Isolador que herda de Element
        >> isolador1 = Isolador(...) # Isolador instanciado
        >> isolador = [isolador1]
        >> cartao.gerarModels(isolador) # Variavel cartao e uma instancia da Classe Cartao
        :param elements: Lista com todos os elementos das Classes do Pacote Isolador ou Mixed e cuja Classe Pai e Element
        :type elements: list
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        self.gerar_models = False
        models_elements = []
        for e in elements:
            if e.models != {"header": {"input": "", "output": "", "input_nodes": ""}, "model": {"nome": "", "texto": ""}, "use": {"input": "", "data": "", "output": ""}}:
                self.gerar_models = True
                models_elements.append(e)

        if self.gerar_models:
            models = "/MODELS" + "\n"
            models += "MODELS" + "\n"

            models += "INPUT" + "\n"
            for e in models_elements:
                if e.models["model"]["nome"] == "isolador":
                    indice = "I"
                    e.models["header"]["input_nodes"] = []
                    for i in e.models["header"]["input"]:
                        e.models["header"]["input_nodes"].append(indice + "{0:0=4d}".format(e.isol_number) + str(e.models["header"]["input"].index(i))) #VERIFICAR
                        models += indice + "{0:0=4d}".format(e.isol_number) + str(e.models["header"]["input"].index(i)) + " {" + i + "}" + "\n" #VERIFICAR
                else:
                    pass # Adicionar outros models aqui

            models += "OUTPUT" + "\n"
            for e in models_elements:
                if e.models["model"]["nome"] == "isolador":
                    for i in e.models["header"]["output"]:
                        models += "  " + Formatter.formatString("I", i, "O") + "\n" #VERIFICAR FORMATTER
                else:
                    pass # Adicionar outros models aqui

            for e in models_elements:
                if e.models["model"]["nome"] == "isolador":
                    models += "MODEL " + e.models["model"]["nome"] + str(e.isol_number) + "\n"
                    models += e.models["model"]["texto"] + "\n"
                else:
                    pass  # Adicionar outros models aqui

            for e in models_elements:
                if e.models["model"]["nome"] == "isolador":
                    models += "USE " + e.models["model"]["nome"] + str(e.isol_number) + " AS I" + str(e.isol_number) + "\n"
                    models += "INPUT" + "\n"
                    for i in e.models["use"]["input"]:
                        models += "  " + i + ":= " + e.models["header"]["input_nodes"][e.models["use"]["input"].index(i)] + "\n"
                    models += "DATA" + "\n"
                    for i in e.models["use"]["data"]:
                        models += "  " + i + "\n"
                    models += "OUTPUT" + "\n"
                    for i in e.models["use"]["output"]:
                        models += "  " + i + "\n"
                    models += "ENDUSE" + "\n"
                else:
                    pass  # Adicionar outros models aqui

            alr_record = False
            for e in models_elements:
                if e.model_output:
                    if not alr_record:
                        models += "RECORD" + "\n"
                        alr_record = True
                    if e.models["model"]["nome"] == "isolador":
                        models += "  I" + str(e.isol_number) + ".CLOSE AS CI" + str(e.isol_number) + "\n"
                    else:
                        pass  # Adicionar outros models aqui

            models += "ENDMODELS" + "\n"

            self.cartao += models

    def generate_branch(self, elements=[]):
        """
        Metodo para a criacao da area Branch do cartao Atp.
        Exemplo:
        >> from Element.Branch.RLC import RLC # Importando a Classe RLC que herda de Element
        >> branch1 = RLC(10, 0, 0, 1, 2, output=1)
        >> branch2 = RLC(0, 0, 1, 2, output=2)
        >> branch_list = [branch1, branch2]
        >> cartao.gerarBranch(branch_list) # Variavel cartao e uma instancia da Classe Cartao
        :param elements: Lista com todos os elementos das Classes do Pacote Branch e cuja Classe Pai e Element
        :type elements: list
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        branch = "/BRANCH" + "\n"
        branch += "C < n1 >< n2 ><ref1><ref2>< R  >< L  >< C  >" + "\n"
        branch += "C < n1 >< n2 ><ref1><ref2>< R  >< A  >< B  ><Leng><><>0" + "\n"
        for e in elements:
            if e.branch != "":
                branch += e.branch + "\n"
        self.cartao += branch

    def generate_equivalent(self, equivalent=[]):
        branch = "C EQUIVALENTES\n"
        for e in equivalent:
            if e.branch != "":
                branch += e.branch + "\n"
        branch += "C /EQUIVALENTES\n"
        self.cartao += branch

    def generate_switch(self, elements=[]):
        """
        Metodo para a criacao da area Switch do cartao Atp.
        Exemplo:
        >> from Element.Switch.TimeControlled import TimeControlled # Importando a Classe TimeControlled que herda de Element
        >> switch1 = TimeControlled(1,2,-1,1)
        >> switch_list = [switch1]
        >> cartao.gerarSwitch(switch_list) # Variavel cartao e uma instancia da Classe Cartao
        :param elements: Lista com todos os elementos das Classes do Pacote Switch e cuja Classe Pai e Element
        :type elements: list
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        switch = "/SWITCH" + "\n"
        switch += "C < n 1>< n 2>< Tclose ><Top/Tde ><   Ie   ><Vf/CLOP ><  type  >" + "\n"
        for e in elements:
            if e.switch != "":
                switch += e.switch + "\n"
        self.cartao += switch

    def generate_source(self, elements=[]):
        """
        Metodo para a criacao da area Source do cartao Atp.
        Exemplo:
        >> from Element.Source.VoltageDC import VoltageDC # Importando a Classe VoltageDC que herda de Element
        >> source1 = VoltageDC(1, 10, -1, 1)
        >> source2 = VoltageDC(2, 10, -1, 1)
        >> source_list = [source1, source2]
        >> cartao.gerarSource(source_list) # Variavel cartao e uma instancia da Classe Cartao
        :param elements: Lista com todos os elementos das Classes do Pacote Source e cuja Classe Pai e Element
        :type elements: list
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        source = "/SOURCE" + "\n"
        source += "C < n 1><>< Ampl.  >< Freq.  ><Phase/T0><   A1   ><   T1   >< TSTART >< TSTOP  >" + "\n"
        for e in elements:
            if e.source != "":
                source += e.source + "\n"
        self.cartao += source

    def generate_output(self, elements=[]):
        """
        Metodo para a criacao da area Output do cartao Atp.
        Exemplo:
        >> from Element.Output.VoltageProbe import VoltageProbe # Importando a Classe VoltageProbe que herda de Element
        >> voltageprobe = VoltageProbe([bus1, bus2, ...])
        >> cartao.gerarOutput(voltageprobe) # Variavel cartao e uma instancia da Classe Cartao
        :param elements: Lista com todos os elementos das Classes do Pacote Output e cuja Classe Pai e Element
        :type elements: list
        :return: Nao retorna valor, mas atualiza a variavel da instancia cartao
        """
        output = "/OUTPUT" + "\n"
        output_list = []
        for e in elements:
            if e.output != "":
                output_list.extend(e.output.split("-"))
        output_separate_lists = []
        for position in range(0, len(output_list), 13):
            output_separate_lists.append(output_list[position:position+13])
        for (n, output_row) in enumerate(output_separate_lists):
            output += "  " + "".join(output_row)
            if not n == len(output_separate_lists):
                output += "\n"
        self.cartao += output