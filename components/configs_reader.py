"""
    Utilities to read and validate configs
    from `config.yaml`
"""
from typing import Text, Union, Dict
from pathlib import Path
from pydantic import BaseModel
import os
import yaml

# Base model for configuration file
class ConfigStructure(BaseModel):
    working_dir: Union[Text,Path]
    output_dir: Union[Text,Path]
    class Config:
        extra = 'forbid'


def create_dirs(configs_dict: Dict) -> None:
    """ Create necessary directories """
    clean_audio_path = os.path.join(configs_dict['working_dir'], 'CLEAN_AUDIO')
    if  not os.path.exists(clean_audio_path):
        os.makedirs(clean_audio_path)
    configs_dict['clean_audio_dir'] = clean_audio_path
    if  not os.path.exists(configs_dict['output_dir']):
        os.makedirs(configs_dict['output_dir'])
    return

def validate(configs_dict: Dict) -> None:
    valid_conf_model = ConfigStructure(**configs_dict)
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