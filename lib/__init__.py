import os
import re
import sys
import json
import time
import ctypes
import shutil
import socket
import datetime
import platform
import threading
import subprocess



from .Config import Config
config = Config(
    './config.json',
    {
        'File_Reading': {
            'default': {
                'mode': 'raw',
                'decode': 'latin-1',
                'label': r'\S{3} \S{6} \S{3}'
            },
            '.pdf': {
                'mode': 'ocr',
                'label': r'\S{3} \S{6} \S{3}'
            }
        },
        'Directory_Mapping': {
            '//PrintReciver/Pot_1/': 'Universal-Printer'
        }
    }
)



from .Network import Ping



import mysql.connector as MySQL_Connector
import oracledb as OracleSQL
import psycopg2 as PostgreSQL

from .Database import Info as DatabaseInfo
from .Database import PostgreSQL_Database

StatusDatabase = PostgreSQL_Database(
    DatabaseInfo(
        host = '127.0.0.1',
        port = '5432',
        database = 'service',
        user = 'service_handler',
        password = 'P@zzw0rd'
    )
)
