from components.configs_reader import read_configs
from components.watchdog_daemon import create_observer
from components.noisereducer import cleaner_worker
from components.transcriber import transcriber_worker
from components.logs_writer import configure_loger
import multiprocessing as mp
import os
import logging

#TODO: Add logging to simple DB, example:
#(https://stackoverflow.com/questions/2314307/python-logging-to-database)
APP_CONFIGS = read_configs() # read configuration file
logger = configure_loger(APP_CONFIGS)

if __name__ == '__main__':
    # variables
    queue_to_cleaning = mp.Queue()
    queue_to_transcribe = mp.Queue()
    
    # subprocesses
    # 1) watchdog with queue to cleaning
    watchdog_cleaner_proc = mp.Process(target= create_observer, args= (APP_CONFIGS['working_dir'], queue_to_cleaning))
    watchdog_cleaner_proc.daemon= True
    watchdog_cleaner_proc.start()
    #watchdog_proc.join()
    # 2) cleaner
    cleaner = mp.Process(target= cleaner_worker, args= (APP_CONFIGS, queue_to_cleaning))
    cleaner.daemon= True
    cleaner.start()
    # 3) watchdog with queue to transcribation
    watchdog_transcribe_proc = mp.Process(target= create_observer, args= (APP_CONFIGS['clean_audio_dir'], queue_to_transcribe))
    watchdog_transcribe_proc.daemon= True
    watchdog_transcribe_proc.start()
    # 4) Russian wav2vec implementation
    transcriber_proc = mp.Process(target= transcriber_worker, args= (APP_CONFIGS, queue_to_transcribe))
    transcriber_proc.daemon= True
    transcriber_proc.start()
    logger.info('Startup success')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        watchdog_cleaner_proc.terminate()
        cleaner.terminate()
        watchdog_transcribe_proc.terminate()
        transcriber_proc.terminate()
        logger.info('All processes terminated')


