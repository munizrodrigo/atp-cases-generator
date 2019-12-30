from exceptions.exceptions import InputValueError


def convert_dict_types(input_dict):
    input_dict_corrected = dict(input_dict)
    list_types = {}
    for (case, elements) in input_dict_corrected.items():
        if case == "feeder":
            list_types = {
                "code": str,
                "vrms": float
            }
        elif case == "bus":
            list_types = {
                "code": str,
                "x": float,
                "y": float
            }
        elif case == "branch":
            list_types = {
                "code": str,
                "from": str,
                "to": str,
                "length": float,
                "phase": str,
                "cable": str,
                "pole": str
            }
        elif case == "source":
            list_types = {
                "code": str,
                "bus": str,
                "vrms": float,
                "frequency": float,
                "phase": str,
            }
        elif case == "load":
            list_types = {
                "code": str,
                "bus": str,
                "phase": str,
                "s": float,
                "fp": float,
                "ra": float,
                "rb": float,
                "rc": float,
                "la": float,
                "lb": float,
                "lc": float
            }
        elif case == "capacitor":
            list_types = {
                "code": str,
                "bus": str,
                "phase": str,
                "q": float,
                "ca": float,
                "cb": float,
                "cc": float
            }
        elif case == "surge_arrester":
            list_types = {
                "code": str,
                "bus": str
            }
        elif case == "pole":
            list_types = {
                "code": str,
                "phase": str,
                "distance": float,
                "height": float,
                "sag": float
            }
        elif case == "cable":
            list_types = {
                "code": str,
                "ri": float,
                "ro": float,
                "resistivity": float
            }
        elif case == "surge":
            list_types = {
                "code": str,
                "bus": str,
                "amp": float,
                "tfront": float,
                "tau": float
            }
        for (element, values) in elements.items():
            for (name, value) in values.items():
                converter = list_types[name]
                try:
                    input_dict_corrected[case][element][name] = converter(value)
                except ValueError as excep:
                    raise InputValueError(
                        message=excep,
                        errors="Conversion error in '{}' - '{}' - '{}', impossible to convert '{}' to {}".format(
                            case,
                            element,
                            name,
                            value,
                            str(converter)
                        )
                    )
    return input_dict_corrected
