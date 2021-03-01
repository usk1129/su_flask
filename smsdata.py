
from twilio.rest import Client
from datetime import datetime
import sqlite3
import yaml

config_file = 'config.yaml'
with open(config_file,'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)


def send_sms(sms):
    account_sid = cfg['credentials'][5]
    auth_token = cfg['credentials'][6]
    client = Client(account_sid, auth_token)

    #    numbers_to_message = ['+46766051555', '+46760344070']
    #   for number in numbers_to_message:
    #      client.messages.create(
    #          body = sms,
    #         from_ ='+46790644309',
    #        to = number
    #  )
    message = client.messages \
        .create(
        body=sms,
        from_= cfg['numbers'][0],
        to= cfg['numbers'][1]

    )
    print(message.sid)

def connect_to_message():
    print(""" Connect to database """)
    try:
        print('Connecting to  database...')
        conn = sqlite3.connect(cfg['database_path'])
        now = datetime.now()
        dtime = now.strftime("%d/%m/%Y %H:%M:%S")
        sql_table = """create table if not exists driftinfo (id integer primary key autoincrement,
                                       rubrik varchar (100), big varchar(100),small varchar(100),
                                       sms varchar(100), wordpress_process varchar(100),
                                       twitter_process varchar(100),sms_process varchar(100));"""
        sql_select_Query = 'select * from driftinfo where sms_process  = 0  and sms="on" '
        cursor = conn.cursor()
        cursor.execute(sql_table)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total of information in driftinfo is ", cursor.rowcount)
        print("Printing each row's column values in driftinfo")
        for row in records:
            send_sms(row[3])
            sql_update_Query = "update driftinfo set sms_process =\"" + str(dtime) + "\" where id = " + str(row[0])
            cursor.execute(sql_update_Query)
            conn.commit()
        cursor.close()
    except ConnectionError as error:
        print(error)

    finally:
        conn.close()
        print('Connection closed.')

connect_to_message()
