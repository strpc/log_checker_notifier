# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers as handlers

from config import DIR_NAME_LOG, FILE_NAME_LOG, LOCAL_LOGS_DIRECTORY

if not os.path.exists(DIR_NAME_LOG) or not os.path.exists(LOCAL_LOGS_DIRECTORY):
    try:
        os.mkdir(DIR_NAME_LOG)
        os.mkdir(LOCAL_LOGS_DIRECTORY)
    except:
        logging.getLogger().error('Ошибка при создании папки для логов.')


formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
    )
handler = handlers.RotatingFileHandler(os.path.join(DIR_NAME_LOG, 
                                                    FILE_NAME_LOG), 
                                        maxBytes=5242880,
                                        backupCount=5,
                                        encoding='utf-8')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def create(msg):
    logger.info(msg)
    