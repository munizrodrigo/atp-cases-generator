import json

from input.impedance_load_capacitor import calculate_impedance_load, calculate_impedance_capacitor

from input.convert_dict_types import convert_dict_types

from exceptions.exceptions import DictValueError


def define_input_dict(input_file):
    try:
        input_dict = json.load(input_file)
    except json.decoder.JSONDecodeError as excep:
        raise DictValueError(
            message=excep,
            errors="Incorrect value in {}".format(str(excep).split(":")[-1])
        )
    input_dict = convert_dict_types(input_dict=input_dict)
    vrms = next(iter(input_dict["feeder"].values()))["vrms"]
    f = next(iter(input_dict["source"].values()))["frequency"]
    for (code, load) in input_dict["load"].items():
        r, l = calculate_impedance_load(s=load["s"], fp=load["fp"], vrms=vrms, f=f, n_phases=len(load["phase"]))
        input_dict["load"][code]["ra"] = float(r) if "A" in load["phase"] else 0.0
        input_dict["load"][code]["rb"] = float(r) if "B" in load["phase"] else 0.0
        input_dict["load"][code]["rc"] = float(r) if "C" in load["phase"] else 0.0
        input_dict["load"][code]["la"] = float(l) if "A" in load["phase"] else 0.0
        input_dict["load"][code]["lb"] = float(l) if "B" in load["phase"] else 0.0
        input_dict["load"][code]["lc"] = float(l) if "C" in load["phase"] else 0.0
    for (code, capacitor) in input_dict["capacitor"].items():
        c = calculate_impedance_capacitor(q=capacitor["q"], vrms=vrms, f=f, n_phases=len(capacitor["phase"]))
        input_dict["capacitor"][code]["ca"] = float(c) if "A" in capacitor["phase"] else 0.0
        input_dict["capacitor"][code]["cb"] = float(c) if "B" in capacitor["phase"] else 0.0
        input_dict["capacitor"][code]["cc"] = float(c) if "C" in capacitor["phase"] else 0.0
    return input_dict
