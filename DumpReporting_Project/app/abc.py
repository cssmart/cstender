import cx_Oracle
import datetime
import re
from mrn_status_report import oracle_db_connection

def abc():
    print("hello")
    aa=oracle_db_connection(r'apps', 'apps1234')
    print(aa,'iiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    cursor = aa.cursor()
    print(cursor,'dddddddddddddddddddddddddd')
abc()
