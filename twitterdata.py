import twitter
#from TwitterAPI import TwitterAPI
from datetime import datetime
import sqlite3
import yaml


config_file = 'config.yaml'
with open(config_file,'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

def send_to_twitter(twitter_data):
    consumer_key = cfg['credentials'][1]
    consumer_secret = cfg['credentials'][2]
    access_token = cfg['credentials'][3]
    access_secret = cfg['credentials'][4]
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_secret)

    status = api.PostUpdate(twitter_data)
    print(status.text)


def connect_to_Twitter():
    try:
        conn = sqlite3.connect(cfg['database_path'])
        now = datetime.now()
        dtime = now.strftime("%d/%m/%Y %H:%M:%S")
        sql_select_Query = 'select * from driftinfo where twitter_process = 0'
        cursor = conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            send_to_twitter(row[3])
            sql_update_Query = "update driftinfo set twitter_process =\"" + str(dtime) + "\" where id  = " + str(row[0])
            cursor.execute(sql_update_Query)
            conn.commit()
        cursor.close()

    except ConnectionError as error:
        print(error)

    finally:
        conn.close()
        print('Connection closes.')


if __name__ == '__main__':
    connect_to_Twitter()
