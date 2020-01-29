from math import sqrt, log10

from numpy import spacing as min_delta

from grid.impedance import Impedance


class GridEquivalent(object):
    def __init__(self):
        pass

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
    def calc_lumped_equivalent_line(branch, cable, pole):
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

        z_eq = {}
        for (phase, ind) in zip(branch["phase"], inductance):
            z_eq[phase] = Impedance(R=length*cable["resistivity"], L=ind)

        return z_eq

    @staticmethod
    def calc_lumped_equivalent_bus(load_dict, capacitor_dict):
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
