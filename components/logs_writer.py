""" Logger configurer depends on `logs_to_db` option
    in configuretion file: 
    True -> write to set path db
    False -> default console logging
"""
from components import db_logs_handler
import os
import logging

def configure_loger(APP_CONFIGS) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    attributes_list = ['asctime', 'levelname', 'service_name', 'message']
    formatter = logging.Formatter('%(' + ((')s' + db_logs_handler.DEFAULT_SEPARATOR + '%(').join(attributes_list)) + ')s')

    if APP_CONFIGS['logs_to_db'] == True:
        logger.propagate = False
        database =  os.path.join(APP_CONFIGS['logs_db_path'], 'LOGS.db')
        table = 'asr_logs'
        sql_handler = db_logs_handler.SQLiteHandler(database = database, table = table, attributes_list = attributes_list)
        sql_handler.setLevel(logging.INFO)
        sql_handler.setFormatter(formatter)
        logger.addHandler(sql_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

    

        error_file_handler = logging.FileHandler('error.log')
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)

        critical_file_handler = logging.FileHandler('critical.log')
        critical_file_handler.setLevel(logging.CRITICAL)
        critical_file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(error_file_handler)
        logger.addHandler(critical_file_handler)
    return logger