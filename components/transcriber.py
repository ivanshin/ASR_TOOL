""" Utilites to transcribe audiofile
    (https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-russian)
"""
from typing import Text, Union
from pathlib import Path
from huggingsound import SpeechRecognitionModel
import torch
import json
import os
import gc

SERVICE_NAME = 'TRANSCRIBER'

def transcribe_audio(
    path_to_audio_file: Union[Text,Path],
    output_dir: Union[Text,Path], 
    model) -> None:
    """ Transcribe single audio file """

    file_name = path_to_audio_file.split(os.sep)[-1] 
    transcription = model.transcribe([path_to_audio_file])
    with open(os.path.join(output_dir, file_name.split('.')[0] + '.json'), 'w', encoding='utf8') as out_file:
        json.dump(transcription, out_file, ensure_ascii= False)
    return None

def transcriber_worker(configs_dict, queue, logs_queue) -> None:
    """ Daemon cleaner worker """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-russian", device)
    while True:
        if not queue.empty():
            f_path = queue.get()
            logs_queue.put(f'{f_path} Transcribe start' + '|' + SERVICE_NAME)
            transcribe_audio(f_path, configs_dict['output_dir'], model)
            logs_queue.put(f'{f_path} Transcribe end' + '|' + SERVICE_NAME)
            torch.cuda.empty_cache()
            gc.collect()
            os.remove(f_path)
        pass