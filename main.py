import pprint
from sys import argv
from os.path import abspath, splitext
from configuration.config import Configuration
from argument.arg import Argument
from input.input_txt import define_input_dict as define_input_dict_txt
from input.input_xlsx import define_input_dict as define_input_dict_xlsx
from exceptions.exceptions import InputValueError


def main():
    config = Configuration(script_path=abspath(__file__))

    cmd = Argument(config=config.parser)

    if len(argv) > 1:
        args = cmd.parser.parse_args()

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

        pprint.pprint(feeder_dict)
    else:
        args = cmd.parser.parse_args(["-h"])


if __name__ == "__main__":
    main()
