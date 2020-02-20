from atp.formatter.formatter import Formatter
from atp.element.element import Element
from atp.element.switch.tacsswitch import TACSSwitch
from atp.node.node import Node


class Insulator(Element):

    isol_number = 0

    def __init__(self, bus_pos, bus_neg, tipo, L, CFO, phase_pos="A", phase_neg="A", freq=60, vi=[0 for n in range(25)], ti=[0 for n in range(25)],
                 model_output=False, hide_c=False):

        super().__init__()

        self.bus_pos = bus_pos
        self.phase_pos = phase_pos
        self.bus_neg = bus_neg
        self.phase_neg = phase_neg
        self.tipo = tipo
        self.L = L
        self.CFO = CFO
        self.freq = freq
        self.vi = vi
        self.ti = ti
        self.model_output = model_output
        self.isol_number = Insulator.isol_number
        self.hide_c = hide_c

        Insulator.isol_number += 1

        if not self.hide_c:
            if self.bus_neg is None:
                self.switch = "C ISOLADOR - POS:" + self.bus_pos.name + "\n"
            else:
                self.switch = "C ISOLADOR - POS:" + self.bus_pos.name + " - NEG: " + self.bus_neg.name + "\n"

        self.models["header"]["input"] = []

        models_header_input = "v("
        if phase_pos == "A":
            models_header_input += self.bus_pos.phaseA + ")"
        elif phase_pos == "B":
            models_header_input += self.bus_pos.phaseB + ")"
        elif phase_pos == "C":
            models_header_input += self.bus_pos.phaseC + ")"
        elif phase_pos == "N":
            models_header_input += self.bus_pos.phaseN + ")"
        self.models["header"]["input"].append(models_header_input)

        models_header_input = "v("
        if phase_neg == "A":
            models_header_input += self.bus_neg.phaseA + ")"
        elif phase_neg == "B":
            models_header_input += self.bus_neg.phaseB + ")"
        elif phase_neg == "C":
            models_header_input += self.bus_neg.phaseC + ")"
        elif phase_neg == "N":
            models_header_input += self.bus_neg.phaseN + ")"
        self.models["header"]["input"].append(models_header_input)

        isol_node = Node(self.isol_number, "Isolador", self.phase_pos)

        if phase_pos == "A":
            self.models["header"]["output"] = [isol_node.phaseA]
        elif phase_pos == "B":
            self.models["header"]["output"] = [isol_node.phaseB]
        elif phase_pos == "C":
            self.models["header"]["output"] = [isol_node.phaseC]
        elif phase_pos == "N":
            self.models["header"]["output"] = [isol_node.phaseN]

        self.models["model"]["nome"] = "isolador"
        self.models["model"]["texto"] = "DATA tipo, L, CFO, freq{DFLT:60}, vi[1..25], ti[1..25]\n" \
                                        "INPUT v1,v2\n" \
                                        "OUTPUT CLOSE\n" \
                                        "VAR viso, tempo, valor1, valor2, Eo, DEb, CLOSE, l1, j, DE, dif_e, ie, Khileman\n" \
                                        "DELAY CELLS (DE): 1\n" \
                                        "INIT\n  CLOSE:=0\n" \
                                        "  valor1:=0\n" \
                                        "  valor2:=0\n" \
                                        "  ie:=0\n" \
                                        "  dif_e:=0\n" \
                                        "  integral(dif_e):=0\n" \
                                        "  histdef(ie):=0\n" \
                                        "  histdef(integral(dif_e)):=0\n" \
                                        "ENDINIT\n" \
                                        "EXEC\n" \
                                        "  tempo:=1.2E-6\n" \
                                        "  -- Modelo 1\n" \
                                        "  IF tipo=1 THEN\n" \
                                        "    viso:=(400*L)+((710*L)/sqrt(sqrt((tempo*tempo*tempo))))\n" \
                                        "    IF abs(v1-v2)>viso THEN\n" \
                                        "      CLOSE:= 1\n" \
                                        "    ENDIF\n" \
                                        "\n" \
                                        "  -- Modelo 2: IEEE\n" \
                                        "  ELSIF tipo=2 THEN\n" \
                                        "    valor1:=CFO*1.5\n" \
                                        "    IF v1>valor1 THEN\n" \
                                        "       CLOSE:=1\n" \
                                        "    ENDIF\n" \
                                        "\n" \
                                        "  -- Modelo3:  Hileman\n" \
                                        "  ELSIF tipo=3 THEN\n" \
                                        "    Eo:=0.77*CFO\n" \
                                        "    Khileman:=1.36\n" \
                                        "\n" \
                                        "    FOR j:=1 TO 69 DO\n" \
                                        "      valor1:=valor1*CFO\n" \
                                        "    ENDFOR\n" \
                                        "\n" \
                                        "    valor2:=valor1\n" \
                                        "\n" \
                                        "    FOR l1:=1 TO 25 DO\n" \
                                        "       valor2:=sqrt(valor2)\n" \
                                        "    ENDFOR\n" \
                                        "\n" \
                                        "    DEb:=1.1506*valor2\n" \
                                        "\n" \
                                        "    dif_e:=(v1-Eo)\n" \
                                        "    ie:=integral(dif_e)\n" \
                                        "    DE:=ie-delay(ie,timestep)\n" \
                                        "\n" \
                                        "    IF DE>DEb THEN CLOSE:=1 ENDIF\n" \
                                        "\n" \
                                        "  ENDIF\n" \
                                        "ENDEXEC\n" \
                                        "ENDMODEL\n" \
                                        "\n"

        self.models["use"]["input"] = ["v1", "v2"]
        self.models["use"]["data"] = [
            "tipo:=" + Formatter.insertFloat(number=self.tipo, leng_max=8, start_position=0, final_position=9),
            "L:=" + Formatter.insertFloat(number=self.L, leng_max=8, start_position=0, final_position=9),
            "CFO:=" + Formatter.insertFloat(number=self.CFO, leng_max=8, start_position=0, final_position=9),
            "freq:=" + Formatter.insertFloat(number=self.freq, leng_max=8, start_position=0, final_position=9)
        ]

        for (n, v) in enumerate(self.vi):
            self.models["use"]["data"].append(
                "vi[" + str(n+1) + "]:=" + Formatter.insertFloat(number=v, leng_max=8, start_position=0, final_position=9)
            )

        for (n, t) in enumerate(self.ti):
            self.models["use"]["data"].append(
                "ti[" + str(n+1) + "]:=" + Formatter.insertFloat(number=t, leng_max=8, start_position=0, final_position=9)
            )

        if phase_pos == "A":
            self.models["use"]["output"] = [isol_node.phaseA + ":=CLOSE"]
        elif phase_pos == "B":
            self.models["use"]["output"] = [isol_node.phaseB + ":=CLOSE"]
        elif phase_pos == "C":
            self.models["use"]["output"] = [isol_node.phaseC + ":=CLOSE"]
        elif phase_pos == "N":
            self.models["use"]["output"] = [isol_node.phaseN + ":=CLOSE"]

        self.tacs_switch = TACSSwitch(bus_tacs=isol_node, phase_tacs=self.phase_pos, bus_pos=bus_pos, phase_pos=phase_pos, bus_neg=bus_neg, phase_neg=phase_neg, hide_c=True)

        self.switch += self.tacs_switch.switch

        if not self.hide_c:
            self.switch += "\nC /ISOLADOR"