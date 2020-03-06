from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.node.node import Node

class VoltageProbe(Element):
    """
    Classe responsavel pela adição de probes de tensão.
    """
    def __init__(self, bus):
        """
        Metodo Construtor da Classe.
        Baseado no modelo encontrado no topico 5.7.1 do Guia Resumido no Atp.
        :param bus: Nó eletrico onde se quer a especificacao da tensao.
        type bus: Node
        """
        super().__init__()
        self.bus = bus

        if self.bus.phaseA is not None:
            self.output += self.bus.phaseA + "-"

        if self.bus.phaseB is not None:
            self.output += self.bus.phaseB + "-"

        if self.bus.phaseC is not None:
            self.output += self.bus.phaseC + "-"

        if self.bus.phaseN is not None:
            self.output += self.bus.phaseN + "-"

        self.output = self.output[:-1]