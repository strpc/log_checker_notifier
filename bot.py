'''
Telegram bot for checking and parcing log errors by SSH connection.
'''
# -*- coding: utf-8 -*-
from functools import wraps
import os
from time import sleep
import threading 

from telebot import TeleBot

import logger
from services import parse_log
from connection_ssh import ConnectToFirstServer, ConnectToSecondServer

import config


bot = TeleBot(config.TOKEN)


def mult_threading(func):
    @wraps(func)
    def wrapper(*args_, **kwargs_):
        func_thread = threading.Thread(target=func,
                                       args=tuple(args_),
                                       kwargs=kwargs_)
        func_thread.start()
        return func_thread
    return wrapper


class CheckLog:
    def check_error(self, count_errors, clean_list_error, name_file):
        if count_errors > 0:
            try:
                bot.send_message(config.GROUP_ID, 
                f'У нас есть некоторое количество(*{count_errors}*) '
                f'проблем в *{name_file}*. Сейчас пришлю лог с ними.', 
                parse_mode='Markdown')
                with open(os.path.join(
                                        os.getcwd(), 
                                        config.LOCAL_LOGS_DIRECTORY, 
                                        name_log)[:-4] + '_errors.log', 
                            'r', encoding='utf-8') as file:
                    bot.send_document(config.GROUP_ID, file)
            except:
                logger.create('Произошла ошибка при'
                              ' попытке отправки сообщения')
            
        elif clean_list_error == 0:
            try:
                bot.send_message(config.GROUP_ID, 
                f'В лог *{name_file}* не приходит информация.'
                ' Проверьте, пожалуйста, исправность системы.', 
                parse_mode='Markdown')
            except:
                logger.create('Произошла ошибка при'
                              ' попытке отправки сообщения')

        try:
            for file in os.listdir(config.LOCAL_LOGS_DIRECTORY):
                os.remove(os.path.join(os.getcwd(), 
                                       config.LOCAL_LOGS_DIRECTORY, 
                                       file)
                          )
        except:
            logger.create('Произошла ошибка при попытке'
                          ' очистки локальной папки с логами')


    def check_supervisor_status(self):
        if ConnectToFirstServer().check_supervisor() != len(
                                                    config.SUPERVISOR_LIST):
            try:
                bot.send_message(config.GROUP_ID, 
                'Наблюдаются проблемы с *supervisor*. Количество'
                ' запущенных воркеров отличается от заданных.', 
                                parse_mode='Markdown') 
            except:
                logger.create('Произошла ошибка'
                              ' при попытке отправки сообщения')


@bot.message_handler(func=lambda message: message.text == '/get_info' \
                                    and message.chat.id == config.GROUP_ID)
def force_check(message):
    try:
        bot.send_message(config.GROUP_ID, 
        'Сейчас будет выполнена проверка всех сервисов.'
        ' Если будут ошибки, я сообщу о них.', 
                                        parse_mode='Markdown') 
    except:
        logger.create('Произошла ошибка при попытке отправки сообщения')
    run_check()


@mult_threading
def run_loop():
    while True:
        run_check()
        sleep(config.SLEEP_FOR_LOOP)


def run_check():
    try:
        ConnectToFirstServer().download_log()
    except:
        logger.create('Произошла ошибка при загрузке лога')
    
    try:
        count_errors, clean_list_error = parse_log(config.PATH_SERVER_LOG[-1])
        CheckLog().check_error(count_errors, 
                                clean_list_error, 
                                config.PATH_SERVER_LOG[-1])
    except:
        logger.create('Произошла ошибка при открытии/парсинге лога')
        for file in os.listdir(config.LOCAL_LOGS_DIRECTORY):
            os.remove(os.path.join(os.getcwd(), 
                                   config.LOCAL_LOGS_DIRECTORY, 
                                   file)
                      )


    CheckLog().check_supervisor_status()
    
    try:
        ConnectToSecondServer().download_trassir_log()
    except:
        logger.create('Произошла ошибка при загрузке лога')
    
    try:
        count_errors, clean_list_error = parse_log(config.PATH_TRASSIR_LOG[-1])
        CheckLog().check_error(count_errors, 
                                clean_list_error, 
                                config.PATH_TRASSIR_LOG[-1])
    except:
        logger.create('Произошла ошибка при открытии/парсинге лога')
        for file in os.listdir(config.LOCAL_LOGS_DIRECTORY):
            os.remove(os.path.join(os.getcwd(), 
                                   config.LOCAL_LOGS_DIRECTORY, 
                                   file)
                      )
            
    try:
        ConnectToSecondServer().download_video_progress_log()
    except:
        logger.create('Произошла ошибка при загрузке лога')
    
    try:
        count_errors, clean_list_error = parse_log(
                                        config.PATH_VIDEO_PROGRESS_LOG[-1])
        CheckLog().check_error(count_errors, 
                                clean_list_error, 
                                config.PATH_VIDEO_PROGRESS_LOG[-1])
    except:
        logger.create('Произошла ошибка при открытии/парсинге лога')
        for file in os.listdir(config.LOCAL_LOGS_DIRECTORY):
            os.remove(os.path.join(os.getcwd(), 
                                   config.LOCAL_LOGS_DIRECTORY, 
                                   file)
                      )


if __name__ == '__main__':
    logger.create('Bot is running...')
    try:
        for file in os.listdir(config.LOCAL_LOGS_DIRECTORY):
            os.remove(os.path.join(os.getcwd(), 
                                   config.LOCAL_LOGS_DIRECTORY, 
                                   file)
                      )
    except:
        logger.create('Произошла ошибка при очистке локальной папки с логами')
    
    run_loop()
    bot.polling(none_stop=True)