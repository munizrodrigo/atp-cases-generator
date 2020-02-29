from argparse import ArgumentParser


class Argument(object):
    def __init__(self, config):
        self.parser = ArgumentParser(
            prog=config["version"]["prog"],
            description="A tool to automatically generate the ATP software input files from the technical information "
                        "of the electrical power systems."
        )

        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="{} v{}".format(config["version"]["prog"], config["version"]["version"])
        )

        gen_group = self.parser.add_argument_group(
            title="ATP cases generator arguments",
            description="Arguments related to reading input files and generating .atp files."
        )

        input_group = gen_group.add_mutually_exclusive_group(required=False)
        input_group.add_argument(
            "-i",
            "--inp",
            action="store",
            type=str,
            help="set the path of input .xlsx or .txt file",
            metavar="FILE"
        )
        input_group.add_argument(
            "-d",
            "--dict",
            action="store",
            type=str,
            help="set the path of input .json file with electric grid dictionary",
            metavar="FILE"
        )

        gen_group.add_argument(
            "-o",
            "--out",
            action="store",
            type=str,
            help="set the directory of output files",
            metavar="PATH"
        )

        gen_group.add_argument(
            "-b",
            "--bus",
            action="store",
            type=str,
            help="set the central bus of the coverage area",
            metavar="NAME"
        )

        gen_group.add_argument(
            "-c",
            "--cov",
            action="store",
            default=config["coverage"]["default_coverage"],
            type=int,
            help="set the number of electric buses in the coverage area (default: %(metavar)s = %(default)s)",
            metavar="BUS"
        )

        gen_group.add_argument(
            "-m",
            "--limit",
            action="store",
            default=config["equivalent"]["maximum_limit"],
            type=float,
            help=("set the maximum permissible length in meters for the transmission line equivalent "
                  "(default: %(metavar)s = %(default)s)"),
            metavar="LIM"
        )

        gen_group.add_argument(
            "-l",
            "--line",
            action="store_true",
            help="use transmission line equivalents"
        )

        gen_group.add_argument(
            "-g",
            "--graph",
            action="store_true",
            help="generate electric grid graphs"
        )

        exec_group = self.parser.add_argument_group(
            title="ATP execution arguments",
            description="Arguments related to the execution of the generated .atp files."
        )
        exec_group.add_argument(
            "-e",
            "--exec",
            action="store_true",
            help="execute generated .atp file"
        )
        exec_group.add_argument(
            "-s",
            "--step",
            action="store",
            default=config["atp"]["default_stepsize"],
            type=float,
            help="set simulation stepsize in seconds, equivalent to DELTAT variable on ATP "
                 "(default: %(metavar)s = %(default)s)",
            metavar="STEP"
        )
        exec_group.add_argument(
            "-t",
            "--tmax",
            action="store",
            default=config["atp"]["default_tmax"],
            type=float,
            help="set maximum simulation time in seconds, equivalent to TMAX variable on ATP "
                 "(default: %(metavar)s = %(default)s)",
            metavar="TMAX"
        )
