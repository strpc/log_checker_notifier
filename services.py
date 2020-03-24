'''
Parsing a log file for errors and system performance.
'''
# -*- coding: utf-8 -*-
import requests

from datetime import datetime, timedelta
import os
import re

import config


try:
    os.path.join('last_errors')
except:
    pass

def get_time():
    '''get actual time from headers google.com'''
    header = requests.get('http://google.com').headers
    date = header['date']
    date_new = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
    date_new = date_new + timedelta(days = 0, 
                                    hours = config.TIME_ZONE, 
                                    minutes = 0)
    return date_new


def check_last_error(name_log):
    try:
        with open(os.path.join(os.getcwd(), 'last_errors', 'last_error_') + name_log, 'r', encoding='utf-8') as last_error:
            last_error = str(last_error.readline())
        return datetime.strptime(last_error, '%Y-%m-%d %H:%M:%S')
    except:
        return datetime.strptime('2020-03-02 15:40:55', '%Y-%m-%d %H:%M:%S')
        


def parse_log(name_log):
    last_error = str(check_last_error(name_log) + timedelta(days = 0, 
                                                        hours = 1, 
                                                        minutes = 0)
                    )
    print(last_error)
    count_errors = 0
    clean_list_error = []
    pattern_error = r'(\d\d\d\d-\d\d-\d\d\s\d\d:\d\d:\d\d):\sERROR:.*'
    pattern_line = r'(\d\d\d\d-\d\d-\d\d\s\d\d:\d\d:\d\d):.*'
    delta_time_error = str(get_time() - timedelta(days = 0, 
                                        hours = 0, 
                                        minutes = config.TIME_DELTA_FOR_CHECK)
                     )
    delta_time_check = str(get_time() - timedelta(days = 0, 
                                        hours = 1, 
                                        minutes = 0)
                     )
    
    
    with open(os.path.join(os.getcwd(), 
                           config.LOCAL_LOGS_DIRECTORY, 
                           name_log), 
              'r', encoding='utf-8') as file:  #SOURCE_LOG[-1]
        for error in file:
            try:
                time_error = re.search(pattern_error, error).group(1)
                print(f'time_error: {time_error} > delta_time_error {delta_time_error}' )
                
                if time_error > delta_time_error and time_error > last_error:
                    print(f'time_error: {time_error} > delta_time_error {delta_time_error}; last_error: {last_error}' )
                    
                    print(1)
                    
                    with open(os.path.join(os.getcwd(), 'last_errors', 'last_error_') + name_log, 
                              'w', encoding='utf-8') as latest_error:
                        latest_error.write(time_error)
                        
                    with open(os.path.join(os.getcwd(), 
                                           config.LOCAL_LOGS_DIRECTORY, name_log)[:-4] 
                              + '_errors.log', 'a', 
                              encoding='utf-8') as errors_file:
                        errors_file.write(error)
                        count_errors += 1
                        
            except:
                pass

            try:
                if re.search(pattern_line, error).group(1) > delta_time_check:
                    clean_list_error.append(error)
            except:
                pass
    return count_errors, len(clean_list_error)