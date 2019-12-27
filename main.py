from sys import argv
from os.path import abspath
from configuration.config import Configuration
from argument.arg import Argument


def main():
    config = Configuration(script_path=abspath(__file__))

    cmd = Argument(config=config.parser)

    if len(argv) > 1:
        args = cmd.parser.parse_args()
    else:
        args = cmd.parser.parse_args(["-h"])


if __name__ == "__main__":
    main()
