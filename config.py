# -*- coding: utf-8 -*-
# LOCAL SETTINGS:
TIME_DELTA_FOR_CHECK = 15 # type: int; SETTING FOR TIMEDELTA IN CHECK LOG in minut
SLEEP_FOR_LOOP = 900 # type: int; # 15 min in second. SETTING FOR TIMEOUT PARSE LOG in second
TIME_ZONE = 3 # type: int
TOKEN = '' #type: str; your token of telegram bot. To create https://t.me/BotFather
GROUP_ID = -000000000 # type: int; group id of telegram chat
LOCAL_LOGS_DIRECTORY = 'temp_logs' # dirname with temporary logs
DIR_NAME_LOG = 'bot_logs' # dirname of telegram dir with logs
FILE_NAME_LOG = 'tg_bot.log' # filename of telegram logs

# FIRST SERVER SETTINGS: 
FIRST_SSH_HOST = '' # type: str
FIRST_SSH_PORT = 22
FIRST_SSH_USERNAME = '' # type: str
FIRST_SSH_PASSWORD = '' # type: str
PATH_SERVER_LOG =  # list with elements path. example: ['/home', 'etc', 'postgres', '11', 'postgres.log']

# SECOND SERVER SETTINGS
SECOND_SSH_HOST = '' # type: str
SECOND_SSH_PORT = 22 # type: int
SECOND_SSH_USERNAME = '' # type: str
SECOND_SSH_PASSWORD = '' # type: str
PATH_TRASSIR_LOG = # list with elements path. example: ['/home', 'etc', 'postgres', '12', 'postgres.log']
PATH_VIDEO_PROGRESS_LOG = # list with elements path. example: ['/home', 'etc', 'postgres', '11', 'postgres.log']

# SUPERVISOR LIST FOR CHECK STATUS
SUPERVISOR_LIST = [# list of supervisor items. to see enter supervisorctl status all. example:
"/usr/bin/python /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf",
"/home/app/venv/bin/python3.7 /home/app/bot/app.py"
]
