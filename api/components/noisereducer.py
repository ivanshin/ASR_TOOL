""" 
    Utilites to reduce noice using spectral gating
    (https://github.com/timsainb/noisereduce)
"""
from scipy.io import wavfile
from typing import Text, Union
from pathlib import Path
from pydub import AudioSegment
from datetime import datetime, timezone
import os
import noisereduce as nr

def reduce_noise(path_to_audio_file: Union[Text,Path], output_dir: Union[Text,Path]) -> None:
    """ Reduce noize from single audio file """

    file_name = path_to_audio_file.split(os.sep)[-1] 
    sound = AudioSegment.from_wav(path_to_audio_file)
    sound = sound.set_channels(1)
    #sound.export("/output/path.wav", format="wav")
    rate = sound.frame_rate
    reduced_noise = nr.reduce_noise(y=sound, sr=rate)
    ts = datetime.strptime(datetime.now(), "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp()
    wavfile.write(os.path.join(output_dir, ts + file_name), rate, reduced_noise)
    return None
