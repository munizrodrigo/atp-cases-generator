from sys import argv
from os.path import abspath
from configuration.config import Configuration
from argument.arg import Argument
from input.input_txt import define_input_dict


def main():
    config = Configuration(script_path=abspath(__file__))

    cmd = Argument(config=config.parser)

    if len(argv) > 1:
        args = cmd.parser.parse_args()

        with open(args.inp, "r", encoding="utf-8-sig") as input_file:
            feeder_dict = define_input_dict(input_file=input_file)

        print(feeder_dict)
    else:
        args = cmd.parser.parse_args(["-h"])


if __name__ == "__main__":
    main()
