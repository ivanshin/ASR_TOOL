from components import db_logs_handler
import os
import logging

def configure_loger(APP_CONFIGS):
    if APP_CONFIGS['logs_to_db'] == False:
        return logging.Logger('default_loger')
    database =  os.path.join(APP_CONFIGS['logs_db_path'], 'LOGS.db')
    table = 'log'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)


    attributes_list = ['asctime', 'levelname', 'message'] 
    formatter = logging.Formatter('%(' + ((')s' + db_logs_handler.DEFAULT_SEPARATOR + '%(').join(attributes_list)) + ')s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    sql_handler = db_logs_handler.SQLiteHandler(database = database, table = table, attributes_list = attributes_list)
    sql_handler.setLevel(logging.INFO)
    sql_handler.setFormatter(formatter)

    error_file_handler = logging.FileHandler('error.log')
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)

    critical_file_handler = logging.FileHandler('critical.log')
    critical_file_handler.setLevel(logging.CRITICAL)
    critical_file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(sql_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(critical_file_handler)
    return logger