class Element(object):
    """
    Classe basica de todos os cartoes ATP, contendo as variaveis comuns e necessarias para o tratamento igual desses elementos frente a Classe Cartao.
    """
    def __init__(self):
        """
        Construtor da Classe.
        """
        self.branch = ""
        self.switch = ""
        self.source = ""
        self.output = ""
        self.models = {"header": {"input": "", "output": "", "input_nodes": ""}, "model": {"nome": "", "texto": ""}, "use": {"input": "", "data": "", "output": ""}}
        self.tacs = ""