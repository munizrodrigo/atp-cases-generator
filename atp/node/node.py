from atp.formatter.formatter import Formatter


class Node(object):

    n_bus = 0
    n_other = 0
    n_surgearrester = 0
    n_trafosat = 0
    n_ground = 0
    n_hybridtrafo = 0
    n_surgeimpedance = 0
    n_insulator = 0

    type_letter = \
        (
            ("Poste", "B"),
            ("Outro", "X"),
            ("Para-Raio", "P"),
            ("Transformador Saturavel", "T"),
            ("Terra", "G"),
            ("Transformador Hibrido", "H"),
            ("Impedancia de Surto", "Z"),
            ("Isolador", "S")
        )

    def __init__(self, name, type, sequence="ABCN"):
        self.name = name
        self.type = type
        self.sequence = sequence

        self.prefix = list(filter(lambda t: t[0]==type, Node.type_letter))[0][1]

        if self.type == "Poste":
            self.number = int(Node.n_bus)
            Node.n_bus += 1
        elif self.type == "Outro":
            self.number = int(Node.n_other)
            Node.n_other += 1
        elif self.type == "Para-Raio":
            self.number = int(Node.n_surgearrester)
            Node.n_surgearrester += 1
        elif self.type == "Transformador Saturavel":
            self.number = int(Node.n_trafosat)
            Node.n_trafosat += 1
        elif self.type == "Terra":
            self.number = int(Node.n_ground)
            Node.n_ground += 1
        elif self.type == "Transformador Hibrido":
            self.number = int(Node.n_hybridtrafo)
            Node.n_hybridtrafo += 1
        elif self.type == "Impedancia de Surto":
            self.number = int(Node.n_surgeimpedance)
            Node.n_surgeimpedance += 1
        elif self.type == "Isolador":
            self.number = int(Node.n_insulator)
            Node.n_insulator += 1
        else:
            raise ValueError("Incorrect type")

        if "A" in self.sequence:
            self.phaseA = Formatter.formatString(prefix=self.prefix, radical=self.number, suffix="A")
        else:
            self.phaseA = None

        if "B" in self.sequence:
            self.phaseB = Formatter.formatString(prefix=self.prefix, radical=self.number, suffix="B")
        else:
            self.phaseB = None

        if "C" in self.sequence:
            self.phaseC = Formatter.formatString(prefix=self.prefix, radical=self.number, suffix="C")
        else:
            self.phaseC = None

        if "N" in self.sequence:
            self.phaseN = Formatter.formatString(prefix=self.prefix, radical=self.number, suffix="N")
        else:
            self.phaseN = None

        self.node = Formatter.formatString(prefix=self.prefix, radical=self.number, suffix="0")[0:-1]