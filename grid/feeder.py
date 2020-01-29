import networkx as nx

from copy import deepcopy as copy

from grid.electricdiagram import ElectricDiagram
from grid.gridequivalent import GridEquivalent
from exceptions.exceptions import CyclicGraphError


class Feeder(object):
    def __init__(self, feeder_dict):
        self.feeder_dict = feeder_dict
        self.main_source_bus = None
        self.graph = None
        self.center_bus = None
        self.bus_area = None
        self.edge_frontier = None
        self.bus_frontier = None
        self.equivalent_graphs = None
        self.electric_diagram = None

        self.define_main_source_bus()
        self.generate_graph()
        self.remove_cycles()
        self.organize_feeder()

        self.grid_equivalent = GridEquivalent(feeder=self)
        self.grid_equivalent.calc_equivalent_impedances()

        self.electric_diagram = ElectricDiagram(feeder=self)
        self.electric_diagram.generate_base_figure()

    def define_main_source_bus(self):
        sources = list(self.feeder_dict["source"].values())
        main_source = sources[0]
        self.main_source_bus = main_source["bus"]

    def generate_graph(self):
        self.graph = nx.DiGraph()
        for (bus, attributes) in self.feeder_dict["bus"].items():
            self.graph.add_node(node_for_adding=bus, pos=(attributes["x"], attributes["y"]))

        for (branch, attributes) in self.feeder_dict["branch"].items():
            self.graph.add_edge(
                u_of_edge=attributes["from"],
                v_of_edge=attributes["to"],
                code=branch,
                length=attributes["length"],
                phase=attributes["phase"],
                cable={attributes["cable"]: self.feeder_dict["cable"][attributes["cable"]]},
                pole={attributes["pole"]: self.feeder_dict["pole"][attributes["pole"]]}
            )

        for (code, attributes) in self.feeder_dict["source"].items():
            try:
                self.graph.nodes[attributes["bus"]]["source"].update(
                    {
                        code: attributes
                    }
                )
            except KeyError:
                self.graph.nodes[attributes["bus"]]["source"] = {
                    code: attributes
                }

        for (code, attributes) in self.feeder_dict["load"].items():
            try:
                self.graph.nodes[attributes["bus"]]["load"].update(
                    {
                        code: attributes
                    }
                )
            except KeyError:
                self.graph.nodes[attributes["bus"]]["load"] = {
                    code: attributes
                }

        for (code, attributes) in self.feeder_dict["capacitor"].items():
            try:
                self.graph.nodes[attributes["bus"]]["capacitor"].update(
                    {
                        code: attributes
                    }
                )
            except KeyError:
                self.graph.nodes[attributes["bus"]]["capacitor"] = {
                    code: attributes
                }

        for (code, attributes) in self.feeder_dict["switch"].items():
            dict_to_add = {copy(code): copy(attributes)}
            invert = not self.graph.has_edge(attributes["from"], attributes["to"])
            if invert:
                from_temp = copy(attributes["from"])
                to_temp = copy(attributes["to"])
                dict_to_add[code]["from"] = to_temp
                dict_to_add[code]["to"] = from_temp
            try:
                if invert:
                    self.graph[attributes["to"]][attributes["from"]]["switch"].update(dict_to_add)
                else:
                    self.graph[attributes["from"]][attributes["to"]]["switch"].update(dict_to_add)
            except KeyError:
                if invert:
                    self.graph[attributes["to"]][attributes["from"]]["switch"] = dict_to_add
                else:
                    self.graph[attributes["from"]][attributes["to"]]["switch"] = dict_to_add

        for (code, attributes) in self.feeder_dict["surge_arrester"].items():
            try:
                self.graph.nodes[attributes["bus"]]["surge_arrester"].update(
                    {
                        code: attributes
                    }
                )
            except KeyError:
                self.graph.nodes[attributes["bus"]]["surge_arrester"] = {
                    code: attributes
                }

        for (code, attributes) in self.feeder_dict["surge"].items():
            try:
                self.graph.nodes[attributes["bus"]]["surge"].update(
                    {
                        code: attributes
                    }
                )
            except KeyError:
                self.graph.nodes[attributes["bus"]]["surge"] = {
                    code: attributes
                }

    def remove_cycles(self):
        is_cyclic = Feeder.is_cyclic(graph=nx.to_undirected(graph=self.graph), root=self.main_source_bus)

        while is_cyclic:
            changed = True
            cycle_path = nx.find_cycle(G=self.graph, source=self.main_source_bus, orientation="ignore")
            print(cycle_path)

            for path in cycle_path:
                if "switch" in self.graph[path[0]][path[1]]:
                    print("removed", path)
                    self.graph.remove_edge(u=path[0], v=path[1])
                    changed = True
                    break
                changed = False

            if not changed:
                raise CyclicGraphError(
                    message="Can't organize cyclic feeder.",
                    errors="The feeder graph is cyclic in paths {0}. "
                           "No switch can be opened to avoid creating cycles.".format(cycle_path)
                )

            is_cyclic = Feeder.is_cyclic(graph=nx.to_undirected(graph=self.graph), root=self.main_source_bus)

    def organize_feeder(self):
        graph_undirected = nx.to_undirected(graph=self.graph)
        graph_list = nx.to_dict_of_lists(G=self.graph)
        out_edge_list = []
        for (bus, adj) in graph_list.items():
            if not adj:
                out_edge_list.append(bus)
            for node in out_edge_list:
                path = nx.shortest_path(G=graph_undirected, source=self.main_source_bus, target=node)
                path_edges = list(zip(path, path[1:]))
                for (edge_from, edge_to) in path_edges:
                    attrs = graph_undirected[edge_from][edge_to]
                    if self.graph.has_edge(u=edge_from, v=edge_to):
                        self.graph.remove_edge(u=edge_from, v=edge_to)
                    if self.graph.has_edge(u=edge_to, v=edge_from):
                        self.graph.remove_edge(u=edge_to, v=edge_from)
                    self.graph.add_edge(u_of_edge=edge_from, v_of_edge=edge_to, **attrs)

    def define_area(self, center_bus, lim=100):
        if lim > len(list(self.graph)):
            lim = len(list(self.graph))
        self.center_bus = center_bus
        graph_undirected = nx.to_undirected(graph=self.graph)
        self.bus_area = []
        self.bus_area.append(self.center_bus)
        next_adj = list(dict(graph_undirected[self.center_bus]).keys())
        while True:
            adj = copy(next_adj)
            next_adj = []
            for bus in adj:
                if bus not in self.bus_area and len(self.bus_area) < lim:
                    self.bus_area.append(bus)
                    next_adj.extend(list(dict(graph_undirected[bus]).keys()))
            next_adj = list(dict.fromkeys(next_adj))
            for bus in self.bus_area:
                if bus in next_adj:
                    next_adj.remove(bus)
            if len(self.bus_area) == lim:
                break
        for node in self.graph.nodes():
            if node in self.bus_area:
                self.graph.nodes[node]["area"] = True
            else:
                self.graph.nodes[node]["area"] = False
        self.bus_frontier = []
        self.edge_frontier = []
        for edge in self.graph.edges():
            (node_from, node_to) = edge
            if node_from in self.bus_area and node_to in self.bus_area:
                self.graph[node_from][node_to]["area"] = True
            elif node_from in self.bus_area:
                self.graph[node_from][node_to]["area"] = False
                self.bus_frontier.append(node_from)
                self.edge_frontier.append(edge)
            elif node_to in self.bus_area:
                self.graph[node_from][node_to]["area"] = False
                self.bus_frontier.append(node_to)
                self.edge_frontier.append(edge)
            else:
                self.graph[node_from][node_to]["area"] = False

        self.generate_equivalent_graphs()

    def generate_equivalent_graphs(self):
        equivalent_graph = copy(self.graph)
        nodes_to_remove = []
        for node in equivalent_graph:
            if equivalent_graph.nodes[node]["area"]:
                nodes_to_remove.append(node)

        equivalent_graph.remove_nodes_from(nodes=nodes_to_remove)

        for (n_eq, edge) in enumerate(self.edge_frontier):
            if edge[0] in self.bus_frontier:
                node_eq_name = "{0} - EQ: {1}".format(edge[0], n_eq)
                equivalent_graph.add_node(node_eq_name, **copy(self.graph.nodes[edge[0]]))
                equivalent_graph.add_edge(
                    u_of_edge=node_eq_name,
                    v_of_edge=edge[1],
                    **copy(self.graph[edge[0]][edge[1]])
                )
            else:
                node_eq_name = "{0} - EQ: {1}".format(edge[1], n_eq)
                equivalent_graph.add_node(node_eq_name, **copy(self.graph.nodes[edge[1]]))
                equivalent_graph.add_edge(
                    u_of_edge=edge[0],
                    v_of_edge=node_eq_name,
                    **copy(self.graph[edge[0]][edge[1]])
                )

        equivalents = list(nx.connected_components(nx.to_undirected(copy(equivalent_graph))))
        equivalents = [list(eq) for eq in equivalents]

        self.equivalent_graphs = []
        for eq in equivalents:
            self.equivalent_graphs.append(equivalent_graph.subgraph(eq).copy())

    @staticmethod
    def is_cyclic(graph, root):
        return False if nx.cycle_basis(G=graph, root=root) == [] else True
