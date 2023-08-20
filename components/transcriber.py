""" Utilites to transcribe audiofile
    (https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-russian)
"""
from typing import Text, Union
from pathlib import Path
from huggingsound import SpeechRecognitionModel
import signal
import whisper
import torch
import json
import os
import gc

SERVICE_NAME = 'TRANSCRIBER'
BATCH_SIZE = 32

def transcribe_audio(
    path_to_audio_file: Union[Text,Path],
    output_dir: Union[Text,Path], 
    model) -> None:
    """ Transcribe single audio file """

    file_name = path_to_audio_file.split(os.sep)[-1] 
    transcription = model.transcribe(path_to_audio_file, language='ru', fp16=True)
    with open(os.path.join(output_dir, file_name.split('.')[0] + '.json'), 'w', encoding='utf8') as out_file:
        json.dump(transcription, out_file, ensure_ascii= False)
    return None


def transcriber_worker(configs_dict, queue, logs_queue, device) -> None:
    """ Daemon cleaner worker """
    #check or load model
    try:
        model = whisper.load_model(configs_dict.model, torch.device(device))
    except RuntimeError as e:
        print(e)
        os.kill(os.getppid(), signal.SIGTERM) # kill parent proc
    f_path = []
    while True:
        if not queue.empty():
            f_path = queue.get()
            logs_queue.put(f'{f_path} Transcribe start' + '|' + SERVICE_NAME + f'_on_{device}_{os.getpid()}')
            transcribe_audio(f_path, configs_dict.output_dir, model)
            logs_queue.put(f'{f_path} Transcribe end' + '|' + SERVICE_NAME + f'_on_{device}')
            torch.cuda.empty_cache()
            gc.collect()
            os.remove(f_path)
        pass