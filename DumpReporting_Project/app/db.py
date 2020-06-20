import cx_Oracle
import datetime
import re

def oracle_db_connection(user, password):
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
    print(conn)
    return conn

#     # cursor = conn.cursor()
#     # print(cursor, 'cursor=========================================')
# data = oracle_db_connection(r'apps', 'apps1234')
# print(data,'ddddddddddddddddddddddddddddd')
#
