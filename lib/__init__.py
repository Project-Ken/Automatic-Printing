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
