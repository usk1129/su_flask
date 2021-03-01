import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime
import yaml



config_file = 'config.yaml'
with open(config_file,'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)




def send_email(message,rubrik):
    email = cfg['email_addresses'][0]
    password = cfg['credentials'][0]
    send_to_email = cfg['email_addresses'][1]
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = rubrik

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

def connect_to_Wordpress():
    print( """ Connect to MySQL database """)
    try:
        print('Connecting to MySQL database...')
        conn = sqlite3.connect(cfg['database_path'])
        print(conn)
        now = datetime.now()
        dtime = now.strftime("%d/%m/%Y %H:%M:%S")
        sql_table = """create table if not exists driftinfo (id integer primary key autoincrement,
                                rubrik varchar (100), big varchar(100),small varchar(100),
                                sms varchar(100), wordpress_process varchar(100),
                                twitter_process varchar(100),sms_process varchar(100));"""

        sql_select_Query = "select * from driftinfo where wordpress_process is NULL"
        cursor = conn.cursor()
        cursor.execute(sql_table)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print(records)
        print("Total of information in driftinfo is ", cursor.rowcount)
        print("Printing each row's column values in driftinfo")
        for row in records:
            send_email(row[2],row[1])
            sql_update_Query = "update driftinfo set wordpress_process =\""+ str(dtime) + "\" where id = " + str(row[0])
            cursor.execute(sql_update_Query)
            conn.commit()
        cursor.close()
    except ConnectionError as error:
        print(error)

    finally:
        conn.close()
        print('Connection closed.')



connect_to_Wordpress()