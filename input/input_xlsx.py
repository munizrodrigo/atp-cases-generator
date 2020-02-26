import pandas as pd

from math import sqrt, acos, sin, pi

from input.convert_dict_types import convert_dict_types


def define_input_dict(input_file):
    dict_df = pd.read_excel(input_file, sheet_name=None, encoding="utf-16", dtype=object, index_col=None, header=0)
    input_dict = {}
    for (case, df) in dict_df.items():
        input_dict[str(case).lower()] = {}
        header = list(df.columns)
        for (index, row) in df.iterrows():
            list_row = list(row)
            if str(list_row[0]) not in input_dict[str(case).lower()]:
                input_dict[str(case).lower()][str(list_row[0])] = {}
            for (h, v) in zip(header[1:], list_row[1:]):
                if str(case).lower() == "pole":
                    if not str(h).lower() in input_dict[str(case).lower()][str(list_row[0])]:
                        input_dict[str(case).lower()][str(list_row[0])][str(h).lower()] = [v]
                    else:
                        input_dict[str(case).lower()][str(list_row[0])][str(h).lower()].append(v)
                else:
                    input_dict[str(case).lower()][str(list_row[0])][str(h).lower()] = v
    input_dict = convert_dict_types(input_dict=input_dict)
    for (code, load) in input_dict["load"].items():
        vrms = next(iter(input_dict["feeder"].values()))["vrms"]
        f = next(iter(input_dict["source"].values()))["frequency"]
        r, l = calculate_impedance_load(s=load["s"], fp=load["fp"], vrms=vrms, f=f, n_phases=len(load["phase"]))
        input_dict["load"][code]["ra"] = float(r) if "A" in load["phase"] else 0.0
        input_dict["load"][code]["rb"] = float(r) if "B" in load["phase"] else 0.0
        input_dict["load"][code]["rc"] = float(r) if "C" in load["phase"] else 0.0
        input_dict["load"][code]["la"] = float(l) if "A" in load["phase"] else 0.0
        input_dict["load"][code]["lb"] = float(l) if "B" in load["phase"] else 0.0
        input_dict["load"][code]["lc"] = float(l) if "C" in load["phase"] else 0.0
    return input_dict


def calculate_impedance_load(s, fp, vrms, f, n_phases):
    v = vrms / sqrt(3) if n_phases == 1 else vrms
    p = s * fp
    z = (v ** 2 / p) * fp
    theta = acos(fp)
    r = z * fp
    l = (z * sin(theta)) / (2 * pi * f)
    return r, l
