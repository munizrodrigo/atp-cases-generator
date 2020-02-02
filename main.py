import pprint

from sys import argv
from os.path import abspath, splitext

from configuration.config import Configuration
from argument.arg import Argument
from input.input_txt import define_input_dict as define_input_dict_txt
from input.input_xlsx import define_input_dict as define_input_dict_xlsx
from input.input_dict import define_input_dict as define_input_dict_json
from grid.feeder import Feeder
from exceptions.exceptions import *


def main():
    config = Configuration(script_path=abspath(__file__))

    cmd = Argument(config=config.parser)

    if len(argv) > 1:
        args = cmd.parser.parse_args()

        if args.inp:
            input_ext = splitext(args.inp)[1].lower()

            if input_ext == ".txt":
                with open(args.inp, "r", encoding="utf-8-sig") as input_file:
                    try:
                        feeder_dict = define_input_dict_txt(input_file=input_file)
                    except InputValueError as excep:
                        print("An error occurred!")
                        print(excep.errors)
                        exit()

            elif input_ext == ".xlsx":
                with open(args.inp, "rb") as input_file:
                    try:
                        feeder_dict = define_input_dict_xlsx(input_file=input_file)
                    except InputValueError as excep:
                        print("An error occurred!")
                        print(excep.errors)
                        exit()

            else:
                try:
                    raise IncorrectInputFormatError(
                        message="Input must be .txt or .xlsx",
                        errors="Input file format is '{0}' instead of .txt or .xlsx".format(input_ext)
                    )
                except IncorrectInputFormatError as excep:
                    print("An error occurred!")
                    print(excep)
                    print(excep.errors)
                    exit()

        elif args.dict:
            dict_ext = splitext(args.dict)[1].lower()

            if dict_ext == ".json" or dict_ext == ".txt":
                with open(args.dict) as dict_file:
                    try:
                        feeder_dict = define_input_dict_json(input_file=dict_file)
                    except DictValueError as excep:
                        print("An error occurred!")
                        print(excep)
                        print(excep.errors)
                        exit()

            else:
                try:
                    raise IncorrectDictFormatError(
                        message="Dict must be .json or .txt",
                        errors="Dict file format is '{0}' instead of .json or .txt".format(dict_ext)
                    )
                except IncorrectDictFormatError as excep:
                    print("An error occurred!")
                    print(excep)
                    print(excep.errors)
                    exit()

        else:
            try:
                raise EmptyRequiredArgumentError(
                    message="Arguments --inp or --dict are empty",
                    errors="You must define arguments --inp or --dict."
                )
            except EmptyRequiredArgumentError as excep:
                print("An error occurred!")
                print(excep)
                print(excep.errors)
                exit()

        pprint.pprint(feeder_dict)

        try:
            feeder = Feeder(feeder_dict=feeder_dict)
        except CyclicGraphError as excep:
            print("An error occurred!")
            print(excep)
            print(excep.errors)
            exit()

        fig_base = feeder.electric_diagram.base_figure

        feeder.define_area("830", lim=18)
        feeder.electric_diagram.generate_area_figure()
        fig_area = feeder.electric_diagram.area_figure

        fig_base.show()
        fig_area.show()

    else:
        args = cmd.parser.parse_args(["-h"])


if __name__ == "__main__":
    main()
