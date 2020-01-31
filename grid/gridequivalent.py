from math import sqrt, log10

from copy import deepcopy as copy

from networkx import to_dict_of_lists

from numpy import spacing as min_delta

from grid.impedance import Impedance


class GridEquivalent(object):
    def __init__(self, feeder):
        self.feeder = feeder
        self.equivalent_trees = None
        self.equivalent_values = None

    def calc_equivalent_impedances(self):
        for node in self.feeder.graph.nodes():
            self.feeder.graph.nodes[node]["z"] = GridEquivalent.calc_lumped_equivalent_bus(
                bus=self.feeder.graph.nodes[node]
            )

        for (edge_from, edge_to) in self.feeder.graph.edges():
            self.feeder.graph[edge_from][edge_to]["z"] = GridEquivalent.calc_lumped_equivalent_line(
                branch=self.feeder.graph[edge_from][edge_to]
            )

    def generate_trees(self):
        self.equivalent_trees = []
        for (n_eq, (start_bus, graph)) in enumerate(zip(self.feeder.bus_frontier, self.feeder.equivalent_graphs)):
            start_bus_eq = "{0} - EQ: {1}".format(start_bus, n_eq)
            graph_dict = to_dict_of_lists(graph)
            tree = GridEquivalent.build_tree(bus_code=start_bus_eq, parent_bus_code=start_bus_eq, graph_dict=graph_dict)
            self.equivalent_trees.append(tree)

    @staticmethod
    def build_tree(bus_code, parent_bus_code, graph_dict):
        adj = []
        for u in graph_dict[bus_code]:
            if u != parent_bus_code:
                b = GridEquivalent.build_tree(bus_code=u, parent_bus_code=parent_bus_code, graph_dict=graph_dict)
                adj.append(b)
        bus = {"bus": bus_code, "adj": adj}
        return bus

    def generate_equivalents(self):
        self.equivalent_values = []
        for (n, (eq_graph, eq_tree)) in enumerate(zip(self.feeder.equivalent_graphs, self.equivalent_trees)):
            if self.feeder.main_source_bus not in eq_graph.nodes():
                z_eq = self.calc_equivalent(bus=eq_tree, eq_graph=eq_graph, start_bus=True)
                self.equivalent_values.append(z_eq)
        self.feeder.equivalent_values = self.equivalent_values

    def calc_equivalent(self, bus, eq_graph, start_bus=False):
        if start_bus:
            bus["zeq"] = {"A": None, "B": None, "C": None, "N": None}
        else:
            bus["zeq"] = copy(eq_graph.nodes[bus["bus"]]["z"])
        if len(bus["adj"]) != 0:
            equivalent = []

            for bus_next in bus["adj"]:
                z_branch = eq_graph[bus["bus"]][bus_next["bus"]]["z"]
                bus_next["zeq"] = self.calc_equivalent(bus=bus_next, eq_graph=eq_graph)
                equivalent.append(GridEquivalent.series(z_branch, bus_next["zeq"]))

            equivalent.append(bus["zeq"])
            bus["zeq"] = equivalent[0]
            for eq in equivalent[1:]:
                bus["zeq"] = GridEquivalent.parallel(z1=bus["zeq"], z2=eq)

        return bus["zeq"]

    @staticmethod
    def series(z1, z2):
        result = {"A": None, "B": None, "C": None, "N": None}
        for phase in "ABCN":
            if z1[phase] is None:
                result[phase] = z2[phase]
            elif z2[phase] is None:
                result[phase] = z1[phase]
            else:
                result[phase] = z1[phase] + z2[phase]
        return result

    @staticmethod
    def parallel(z1, z2):
        result = {"A": None, "B": None, "C": None, "N": None}
        for phase in "ABCN":
            if z1[phase] is None:
                result[phase] = z2[phase]
            elif z2[phase] is None:
                result[phase] = z1[phase]
            else:
                result[phase] = z1[phase] // z2[phase]
        return result

    @staticmethod
    def calc_inductance_line(height_struct, sag, length, rmg, dist_horiz):
        height_mean = [H - 0.7 * f for (H, f) in zip(height_struct, sag)]

        dist_img = [[0 for Hi in height_struct] for Hj in height_struct]

        for i in range(len(height_struct)):
            for j in range(len(height_struct)):
                if i == j:
                    dist_img[i][j] = 0
                else:
                    dist_img[i][j] = sqrt(4 * height_mean[i] * height_mean[j] + dist_horiz[i][j])

        ind_matrix = [[0 for Hi in height_struct] for Hj in height_struct]

        for i in range(len(height_struct)):
            for j in range(len(height_struct)):
                if i == j:
                    ind_matrix[i][j] = (4.6052 * 1e-4 * log10((2 * height_mean[i]) / rmg)) * (length / 1e3)
                else:
                    if dist_horiz[i][j] == 0.0:
                        dist_horiz[i][j] = float(min_delta(1.0))
                    ind_matrix[i][j] = -(4.6052 * 1e-4 * log10(dist_img[i][j] / dist_horiz[i][j])) * (length / 1e3)

        inductance = []

        for i in range(len(height_struct)):
            if len(ind_matrix[i]) == 1:
                inductance.append(ind_matrix[i][i])
            else:
                inductance.append(ind_matrix[i][i] + (sum(ind_matrix[i]) - ind_matrix[i][i]) / (len(ind_matrix[i]) - 1))

        return inductance

    @staticmethod
    def calc_lumped_equivalent_line(branch):
        cable = next(iter(branch["cable"].values()))

        pole = next(iter(branch["pole"].values()))

        length = branch["length"]

        rmg = cable["ro"]

        height_struct = []
        sag = []

        for (n, phase) in enumerate(pole["phase"]):
            height_struct.append(pole["height"][n])
            sag.append(pole["height"][n] - pole["sag"][n])

        dist_horiz = [[0 for Hi in height_struct] for Hj in height_struct]

        for i in range(len(dist_horiz)):
            for j in range(len(dist_horiz[i])):
                if i == j:
                    dist_horiz[i][j] = 0
                else:
                    dist_horiz[i][j] = abs(pole["distance"][i] - pole["distance"][j])

        inductance = GridEquivalent.calc_inductance_line(
            height_struct=height_struct,
            sag=sag,
            length=length,
            rmg=rmg,
            dist_horiz=dist_horiz
        )

        z_eq = {
            "A": None,
            "B": None,
            "C": None,
            "N": None
        }

        for (phase, ind) in zip(branch["phase"], inductance):
            z_eq[phase] = Impedance(R=length*cable["resistivity"], L=ind)

        return z_eq

    @staticmethod
    def calc_lumped_equivalent_bus(bus):
        if "load" in bus:
            load_dict = bus["load"]
        else:
            load_dict = {}
        if "capacitor" in bus:
            capacitor_dict = bus["capacitor"]
        else:
            capacitor_dict = {}

        z_eq = {
            "A": None,
            "B": None,
            "C": None,
            "N": None
        }

        for (code, load) in load_dict.items():
            resistance = [
                load["ra"],
                load["rb"],
                load["rc"]
            ]

            inductance = [
                load["la"],
                load["lb"],
                load["lc"]
            ]

            for (phase, R, L) in zip("ABC", resistance, inductance):
                if phase in load["phase"]:
                    if z_eq[phase] is None:
                        z_eq[phase] = Impedance(R=R, L=L)
                    else:
                        z_eq[phase] = z_eq[phase] // Impedance(R=R, L=L)

        for (code, capacitor) in capacitor_dict.items():
            capacitance = [
                capacitor["ca"],
                capacitor["cb"],
                capacitor["cc"]
            ]

            for (phase, C) in zip("ABC", capacitance):
                if phase in capacitor["phase"]:
                    if z_eq[phase] is None:
                        z_eq[phase] = Impedance(R=0.0, C=C)
                    else:
                        z_eq[phase] = z_eq[phase] // Impedance(R=0.0, C=C)

        return z_eq
