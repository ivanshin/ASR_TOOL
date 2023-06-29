"""
    Utilities to read and validate configs
    from `config.yaml`
"""
from typing import Text, Union, Dict
from pathlib import Path
import yaml

def read_configs(config_file: Union[Text,Path] = "config.yaml") -> Dict:
    """ Read configs"""
    configs_dict = Dict()
    with open(config_file, "r") as stream:
        try:
            configs_dict = yaml.safe_load(stream)
            return configs_dict
        except yaml.YAMLError as exc:
            print(exc)