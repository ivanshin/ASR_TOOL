""" 
    Utilites to reduce noice using spectral gating
    (https://github.com/timsainb/noisereduce)
"""
from scipy.io import wavfile
from typing import Text, Union
from pathlib import Path
from pydub import AudioSegment
from datetime import datetime
import librosa
import soundfile
import os
import noisereduce as nr


SERVICE_NAME = 'NOISE_CLEANER'

def reduce_noise(path_to_audio_file: Union[Text,Path], output_dir: Union[Text,Path]) -> None:
    """ Reduce noize from single audio file """

    file_name = path_to_audio_file.split(os.sep)[-1] 
    sound = AudioSegment.from_file(path_to_audio_file).set_channels(1)
    rate = sound.frame_rate
    reduced_noise = nr.reduce_noise(y=sound.get_array_of_samples(), sr=rate, prop_decrease= 0.1)
    ts = str(datetime.timestamp(datetime.now()) * 1000).split('.')[0]
    wavfile.write(os.path.join(output_dir, ts + "_" + file_name), 16000, reduced_noise)
    return None

def cleaner_worker(configs_dict, queue, logs_queue) -> None:
    """ Daemon cleaner worker """
    while True:
        if not queue.empty():
            f_path = queue.get()
            logs_queue.put(f'{f_path} Clean start' + '|' + SERVICE_NAME)
            reduce_noise(f_path, configs_dict['clean_audio_dir'])
            logs_queue.put(f'{f_path} Clean end'+'|' + SERVICE_NAME)
            os.remove(f_path)
        pass
