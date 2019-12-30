import json

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
    return input_dict
