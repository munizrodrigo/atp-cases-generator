import json
import math
import os

from os.path import abspath, join, dirname

from copy import deepcopy as copy

from atp.node.node import Node
from atp.element.source.voltageac_3ph import VoltageAC_3ph
from atp.element.source.voltageac import VoltageAC
from atp.element.source.currentheidler import CurrentHEIDLER
from atp.element.branch.rlc3phY import RLC_3ph_Y
from atp.element.branch.rlc import RLC
from atp.element.branch.lcc import LCC
from atp.element.branch.surgearresterieee import SurgeArresterIEEE
from atp.element.branch.ground import Ground
from atp.element.output.voltageprobe import VoltageProbe
from atp.atpcard.card import ATPCard


def create_atp_file(atp_card, folder_path, atp_filename):
    if not atp_filename[-4:] == ".atp":
        atp_filename += ".atp"
    atp_file = open(os.path.join(folder_path, atp_filename), 'w+')
    atp_file.write(atp_card)
    atp_file.close()


class CaseGenerator(object):
    def __init__(self, feeder):
        self.feeder = feeder
        self.atp_card_base = ATPCard()
        self.atp_card_mod_surge = None
        self.bus = []
        self.line = []
        self.source = []
        self.load = []
        self.capacitor = []
        self.equivalent = []
        self.output = []
        self.elements = []
        self.surge = []
        self.surge_arrester = []
        self.surge_arrester_ground = []

    def generate_base_card(self, simulation_path, execution_cmd, create_file=True, overwrite_line=True, deltat=1e-8,
                           tmax=0.01):
        self.generate_bus()

        self.generate_elements()

        self.generate_line(
            simulation_path=simulation_path,
            execution_cmd=execution_cmd,
            overwrite=overwrite_line
        )

        self.generate_output(
            list_bus_obj=self.bus
        )

        self.generate_equivalent()

        self.generate_surge_arrester()

        self.elements = (
                self.source
                + self.capacitor
                + self.load
                + self.line
                + self.surge_arrester
                + self.surge_arrester_ground
                + self.output
        )

        self.atp_card_base.generate_card()
        self.atp_card_base.generate_header()
        self.atp_card_base.generate_miscellaneous_float(
            deltat=deltat,
            tmax=tmax,
            xopt=0,
            copt=0,
            epsiln=0
        )
        self.atp_card_base.generate_miscellaneous_int(
            iout=34464,
            iplot=1,
            idoubl=1,
            kssout=1,
            maxout=1,
            ipun=0,
            mensav=0,
            icat=1,
            nenerg=0,
            iprsup=0
        )
        self.atp_card_base.generate_models(elements=self.elements)
        self.atp_card_base.generate_branch(elements=self.elements)
        self.atp_card_base.generate_equivalent(equivalent=self.equivalent)
        self.atp_card_base.mark_surge_arrester_position()
        self.atp_card_base.generate_switch(elements=self.elements)
        self.atp_card_base.generate_source(elements=self.elements)
        self.atp_card_base.mark_surge_position()
        self.atp_card_base.generate_output(elements=self.elements)
        self.atp_card_base.end_card()
        if create_file:
            create_atp_file(
                atp_card=self.atp_card_base.cartao,
                folder_path=simulation_path,
                atp_filename="base_feeder"
            )

        self.generate_surge()

        if create_file:
            create_atp_file(
                atp_card=self.atp_card_mod_surge.cartao,
                folder_path=simulation_path,
                atp_filename="surge_feeder"
            )

    def generate_bus(self):
        for bus_name in sorted(self.feeder.graph.nodes()):
            bus = self.feeder.graph.nodes[bus_name]
            if bus["area"]:
                self.bus.append(
                    Node(
                        name=bus_name,
                        type="Poste",
                        sequence=bus["phase"]
                    )
                )

    def generate_elements(self):
        for bus_name in sorted(self.feeder.graph.nodes()):
            bus = self.feeder.graph.nodes[bus_name]
            if "source" in bus:
                for (code, source) in bus["source"].items():
                    if bus["area"]:
                        bus_obj_source = list(
                            filter(
                                lambda b: b.name == bus_name,
                                self.bus
                            )
                        )[0]

                        phases = []
                        for ph in bus["phase"]:
                            if ph == "A":
                                phases.append(0.0)
                            elif ph == "B":
                                phases.append(-120.0)
                            elif ph == "C":
                                phases.append(120.0)

                        if len(phases) == 1:
                            self.source.append(
                                VoltageAC(
                                    bus_pos=bus_obj_source,
                                    phase_pos=bus["phase"][0],
                                    phase=phases[0],
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )

                        elif len(phases) == 2:
                            self.source.append(
                                VoltageAC(
                                    bus_pos=bus_obj_source,
                                    phase_pos=bus["phase"][0],
                                    phase=phases[0],
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )
                            self.source.append(
                                VoltageAC(
                                    bus_pos=bus_obj_source,
                                    phase_pos=bus["phase"][1],
                                    phase=phases[1],
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )

                        else:
                            self.source.append(
                                VoltageAC_3ph(
                                    bus_pos=bus_obj_source,
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )

                    else:
                        eq_bus_pos = None
                        for (n, graph) in enumerate(self.feeder.equivalent_graphs):
                            if bus_name in graph.nodes():
                                eq_bus_pos = int(n)
                                break
                        bus_frontier_name = self.feeder.bus_frontier[eq_bus_pos]
                        z_eq = self.feeder.equivalent_values[eq_bus_pos]

                        bus_obj_frontier = list(
                            filter(
                                lambda b: b.name == bus_frontier_name,
                                self.bus
                            )
                        )[0]

                        self.bus.append(
                            Node(
                                name="sourcebus_" + code,
                                type="Outro",
                                sequence=bus_obj_frontier.sequence
                            )
                        )

                        bus_obj_source = list(
                            filter(
                                lambda b: b.name == "sourcebus_" + code,
                                self.bus
                            )
                        )[0]

                        phases = []
                        for ph in bus_obj_source.sequence:
                            if ph == "A":
                                phases.append(0.0)
                            elif ph == "B":
                                phases.append(-120.0)
                            elif ph == "C":
                                phases.append(120.0)

                        if len(phases) == 1:
                            self.source.append(
                                VoltageAC(
                                    bus_pos=bus_obj_source,
                                    phase_pos=bus_obj_source.sequence[0],
                                    phase=phases[0],
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )

                        elif len(phases) == 2:
                            self.source.append(
                                VoltageAC(
                                    bus_pos=bus_obj_source,
                                    phase_pos=bus_obj_source.sequence[0],
                                    phase=phases[0],
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )
                            self.source.append(
                                VoltageAC(
                                    bus_pos=bus_obj_source,
                                    phase_pos=bus_obj_source.sequence[1],
                                    phase=phases[1],
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )

                        else:
                            self.source.append(
                                VoltageAC_3ph(
                                    bus_pos=bus_obj_source,
                                    amp=source["vrms"] * math.sqrt(2) / math.sqrt(3)
                                )
                            )
                        for (phase, z) in z_eq.items():
                            self.line.append(
                                RLC(
                                    R=z.R,
                                    L=z.L if z.X > 0.0 else 0.0,
                                    C=z.C if z.X < 0.0 else 0.0,
                                    bus_pos=bus_obj_source,
                                    phase_pos=phase,
                                    bus_neg=bus_obj_frontier,
                                    phase_neg=phase
                                )
                            )

            if "capacitor" in bus:
                dump_resistance = 0.001
                for (code, capacitor) in bus["capacitor"].items():
                    if bus["area"]:
                        bus_obj = list(
                            filter(
                                lambda b: b.name == bus_name,
                                self.bus
                            )
                        )[0]

                        if bus_obj.sequence == "ABC":
                            self.capacitor.append(
                                RLC_3ph_Y(
                                    R1=dump_resistance,
                                    L1=0,
                                    C1=capacitor["ca"] * 1e6,
                                    R2=dump_resistance,
                                    L2=0,
                                    C2=capacitor["cb"] * 1e6,
                                    R3=dump_resistance,
                                    L3=0,
                                    C3=capacitor["cc"] * 1e6,
                                    bus_pos=bus_obj,
                                    vintage=1
                                )
                            )
                        else:
                            if "A" in bus_obj.sequence:
                                self.capacitor.append(
                                    RLC(
                                        R=dump_resistance,
                                        L=0,
                                        C=capacitor["ca"] * 1e6,
                                        bus_pos=bus_obj,
                                        phase_pos="A"
                                    )
                                )
                            if "B" in bus_obj.sequence:
                                self.capacitor.append(
                                    RLC(
                                        R=dump_resistance,
                                        L=0,
                                        C=capacitor["cb"] * 1e6,
                                        bus_pos=bus_obj,
                                        phase_pos="B"
                                    )
                                )
                            if "C" in bus_obj.sequence:
                                self.capacitor.append(
                                    RLC(
                                        R=dump_resistance,
                                        L=0,
                                        C=capacitor["cc"] * 1e6,
                                        bus_pos=bus_obj,
                                        phase_pos="C"
                                    )
                                )

            if "load" in bus:
                for (code, load) in bus["load"].items():
                    if bus["area"]:
                        bus_obj = list(
                            filter(
                                lambda b: b.name == bus_name,
                                self.bus
                            )
                        )[0]

                        if bus_obj.sequence == "ABC":
                            self.load.append(
                                RLC_3ph_Y(
                                    R1=load["ra"],
                                    L1=load["la"] * 1e3,
                                    C1=0.0,
                                    R2=load["rb"],
                                    L2=load["lb"] * 1e3,
                                    C2=0.0,
                                    R3=load["rc"],
                                    L3=load["lc"] * 1e3,
                                    C3=0.0,
                                    bus_pos=bus_obj
                                )
                            )
                        else:
                            if "A" in bus_obj.sequence and (load["ra"] != 0.0 or load["la"] != 0.0):
                                self.capacitor.append(
                                    RLC(
                                        R=load["ra"],
                                        L=load["la"] * 1e3,
                                        C=0.0,
                                        bus_pos=bus_obj,
                                        phase_pos="A"
                                    )
                                )
                            if "B" in bus_obj.sequence and (load["rb"] != 0.0 or load["lb"] != 0.0):
                                self.capacitor.append(
                                    RLC(
                                        R=load["rb"],
                                        L=load["lb"] * 1e3,
                                        C=0.0,
                                        bus_pos=bus_obj,
                                        phase_pos="B"
                                    )
                                )
                            if "C" in bus_obj.sequence and (load["rc"] != 0.0 or load["lc"] != 0.0):
                                self.capacitor.append(
                                    RLC(
                                        R=load["rc"],
                                        L=load["lc"] * 1e3,
                                        C=0.0,
                                        bus_pos=bus_obj,
                                        phase_pos="C"
                                    )
                                )

    def generate_line(self, simulation_path, execution_cmd, overwrite=False, min_lim_km=0.01):
        for (edge_from, edge_to) in self.feeder.graph.edges():
            branch = self.feeder.graph[edge_from][edge_to]
            if branch["area"]:
                bus_neg = list(
                    filter(
                        lambda b: b.name == edge_from,
                        self.bus
                    )
                )[0]
                bus_pos = list(
                    filter(
                        lambda b: b.name == edge_to,
                        self.bus
                    )
                )[0]

                length_line = float(branch["length"] / 1e3)

                # Correct if the line is smaller than min_lim_km
                if length_line < min_lim_km:
                    length_line = float(min_lim_km)

                sequence = branch["phase"]
                cond_type = next(iter(branch["cable"].keys()))
                struct_type = next(iter(branch["pole"].keys()))
                cond = []
                for (n, phase) in enumerate(sequence):
                    struct_type_phase = {
                        "phase": branch["pole"][struct_type]["phase"][n],
                        "distance": branch["pole"][struct_type]["distance"][n],
                        "height": branch["pole"][struct_type]["height"][n],
                        "sag": branch["pole"][struct_type]["sag"][n],
                    }
                    if branch["cable"][cond_type]["ri"] == 0.0:
                        skin = 0.5
                    else:
                        skin = branch["cable"][cond_type]["ri"] / branch["cable"][cond_type]["ro"]
                    cond_phase = {
                        "ip": n + 1,
                        "skin": skin,
                        "resis": branch["cable"][cond_type]["resistivity"] * 1e3,
                        "ix": 4,
                        "react": 0,
                        "diam": 2 * branch["cable"][cond_type]["ro"] * 1e2,
                        "horiz": struct_type_phase["distance"],
                        "vtower": struct_type_phase["height"],
                        "vmid": struct_type_phase["sag"],
                        "bus_in": bus_neg.node,
                        "bus_out": bus_pos.node,
                        "fase": phase
                    }
                    cond.append(cond_phase)
                lcc = LCC(
                    cond=cond,
                    dist=length_line,
                    bus_pos=bus_pos,
                    bus_neg=bus_neg,
                    dat_name=bus_neg.node.lower() + "_" + bus_pos.node.lower(),
                    rho=branch["rho"],
                    simulation_path=simulation_path,
                    run_cmd=execution_cmd,
                    overwrite=overwrite
                )
                self.line.append(lcc)

    def generate_output(self, list_bus_obj):
        for bus in list_bus_obj:
            self.output.append(VoltageProbe(bus=bus))

    def generate_equivalent(self):
        for (n, (bus_frontier, graph, z)) in enumerate(
                zip(self.feeder.bus_frontier, self.feeder.equivalent_graphs, self.feeder.equivalent_values)
        ):
            if self.feeder.main_source_bus not in graph.nodes():
                bus = list(
                    filter(
                        lambda b: b.name == bus_frontier,
                        self.bus
                    )
                )[0]
                if z["A"] is not None and bus.phaseA is not None:
                    self.equivalent.append(
                        RLC(
                            R=z["A"].R,
                            L=z["A"].L if z["A"].X >= 0.0 else 0.0,
                            C=z["A"].C if z["A"].X < 0.0 else 0.0,
                            bus_pos=bus,
                            phase_pos="A",
                            hide_c=True
                        )
                    )
                if z["B"] is not None and bus.phaseB is not None:
                    self.equivalent.append(
                        RLC(
                            R=z["B"].R,
                            L=z["B"].L if z["B"].X >= 0.0 else 0.0,
                            C=z["B"].C if z["B"].X < 0.0 else 0.0,
                            bus_pos=bus,
                            phase_pos="B",
                            hide_c=True
                        )
                    )
                if z["C"] is not None and bus.phaseC is not None:
                    self.equivalent.append(
                        RLC(
                            R=z["C"].R,
                            L=z["C"].L if z["C"].X >= 0.0 else 0.0,
                            C=z["C"].C if z["C"].X < 0.0 else 0.0,
                            bus_pos=bus,
                            phase_pos="C",
                            hide_c=True
                        )
                    )
                if z["N"] is not None and bus.phaseN is not None:
                    self.equivalent.append(
                        RLC(
                            R=z["N"].R,
                            L=z["N"].L if z["N"].X >= 0.0 else 0.0,
                            C=z["N"].C if z["N"].X < 0.0 else 0.0,
                            bus_pos=bus,
                            phase_pos="N",
                            hide_c=True
                        )
                    )

    def generate_surge_arrester(self, surge_arrester_phases="ABC"):
        db_path = join(abspath(dirname(__file__)), "surge_arrester_database.json")
        with open(db_path) as surge_arrester_database:
            surge_arrester_database = json.load(surge_arrester_database)
        vrms = next(iter(self.feeder.feeder_dict["feeder"].values()))["vrms"]
        vrms_db = [float(k) for k in surge_arrester_database.keys()]
        v_surge_arrester = min(vrms_db, key=lambda v: abs(v - vrms))
        surge_arrester_type = None
        for k in surge_arrester_database.keys():
            if float(k) == v_surge_arrester:
                surge_arrester_type = surge_arrester_database[k]

        A0 = []
        for (v, i) in zip(surge_arrester_type["a0"]["v"], surge_arrester_type["a0"]["i"]):
            A0.append([v, i])

        A1 = []
        for (v, i) in zip(surge_arrester_type["a1"]["v"], surge_arrester_type["a1"]["i"]):
            A1.append([v, i])

        surge_arrester_number = 0
        ground_number = 0
        for bus_name in sorted(self.feeder.graph.nodes()):
            bus = self.feeder.graph.nodes[bus_name]
            if "surge_arrester" in bus:
                for (code, surge_arrester) in bus["surge_arrester"].items():
                    if bus["area"]:
                        bus_obj = list(
                            filter(
                                lambda b: b.name == bus_name,
                                self.bus
                            )
                        )[0]

                        bus_obj_ground = Node(name="Terra " + bus_obj.name, type="Terra", sequence=bus_obj.sequence)

                        if "A" in surge_arrester_phases and bus_obj.phaseA is not None:
                            surge_arrester_number += 1
                            ground_number += 1
                            self.surge_arrester.append(
                                SurgeArresterIEEE(
                                    bus_pos=bus_obj,
                                    currentvoltageA0=A0,
                                    currentvoltageA1=A1,
                                    phase_pos="A",
                                    bus_neg=bus_obj_ground,
                                    phase_neg="A",
                                    d=surge_arrester_type["height"],
                                    n=surge_arrester_type["columns"],
                                    prnumber=surge_arrester_number
                                )
                            )
                            self.surge_arrester_ground.append(
                                Ground(
                                    bus_pos=bus_obj_ground,
                                    r=(surge_arrester["diameter"] / 2),
                                    l=surge_arrester["length"],
                                    ro=surge_arrester["ro"],
                                    phase_pos="A",
                                    gndnumber=int(ground_number)
                                )
                            )

                        if "B" in surge_arrester_phases and bus_obj.phaseB is not None:
                            surge_arrester_number += 1
                            ground_number += 1
                            self.surge_arrester.append(
                                SurgeArresterIEEE(
                                    bus_pos=bus_obj,
                                    currentvoltageA0=A0,
                                    currentvoltageA1=A1,
                                    phase_pos="B",
                                    bus_neg=bus_obj_ground,
                                    phase_neg="B",
                                    d=surge_arrester_type["height"],
                                    n=surge_arrester_type["columns"],
                                    prnumber=surge_arrester_number
                                )
                            )
                            self.surge_arrester_ground.append(
                                Ground(
                                    bus_pos=bus_obj_ground,
                                    r=(surge_arrester["diameter"] / 2),
                                    l=surge_arrester["length"],
                                    ro=surge_arrester["ro"],
                                    phase_pos="B",
                                    gndnumber=int(ground_number)
                                )
                            )

                        if "C" in surge_arrester_phases and bus_obj.phaseC is not None:
                            surge_arrester_number += 1
                            ground_number += 1
                            self.surge_arrester.append(
                                SurgeArresterIEEE(
                                    bus_pos=bus_obj,
                                    currentvoltageA0=A0,
                                    currentvoltageA1=A1,
                                    phase_pos="C",
                                    bus_neg=bus_obj_ground,
                                    phase_neg="C",
                                    d=surge_arrester_type["height"],
                                    n=surge_arrester_type["columns"],
                                    prnumber=surge_arrester_number
                                )
                            )
                            self.surge_arrester_ground.append(
                                Ground(
                                    bus_pos=bus_obj_ground,
                                    r=(surge_arrester["diameter"] / 2),
                                    l=surge_arrester["length"],
                                    ro=surge_arrester["ro"],
                                    phase_pos="C",
                                    gndnumber=int(ground_number)
                                )
                            )

    def generate_surge(self, surge_phases="ABC"):
        for bus_name in sorted(self.feeder.graph.nodes()):
            bus = self.feeder.graph.nodes[bus_name]
            if "surge" in bus:
                for (code, surge) in bus["surge"].items():
                    if bus["area"]:
                        bus_obj_surge = list(
                            filter(
                                lambda b: b.name == bus_name,
                                self.bus
                            )
                        )[0]
                        if "A" in surge_phases and bus_obj_surge.phaseA is not None:
                            self.surge.append(
                                CurrentHEIDLER(
                                    bus_pos=bus_obj_surge,
                                    phase_pos="A",
                                    amp=surge["amp"],
                                    tfront=surge["tfront"],
                                    tau=surge["tau"]
                                )
                            )
                        if "B" in surge_phases and bus_obj_surge.phaseB is not None:
                            self.surge.append(
                                CurrentHEIDLER(
                                    bus_pos=bus_obj_surge,
                                    phase_pos="B",
                                    amp=surge["amp"],
                                    tfront=surge["tfront"],
                                    tau=surge["tau"]
                                )
                            )
                        if "C" in surge_phases and bus_obj_surge.phaseC is not None:
                            self.surge.append(
                                CurrentHEIDLER(
                                    bus_pos=bus_obj_surge,
                                    phase_pos="C",
                                    amp=surge["amp"],
                                    tfront=surge["tfront"],
                                    tau=surge["tau"]
                                )
                            )
        surge_sources = ""
        for surge in self.surge:
            if surge.source != "":
                surge_sources += surge.source + "\n"
        self.atp_card_mod_surge = copy(self.atp_card_base)
        self.atp_card_mod_surge.cartao = self.atp_card_mod_surge.cartao.replace("C INSERIR RAIOS AQUI\n", surge_sources)
