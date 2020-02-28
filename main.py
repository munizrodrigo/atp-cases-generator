import json
import pprint
import pickle

from sys import argv
from os import makedirs
from os.path import abspath, splitext, isdir, join, dirname
from plotly.io.orca import config as orca_config
from plotly.offline import plot as offline_plot

from configuration.config import Configuration
from argument.arg import Argument
from input.input_txt import define_input_dict as define_input_dict_txt
from input.input_xlsx import define_input_dict as define_input_dict_xlsx
from input.input_dict import define_input_dict as define_input_dict_json
from grid.feeder import Feeder
from atp.casegenerator import CaseGenerator
from atp.executor import ATPExecutor
from exceptions.exceptions import *


def main():
    config = Configuration(script_path=abspath(__file__))

    cmd = Argument(config=config.parser)

    if len(argv) > 1:
        args = cmd.parser.parse_args()

        try:
            atp_path = ATPExecutor.find_atp()
        except ATPNotFoundError as excep:
            print("An error occurred!")
            print(excep)
            print(excep.errors)
            exit()

        execution_cmd = join(atp_path, "tools", "runATP.exe")

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

        if args.out:
            output_path = abspath(args.out)
            if not isdir(output_path):
                makedirs(output_path)
        else:
            if args.inp:
                output_path = abspath(join(dirname(args.inp), "output"))
                if not isdir(output_path):
                    makedirs(output_path)
            elif args.dict:
                output_path = abspath(join(dirname(args.dict), "output"))
                if not isdir(output_path):
                    makedirs(output_path)

        if args.bus:
            if args.bus in feeder.graph.nodes():
                feeder.define_area(center_bus=args.bus, lim=args.cov)
            else:
                try:
                    raise BusNotFoundError(
                        message="Bus not found on grid",
                        errors="The central bus '{0}' must be on the grid.".format(args.bus)
                    )
                except BusNotFoundError as excep:
                    print("An error occurred!")
                    print(excep)
                    print(excep.errors)
                    exit()
        else:
            feeder.define_area(center_bus=feeder.main_source_bus, lim=args.cov)
        feeder.electric_diagram.generate_area_figure()
        fig_area = feeder.electric_diagram.area_figure

        case = CaseGenerator(feeder=feeder)
        case.generate_base_card(
            simulation_path=output_path,
            execution_cmd=execution_cmd,
            deltat=args.step,
            tmax=args.tmax
        )

        dict_bus = {}
        for bus in case.bus:
            dict_bus[bus.name] = bus.node

        with open(join(output_path, "bus_names.json"), "w") as bus_names:
            json.dump(obj=dict_bus, fp=bus_names, indent=4, sort_keys=True)

        if args.exec:
            ATPExecutor.execute_atp(
                folder_path=output_path,
                atp_filename="base_feeder",
                execution_cmd=execution_cmd
            )

            output = ATPExecutor.read_pl4(pl4_file=join(output_path, "base_feeder.pl4"))

            with open(join(output_path, "output.pckl"), "wb") as output_pckl:
                pickle.dump(output, output_pckl)

        if args.graph:
            orca_config.executable = join(dirname(abspath(__file__)), "orca", "orca.exe")

            fig_base.write_image(join(output_path, "base_feeder.png"))
            fig_area.write_image(join(output_path, "area_feeder.png"))

            offline_plot(fig_base, filename=join(output_path, "base_feeder.html"), auto_open=False)
            offline_plot(fig_area, filename=join(output_path, "area_feeder.html"), auto_open=False)

    else:
        args = cmd.parser.parse_args(["-h"])


if __name__ == "__main__":
    main()
