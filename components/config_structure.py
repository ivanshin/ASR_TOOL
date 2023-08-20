from typing import Text, Union, Dict, Iterable
from pathlib import Path
from pydantic import BaseModel, model_validator

# Base model for configuration file
class ConfigStructure(BaseModel):
    working_dir: Union[Text,Path]
    output_dir: Union[Text,Path]
    clean_audio_dir: Union[Text,Path] = None
    model: Union[Text,None] = 'large-v2'
    devices: Union[Text, Iterable, None] = 'cpu'
    logs_to_db: bool
    logs_db_path: Union[Text,Path,None]
    class Config:
        extra = 'forbid'
        validate_assigment = True

    @model_validator(mode= 'before')
    @classmethod
    def set_null_feilds(cls, field_values):
        if field_values['devices'] is None:
            field_values['devices'] = ['cpu']
        if field_values['model'] is None:
            field_values['model'] = 'tiny'
        return field_values