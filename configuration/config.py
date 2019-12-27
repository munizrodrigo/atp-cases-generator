from os.path import abspath, dirname, basename, join
from configparser import ConfigParser


class Configuration(object):
    def __init__(self, script_path):
        self.parser = ConfigParser(default_section="default")
        self.parser.read(abspath(join(dirname(script_path), "config.ini")))
        self.parser["path"] = {
            "script_path": script_path,
            "script_dir": dirname(script_path),
            "script_name": basename(script_path),
            "config_path": abspath(join(dirname(script_path), "config.ini"))
        }