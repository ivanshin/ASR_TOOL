"""
    Utilities to read and validate configs
    from `config.yaml`
"""
from typing import Text, Union, Dict
from pathlib import Path
from components.config_structure import ConfigStructure
import os
import yaml


def create_dirs(configs_dict: ConfigStructure) -> None:
    """ Create necessary directories """
    clean_audio_path = os.path.join(configs_dict.working_dir, 'CLEAN_AUDIO')
    if not os.path.exists(clean_audio_path):
        os.makedirs(clean_audio_path)
    configs_dict.clean_audio_dir = clean_audio_path
    if not os.path.exists(configs_dict.output_dir):
        os.makedirs(configs_dict.output_dir)
    if configs_dict.logs_to_db == True:
        if not os.path.exists(configs_dict.logs_db_path):
            os.makedirs(configs_dict.logs_db_path)
    
    return

def validate(configs_dict: Dict) -> None:
    valid_conf_model = ConfigStructure(**configs_dict)
    return valid_conf_model

def read_configs(config_file: Union[Text,Path] = "config.yaml") -> ConfigStructure:
    """ Read configs"""
    configs_dict = dict()
    with open(config_file, "r") as stream:
        try:
            configs_dict = yaml.safe_load(stream)
            configs_dict = validate(configs_dict)
            configs_dict.devices = list(configs_dict.devices)
            create_dirs(configs_dict)
            return configs_dict
        except yaml.YAMLError as exc:
            print(exc)
        except IOError as exc:
            print(exc)