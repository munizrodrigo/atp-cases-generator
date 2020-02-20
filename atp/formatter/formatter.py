class Formatter(object):
    """
    Classe responsavel pela formatacao numerica de acordo com o Guia de Formatacao FORTRAN.
    """
    @staticmethod
    def formatFloat(number, leng_max, blank=True):
        """
        Converte um numero do tipo float para o formato de string E e F utilizado por alguns dos cartoes ATP com base no Guia de Formatacao FORTRAN.
        :param number: Numero a ser convertido
        :type number: int
        :param leng_max: Comprimento maximo da string
        :type leng_max: int
        :param blank: Valor booleano que indica se o valor 0 sera representado por um espaco em branco
        :type blank: bool
        :return: String padronizada FORTRAN para numeros inteiros
        :rtype: basestring
        """
        strdec = ""
        strexp = ""
        erro_dec = 0
        erro_exp = 0
        if number == 0 and blank:
            return ""
        else:
            number = float(number)
            force_dec = False
            force_expo = False

            try:
                (integ, dec) = str(number).replace("-", "").split(".")
                strdec = str(round(number, len(dec) - (len(str(integ + "." + dec)) - leng_max)))
                float_dec = float(strdec)
                erro_dec = abs(float_dec - number)
            except:
                force_expo = True

            try:
                number_expo = "{:E}".format(number).replace("E+0", "E").replace("E-0", "E-").replace("E+", "E")
                coef_expo = number_expo.split("E")[0]
                (integ_expo, dec_expo) = coef_expo.replace("-", "").split(".")
                strexp = (str(round(float(coef_expo), len(dec_expo) - (len(number_expo) - leng_max))) + number_expo[number_expo.find("E"):]).replace(".0E", ".E")
                float_exp = float(strexp)
                erro_exp = abs(float_exp - number)
            except:
                force_dec = True

            if force_dec:
                if len(strdec) <= leng_max:
                    return strdec
                else:
                    raise ValueError("Number exceeds maximum length")

            if force_expo:
                if len(strexp) <= leng_max:
                    return strexp
                else:
                    raise ValueError("Number exceeds maximum length")

            if len(strdec) <= leng_max and len(strexp) <= leng_max:
                if erro_dec <= erro_exp:
                    return strdec
                else:
                    return strexp
            elif len(strdec) <= leng_max:
                return strdec
            elif len(strexp) <= leng_max:
                return strexp
            else:
                raise ValueError("Number exceeds maximum length")

    @staticmethod
    def formatInteger(number, leng_max, blank=True):
        """
        Converte um numero do tipo int para o formato de string I utilizado por alguns dos cartoes ATP com base no Guia de Formatacao FORTRAN.
        :param number: Numero a ser convertido
        :type number: int
        :param leng_max: Comprimento maximo da string
        :type leng_max: int
        :param blank: Valor booleano que indica se o valor 0 sera representado por um espaco em branco
        :type blank: bool
        :return: String padronizada FORTRAN para numeros inteiros
        :rtype: basestring
        """
        if Formatter.isInt(number):
            if number == 0:
                if blank:
                    strval = ""
                else:
                    strval = "0"
            else:
                strval = str(number)
            if strval[-2:] == ".0":
                strval = strval[0:-2]
            if len(strval) <= leng_max:
                return strval
            else:
                raise ValueError("Number exceeds maximum length")
        else:
            raise ValueError("Number is not int")

    @staticmethod
    def formatString(prefix, radical, suffix):
        """
        Cria uma string apropriada para uso por alguns dos cartoes ATP com base no Guia de Formatacao FORTRAN. Todas as strings sao compostas por seis posicoes. A primeira posicao corresponde a variavel prefix e identifica o tipo do no. As posicoes de 2 a 5 correspondem a um numero identificador do no codificado em hexadecimal, oriundo da variavel radical. A posicao 6 corresponde a variavel suffix, podendo indicar a fase do no ou o numero do no interno. Para mais detalhes, consultar tabela a seguir.
        < Posicao 1> < Posicoes de 2 a 5 > <  Posicao 6  >
        <     0    > <      2 3 4 5      > <      6      >
        <     B    > <Numero Hexadecimal > <Fase(A,B,C,N)>
        <     X    > <Numero Hexadecimal > <Fase(A,B,C,N)>
        <     P    > <Numero Hexadecimal > < No Interno  >
        <     T    > <Numero Hexadecimal > < No Interno  >
        <     G    > <Numero Hexadecimal > < No Interno  >
        <     H    > <Numero Hexadecimal > < No Interno  >
        <     Z    > <Numero Hexadecimal > < No Interno  >
        <     S    > <Numero Hexadecimal > < No Interno  >
        :param prefix: Sigla Inicial da Barra
        :type prefix: basestring
        :param radical: Numero identificador
        :type radical: int
        :param suffix: Fase do Elemento ou No interno
        :type suffix: basestring ou int
        :return: Valor convertido para o formato string
        :rtype: basestring
        """
        string = ""
        if Formatter.isStr(prefix):
            if len(prefix) == 1:
                string += prefix
            else:
                raise ValueError("String length incompatible")
        else:
            raise ValueError("Value is not string")
        if Formatter.isInt(radical):
            if len("{0:0=4X}".format(radical)) == 4:
                string += "{0:0=4X}".format(radical)
            else:
                raise ValueError("Number exceeds maximum length")
        else:
            raise ValueError("Number is not int")
        if Formatter.isInt(suffix):
            if len("{0:0=1X}".format(suffix)) == 1:
                string += "{0:0=1X}".format(suffix)
            else:
                raise ValueError("Number exceeds maximum length")
        elif Formatter.isStr(suffix):
            if len(suffix) == 1:
                string += suffix
            else:
                raise ValueError("String length incompatible")
        else:
            raise ValueError
        if len(string) == 6:
            return string
        else:
            raise ValueError("String length incompatible")

    @staticmethod
    def insertFloat(number, leng_max, start_position, final_position, blank=True):
        string = Formatter.formatFloat(number=number, leng_max=leng_max, blank=blank)
        string = Formatter.calcSpace(string=string, start_position=start_position, final_position=final_position) + string
        return string

    @staticmethod
    def insertInteger(number, leng_max, start_position, final_position, blank=True):
        string = Formatter.formatInteger(number=number, leng_max=leng_max, blank=blank)
        string = Formatter.calcSpace(string=string, start_position=start_position, final_position=final_position) + string
        return string

    @staticmethod
    def insertString(string, start_position, final_position):
        string = Formatter.calcSpace(string=string, start_position=start_position, final_position=final_position) + string
        return string

    @staticmethod
    def calcSpace(string, start_position, final_position):
        """
        Metodo para o calculo do numero de espacos necessarios para o correto posicionamento dos dados nas colunas para a execucao no ATP e geracao de uma string com espacos definidos por esse calculo.
        :param string: String com o dado a ser posicionado no cartao
        :type string: basestring
        :param final_position: Ultima posicao a ser ocupada pelo dado no cartao ATP, consultar o Guia Resumido do ATP ou o ATp RuleBook para o dado em questao
        :type final_position: int
        :param start_position: Ultima posicao ja ocupada na linha onde o dado sera posicionado
        :type start_position: int
        :return: String com o numero de espacos correspondente ao correto posicionamento
        :rtype: basestring
        """
        tam = final_position - len(string) - start_position
        esp = ""
        for i in range(0, tam):
            esp = esp + " "
        return esp

    @staticmethod
    def isInt(number):
        """
        Verifica se o numero fornecido e do tipo inteiro.
        :param number: Numero a ser verificado
        :type number: int ou float
        :return: Booleano True se o numero e inteiro, False caso contrário
        :rtype: bool
        """
        try:
            if type(number) == int:
                return True
            else:
                if number.is_integer():
                    return True
                else:
                    return False
        except:
            return False

    @staticmethod
    def isStr(value):
        """
        Verifica se o valor passado e do tipo string.
        :param value: Valor a ser verificado
        :type value: basestring
        :return: Booleano True se o valor e uma String, False caso contrário
        :rtype: bool
        """
        return isinstance(value, str)