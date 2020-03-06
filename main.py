import json
import pickle
import warnings

from sys import argv
from os import makedirs
from os.path import abspath, splitext, isdir, join, dirname
from pathlib import Path
from shutil import rmtree, copytree

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
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from plotly.io.orca import config as orca_config
        from plotly.offline import plot as offline_plot

    config = Configuration(script_path=abspath(__file__))

    cmd = Argument(config=config.parser)

    if len(argv) > 1:
        args = cmd.parser.parse_args()

        if args.print:
            print(config.parser["version"]["prog"])
            print("Version: " + config.parser["version"]["version"])
            print()

            print("Searching for ATP installation path...")
            print()

        try:
            atp_path = ATPExecutor.find_atp()
            if args.print:
                print("ATP installation found at: " + atp_path)
                print()
        except ATPNotFoundError as excep:
            print("An error occurred!")
            print(excep)
            print(excep.errors)
            exit()

        execution_cmd = join(atp_path, "tools", "runATP.exe")

        if args.inp:
            if args.print:
                print("Input file defined as: " + args.inp)
                print()
                print("Reading input file ...")
                print()

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
            if args.print:
                print("Input dict defined as: " + args.dict)
                print()
                print("Reading input file...")
                print()

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

        if args.print:
            print("Input file read successfully!")
            print()
            print("Feeder: " + next(iter(feeder_dict["feeder"])))
            print("Voltage RMS: " + str(next(iter(feeder_dict["feeder"].values()))["vrms"]))
            print("Number of Buses: " + str(len(feeder_dict["bus"])))
            print("Number of Branches: " + str(len(feeder_dict["branch"])))
            print()

        try:
            feeder = Feeder(
                feeder_dict=feeder_dict,
                use_line_equivalents=args.line,
                line_equivalents_length_limit=args.limit
            )
        except CyclicGraphError as excep:
            print("An error occurred!")
            print(excep)
            print(excep.errors)
            exit()

        fig_base = feeder.electric_diagram.base_figure

        if args.out:
            if args.print:
                print("Output directory defined as: " + args.out)
                print()
                print("Creating output directory...")
                print()
            output_path = abspath(args.out)
            if not isdir(output_path):
                makedirs(output_path)
        else:
            if args.print:
                print("Output directory not defined! Using default instead.")
                print()
                print("Creating output directory...")
                print()
            if args.inp:
                output_path = abspath(join(dirname(args.inp), "output"))
                if not isdir(output_path):
                    makedirs(output_path)
            elif args.dict:
                output_path = abspath(join(dirname(args.dict), "output"))
                if not isdir(output_path):
                    makedirs(output_path)

        use_temp_directory = False
        if " " in output_path:
            use_temp_directory = True

        if use_temp_directory:
            home_path = abspath(str(Path.home()))
            work_directory = join(home_path, "DOCUME~1", "ATPdata", "work")
            sim_directory = join(work_directory, next(iter(feeder.feeder_dict["feeder"])))
            if not isdir(sim_directory):
                makedirs(sim_directory)
            else:
                rmtree(path=sim_directory)
                makedirs(sim_directory)
            if args.print:
                print(
                    "Illegal ATP character found in the output directory. Using the temporary directory: "
                    + sim_directory
                )
                print()
        else:
            sim_directory = str(output_path)

        if args.print:
            print("Output directory created successfully!")
            print()

        if args.bus:
            if args.print:
                print("Coverage area central bus defined as: " + args.bus)
                print()
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

        if args.print:
            print("Generating feeder ATP Cases...")
            print()

        case.generate_card(
            simulation_path=sim_directory,
            execution_cmd=execution_cmd,
            deltat=args.step,
            tmax=args.tmax
        )

        if args.print:
            print("Feeder ATP Cases generated successfully!")
            print()

        dict_bus = {}
        for bus in case.bus:
            dict_bus[bus.name] = bus.node

        with open(join(sim_directory, "bus_names.json"), "w") as bus_names:
            json.dump(obj=dict_bus, fp=bus_names, indent=4, sort_keys=True)

        if args.exec:
            if args.print:
                print("Executing ATP base feeder file...")
                print()

            ATPExecutor.execute_atp(
                folder_path=sim_directory,
                atp_filename="base_feeder",
                execution_cmd=execution_cmd
            )

            output = ATPExecutor.read_pl4(pl4_file=join(sim_directory, "base_feeder.pl4"))

            with open(join(sim_directory, "base_feeder_output.pckl"), "wb") as output_pckl:
                pickle.dump(output, output_pckl)

            if args.print:
                print("ATP base feeder file executed successfully!")
                print()
                print("Executing ATP surge feeder file...")
                print()

            ATPExecutor.execute_atp(
                folder_path=sim_directory,
                atp_filename="surge_feeder",
                execution_cmd=execution_cmd
            )

            output = ATPExecutor.read_pl4(pl4_file=join(sim_directory, "surge_feeder.pl4"))

            with open(join(sim_directory, "surge_feeder_output.pckl"), "wb") as output_pckl:
                pickle.dump(output, output_pckl)

            if args.print:
                print("ATP surge feeder file executed successfully!")
                print()

        if args.graph:
            if args.print:
                print("Generating feeder figures...")
                print()

            orca_config.executable = join(dirname(abspath(__file__)), ".orca", "orca.exe")

            fig_base.write_image(join(sim_directory, "base_feeder.png"))
            fig_area.write_image(join(sim_directory, "area_feeder.png"))

            offline_plot(fig_base, filename=join(sim_directory, "base_feeder.html"), auto_open=False)
            offline_plot(fig_area, filename=join(sim_directory, "area_feeder.html"), auto_open=False)

            if args.print:
                print("Feeder figures generated successfully!")
                print()

        if use_temp_directory:
            if args.print:
                print("Copying files from the temporary directory to the output directory...")
                print()
            copytree(src=sim_directory, dst=output_path, dirs_exist_ok=True)
            if args.print:
                print("Files copied successfully!")
                print()
                print("Deleting temporary directory...")
                print()
            rmtree(path=sim_directory)
            if args.print:
                print("Directory deleted successfully!")
                print()

        if args.print:
            print("ATP Cases Generator executed successfully!")
            print()

    else:
        args = cmd.parser.parse_args(["-h"])


if __name__ == "__main__":
    main()
