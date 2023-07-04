"""
    Utilities to read and validate configs
    from `config.yaml`
"""
from typing import Text, Union, Dict
from pathlib import Path
import os
import yaml

def create_dirs(configs_dict: Dict) -> None:
    """ Create necessary directories """
    clean_audio_path = os.path.join(configs_dict['working_dir'], 'CLEAN_AUDIO')
    if  not os.path.exists(clean_audio_path):
        os.makedirs(clean_audio_path)
    configs_dict['clean_audio_dir'] = clean_audio_path
    return

def validate(configs_dict: Dict) -> None:
    #TODO: using Pydantic validate config dictionary
    # https://stackoverflow.com/questions/45812387/how-to-validate-structure-or-schema-of-dictionary-in-python
    return

def read_configs(config_file: Union[Text,Path] = "config.yaml") -> Dict:
    """ Read configs"""
    configs_dict = dict()
    with open(config_file, "r") as stream:
        try:
            configs_dict = yaml.safe_load(stream)
            validate(configs_dict)
            create_dirs(configs_dict)
            return configs_dict
        except yaml.YAMLError as exc:
            print(exc)
        except IOError as exc:
            print(exc)