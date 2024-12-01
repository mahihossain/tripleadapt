import time
import pandas as pd
import datetime
import warnings
import psycopg2

sensor_name="sensor27.csv"
warnings.filterwarnings("ignore")
counter = 0
prev_length = 0
df = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
CONNECTION = "dbname =tsdb user=tsdbadmin password=ktk5j0c2aomvdrzb host=m125t7sid4.rapfduobbe.tsdb.cloud.timescale.com port=34231 sslmode=require"
conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

while True:

    file = open('data.txt', 'r')
    time.sleep(0.5)  ################## time delay between values sent by the sensor consequtively
    incoming_lines = file.readlines()

    if len(incoming_lines) > prev_length:

        prev_length = len(incoming_lines)
        pos_start = incoming_lines[counter].find("b'")
        pos_end = incoming_lines[counter].find("\n")
        values = (incoming_lines[counter][pos_start+2:pos_end]).split(";")
        (ax,ay,az,gx,gy,gz) = tuple(values)
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime('%d-%m-%Y %H:%M:%S.%f')


        df.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
        counter = counter + 1

    else:
        break    

df.to_csv(sensor_name, index = False)   
file.close()

# clear file
open('data.txt', 'w').close()

# putting into timescale db
f = open(sensor_name, 'r')
cursor.copy_from(f, 'sensor_data', sep=',')
f.close()
conn.commit()
cursor.close()