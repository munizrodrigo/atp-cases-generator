from copy import deepcopy as copy

from webcolors import name_to_rgb as rgb

import plotly.graph_objects as go


class ElectricDiagram(object):
    def __init__(self, feeder):
        self.feeder = feeder
        self.base_figure = None
        self.area_figure = None

    def generate_base_figure(self):
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        for node in self.feeder.graph.nodes():
            x, y = self.feeder.graph.nodes[node]["pos"]
            node_x.append(x)
            node_y.append(y)

            bus_str = "Bus: {0}<br>"
            bus_str = bus_str.format(str(node))

            z_str = "Zeq: "
            z_str += "Za = {0}, Zb = {1}, Zc = {2}<br>".format(
                str(self.feeder.graph.nodes[node]["z"]["A"]),
                str(self.feeder.graph.nodes[node]["z"]["B"]),
                str(self.feeder.graph.nodes[node]["z"]["C"]),
            )

            if "source" in self.feeder.graph.nodes[node]:
                source_str = "Source:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["source"].items():
                    source_str += "{0} - Amp = {1:.2f} Vrms, f = {2:.2f} Hz<br>".format(
                        code,
                        attr["vrms"],
                        attr["frequency"]
                    )
            else:
                source_str = ""

            if "load" in self.feeder.graph.nodes[node]:
                load_str = "Load:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["load"].items():
                    load_str += "{0} - Phase = {1}, S = {2:.2f} VA, FP = {3:.2f}<br>".format(
                        code,
                        attr["phase"],
                        attr["s"],
                        attr["fp"]
                    )
            else:
                load_str = ""

            if "capacitor" in self.feeder.graph.nodes[node]:
                capacitor_str = "Capacitor:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["capacitor"].items():
                    capacitor_str += "{0} - Phase = {1}, Q = {2:.2f} VA<br>".format(
                        code,
                        attr["phase"],
                        attr["q"]
                    )
            else:
                capacitor_str = ""

            if "surge_arrester" in self.feeder.graph.nodes[node]:
                surge_arrester_str = "Surge Arrester:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["surge_arrester"].items():
                    surge_arrester_str += "{0}<br>".format(
                        code
                    )
            else:
                surge_arrester_str = ""

            if "surge" in self.feeder.graph.nodes[node]:
                surge_str = "Surge:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["surge"].items():
                    surge_str += "{0} - Amp = {1:.2f} A, Tfront = {2:.2e} s, tau = {3:.2e} s<br>".format(
                        code,
                        attr["amp"],
                        attr["tfront"],
                        attr["tau"]
                    )
            else:
                surge_str = ""

            text_str = bus_str + z_str + source_str + load_str + capacitor_str + surge_arrester_str + surge_str

            node_text.append(text_str)

            if node == self.feeder.main_source_bus:
                node_color.append("green")
            else:
                node_color.append("black")

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            text=node_text,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                size=10,
                color=node_color,
                line_width=2,
                line_color="black"
            )
        )

        middle_node_x = []
        middle_node_y = []
        middle_node_text = []

        edge_trace = []
        for edge in self.feeder.graph.edges():
            x0, y0 = self.feeder.graph.nodes[edge[0]]["pos"]
            x1, y1 = self.feeder.graph.nodes[edge[1]]["pos"]
            dash = "dot" if "switch" in self.feeder.graph[edge[0]][edge[1]] else "solid"
            edge_go = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                hoverinfo="none",
                line=dict(
                    width=2,
                    color="black",
                    dash=dash
                )
            )
            edge_trace.append(edge_go)

            middle_node_x.append((x0 + x1) / 2)
            middle_node_y.append((y0 + y1) / 2)

            str_format = "Branch: {0}<br>"
            str_format += "Zeq: Za = {1}, Zb = {2}, Zc = {3}, Zn = {4}<br>"
            str_format += "Length = {5:.2f} m, Phase = {6}, Cable = {7}, Pole = {8}"

            middle_node_str = str_format.format(
                self.feeder.graph[edge[0]][edge[1]]["code"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["A"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["B"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["C"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["N"],
                self.feeder.graph[edge[0]][edge[1]]["length"],
                self.feeder.graph[edge[0]][edge[1]]["phase"],
                next(iter(self.feeder.graph[edge[0]][edge[1]]["cable"].keys())),
                next(iter(self.feeder.graph[edge[0]][edge[1]]["pole"].keys()))
            )

            if "switch" in self.feeder.graph[edge[0]][edge[1]]:
                middle_node_str += "<br>Switch:<br>"
                for (code, attr) in self.feeder.graph[edge[0]][edge[1]]["switch"].items():
                    middle_node_str += "{0} - tclose = {1} s, topen = {2} s<br>".format(
                        code,
                        attr["tclose"],
                        attr["topen"]
                    )

            middle_node_text.append(middle_node_str)

        middle_node_trace = go.Scatter(
            x=middle_node_x,
            y=middle_node_y,
            text=middle_node_text,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=10,
                color="black",
                opacity=0.2,
                symbol="square"
            )
        )

        data = []
        data.extend(edge_trace)
        data.append(node_trace)
        data.append(middle_node_trace)

        base_figure = go.Figure(
            data=data,
            layout=go.Layout(
                plot_bgcolor="white",
                showlegend=False,
                hovermode="closest",
                margin=dict(b=0, l=0, r=0, t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )

        self.base_figure = base_figure

    def generate_area_figure(self):
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_aura_color = []
        node_aura_opacity = []
        node_line_color = []
        for node in self.feeder.graph.nodes():
            x, y = self.feeder.graph.nodes[node]["pos"]
            node_x.append(x)
            node_y.append(y)

            bus_str = "Bus: {0}<br>"
            bus_str = bus_str.format(str(node))

            z_str = "Zeq: "
            z_str += "Za = {0}, Zb = {1}, Zc = {2}<br>".format(
                str(self.feeder.graph.nodes[node]["z"]["A"]),
                str(self.feeder.graph.nodes[node]["z"]["B"]),
                str(self.feeder.graph.nodes[node]["z"]["C"]),
            )

            if "source" in self.feeder.graph.nodes[node]:
                source_str = "Source:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["source"].items():
                    source_str += "{0} - Amp = {1:.2f} Vrms, f = {2:.2f} Hz<br>".format(
                        code,
                        attr["vrms"],
                        attr["frequency"]
                    )
            else:
                source_str = ""

            if "load" in self.feeder.graph.nodes[node]:
                load_str = "Load:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["load"].items():
                    load_str += "{0} - Phase = {1}, S = {2:.2f} VA, FP = {3:.2f}<br>".format(
                        code,
                        attr["phase"],
                        attr["s"],
                        attr["fp"]
                    )
            else:
                load_str = ""

            if "capacitor" in self.feeder.graph.nodes[node]:
                capacitor_str = "Capacitor:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["capacitor"].items():
                    capacitor_str += "{0} - Phase = {1}, Q = {2:.2f} VA<br>".format(
                        code,
                        attr["phase"],
                        attr["q"]
                    )
            else:
                capacitor_str = ""

            if "surge_arrester" in self.feeder.graph.nodes[node]:
                surge_arrester_str = "Surge Arrester:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["surge_arrester"].items():
                    surge_arrester_str += "{0}<br>".format(
                        code
                    )
            else:
                surge_arrester_str = ""

            if "surge" in self.feeder.graph.nodes[node]:
                surge_str = "Surge:<br>"
                for (code, attr) in self.feeder.graph.nodes[node]["surge"].items():
                    surge_str += "{0} - Amp = {1:.2f} A, Tfront = {2:.2e} s, tau = {3:.2e} s<br>".format(
                        code,
                        attr["amp"],
                        attr["tfront"],
                        attr["tau"]
                    )
            else:
                surge_str = ""

            text_str = bus_str + z_str + source_str + load_str + capacitor_str + surge_arrester_str + surge_str

            node_text.append(text_str)

            if self.feeder.graph.nodes[node]["area"]:
                node_aura_color.append("blue")
                node_aura_opacity.append(0.1)
            else:
                node_aura_color.append("black")
                node_aura_opacity.append(0.0)

            if node == self.feeder.main_source_bus:
                node_color.append("green")
                node_line_color.append("black")
            elif self.feeder.graph.nodes[node]["area"]:
                node_color.append("blue")
                node_line_color.append("black")
            else:
                node_color.append("black")
                node_line_color.append("black")

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            text=node_text,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                size=10,
                color=node_color,
                line_width=2,
                line_color=node_line_color
            )
        )

        node_aura_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="none",
            marker=dict(
                size=20,
                color=node_aura_color,
                opacity=node_aura_opacity
            )
        )

        middle_node_x = []
        middle_node_y = []
        middle_node_text = []

        edge_trace = []
        edge_aura_trace = []
        for edge in self.feeder.graph.edges():
            x0, y0 = self.feeder.graph.nodes[edge[0]]["pos"]
            x1, y1 = self.feeder.graph.nodes[edge[1]]["pos"]
            dash = "dot" if "switch" in self.feeder.graph[edge[0]][edge[1]] else "solid"
            color = "blue" if self.feeder.graph[edge[0]][edge[1]]["area"] else "black"
            edge_go = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                hoverinfo="none",
                line=dict(
                    width=2,
                    color=color,
                    dash=dash
                )
            )
            edge_trace.append(edge_go)
            edge_aura_color = list(rgb(color))
            if self.feeder.graph[edge[0]][edge[1]]["area"]:
                edge_aura_color.append(0.09)
            else:
                edge_aura_color.append(0.0)
            edge_aura_color = "rgba" + str(tuple(edge_aura_color))
            edge_go = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                hoverinfo="none",
                line=dict(
                    width=10,
                    color=edge_aura_color,
                    dash="solid"
                )
            )
            edge_aura_trace.append(edge_go)

            middle_node_x.append((x0 + x1) / 2)
            middle_node_y.append((y0 + y1) / 2)

            str_format = "Branch: {0}<br>"
            str_format += "Zeq: Za = {1}, Zb = {2}, Zc = {3}, Zn = {4}<br>"
            str_format += "Length = {5:.2f} m, Phase = {6}, Cable = {7}, Pole = {8}"

            middle_node_str = str_format.format(
                self.feeder.graph[edge[0]][edge[1]]["code"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["A"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["B"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["C"],
                self.feeder.graph[edge[0]][edge[1]]["z"]["N"],
                self.feeder.graph[edge[0]][edge[1]]["length"],
                self.feeder.graph[edge[0]][edge[1]]["phase"],
                next(iter(self.feeder.graph[edge[0]][edge[1]]["cable"].keys())),
                next(iter(self.feeder.graph[edge[0]][edge[1]]["pole"].keys()))
            )

            if "switch" in self.feeder.graph[edge[0]][edge[1]]:
                middle_node_str += "<br>Switch:<br>"
                for (code, attr) in self.feeder.graph[edge[0]][edge[1]]["switch"].items():
                    middle_node_str += "{0} - tclose = {1} s, topen = {2} s<br>".format(
                        code,
                        attr["tclose"],
                        attr["topen"]
                    )

            middle_node_text.append(middle_node_str)

        middle_node_trace = go.Scatter(
            x=middle_node_x,
            y=middle_node_y,
            text=middle_node_text,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=10,
                color="black",
                opacity=0.2,
                symbol="square"
            )
        )

        data = []
        data.extend(edge_trace)
        data.extend(edge_aura_trace)
        data.append(node_trace)
        data.append(node_aura_trace)
        data.append(middle_node_trace)

        area_figure = go.Figure(
            data=data,
            layout=go.Layout(
                plot_bgcolor="white",
                showlegend=False,
                hovermode="closest",
                margin=dict(b=0, l=0, r=0, t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )

        self.area_figure = area_figure

    @staticmethod
    def plot_basic_graph(graph):
        node_x = []
        node_y = []
        node_text = []
        for node in graph.nodes():
            x, y = graph.nodes[node]["pos"]
            node_x.append(x)
            node_y.append(y)

            bus_str = "Bus: {0}<br>"
            bus_str = bus_str.format(str(node))

            z_str = "Zeq: "
            z_str += "Za = {0}, Zb = {1}, Zc = {2}<br>".format(
                str(graph.nodes[node]["z"]["A"]),
                str(graph.nodes[node]["z"]["B"]),
                str(graph.nodes[node]["z"]["C"]),
            )

            if "source" in graph.nodes[node]:
                source_str = "Source:<br>"
                for (code, attr) in graph.nodes[node]["source"].items():
                    source_str += "{0} - Amp = {1:.2f} Vrms, f = {2:.2f} Hz<br>".format(
                        code,
                        attr["vrms"],
                        attr["frequency"]
                    )
            else:
                source_str = ""

            if "load" in graph.nodes[node]:
                load_str = "Load:<br>"
                for (code, attr) in graph.nodes[node]["load"].items():
                    load_str += "{0} - Phase = {1}, S = {2:.2f} VA, FP = {3:.2f}<br>".format(
                        code,
                        attr["phase"],
                        attr["s"],
                        attr["fp"]
                    )
            else:
                load_str = ""

            if "capacitor" in graph.nodes[node]:
                capacitor_str = "Capacitor:<br>"
                for (code, attr) in graph.nodes[node]["capacitor"].items():
                    capacitor_str += "{0} - Phase = {1}, Q = {2:.2f} VA<br>".format(
                        code,
                        attr["phase"],
                        attr["q"]
                    )
            else:
                capacitor_str = ""

            if "surge_arrester" in graph.nodes[node]:
                surge_arrester_str = "Surge Arrester:<br>"
                for (code, attr) in graph.nodes[node]["surge_arrester"].items():
                    surge_arrester_str += "{0}<br>".format(
                        code
                    )
            else:
                surge_arrester_str = ""

            if "surge" in graph.nodes[node]:
                surge_str = "Surge:<br>"
                for (code, attr) in graph.nodes[node]["surge"].items():
                    surge_str += "{0} - Amp = {1:.2f} A, Tfront = {2:.2e} s, tau = {3:.2e} s<br>".format(
                        code,
                        attr["amp"],
                        attr["tfront"],
                        attr["tau"]
                    )
            else:
                surge_str = ""

            text_str = bus_str + z_str + source_str + load_str + capacitor_str + surge_arrester_str + surge_str

            node_text.append(text_str)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            text=node_text,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                size=10,
                color="black",
                line_width=2,
                line_color="black"
            )
        )

        middle_node_x = []
        middle_node_y = []
        middle_node_text = []

        edge_trace = []
        for edge in graph.edges():
            x0, y0 = graph.nodes[edge[0]]["pos"]
            x1, y1 = graph.nodes[edge[1]]["pos"]
            dash = "dot" if "switch" in graph[edge[0]][edge[1]] else "solid"
            edge_go = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                hoverinfo="none",
                line=dict(
                    width=2,
                    color="black",
                    dash=dash
                )
            )
            edge_trace.append(edge_go)

            middle_node_x.append((x0 + x1) / 2)
            middle_node_y.append((y0 + y1) / 2)

            str_format = "Branch: {0}<br>"
            str_format += "Zeq: Za = {1}, Zb = {2}, Zc = {3}, Zn = {4}<br>"
            str_format += "Length = {5:.2f} m, Phase = {6}, Cable = {7}, Pole = {8}"

            middle_node_str = str_format.format(
                graph[edge[0]][edge[1]]["code"],
                graph[edge[0]][edge[1]]["z"]["A"],
                graph[edge[0]][edge[1]]["z"]["B"],
                graph[edge[0]][edge[1]]["z"]["C"],
                graph[edge[0]][edge[1]]["z"]["N"],
                graph[edge[0]][edge[1]]["length"],
                graph[edge[0]][edge[1]]["phase"],
                next(iter(graph[edge[0]][edge[1]]["cable"].keys())),
                next(iter(graph[edge[0]][edge[1]]["pole"].keys()))
            )

            if "switch" in graph[edge[0]][edge[1]]:
                middle_node_str += "<br>Switch:<br>"
                for (code, attr) in graph[edge[0]][edge[1]]["switch"].items():
                    middle_node_str += "{0} - tclose = {1} s, topen = {2} s<br>".format(
                        code,
                        attr["tclose"],
                        attr["topen"]
                    )

            middle_node_text.append(middle_node_str)

        middle_node_trace = go.Scatter(
            x=middle_node_x,
            y=middle_node_y,
            text=middle_node_text,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=10,
                color="black",
                opacity=0.2,
                symbol="square"
            )
        )

        data = []
        data.extend(edge_trace)
        data.append(node_trace)
        data.append(middle_node_trace)

        figure = go.Figure(
            data=data,
            layout=go.Layout(
                plot_bgcolor="white",
                showlegend=False,
                hovermode="closest",
                margin=dict(b=0, l=0, r=0, t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )

        figure.show()
