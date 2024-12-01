import time
import pandas as pd
import datetime
import warnings
import psycopg2

warnings.filterwarnings("ignore")
df1 = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
df2 = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
df3 = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
df4 = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
df5 = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
df6 = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
df7 = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])


CONNECTION = "dbname =tsdb user=tsdbadmin password=ktk5j0c2aomvdrzb host=m125t7sid4.rapfduobbe.tsdb.cloud.timescale.com port=34231 sslmode=require"
conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

counter = 0
file = open('data.txt', 'r')
lines = file.readlines()

for incoming_lines in lines:
    pos_start = incoming_lines.find("b'")
    pos_end = incoming_lines.find("#")
    ts_end = incoming_lines.find("\n")
    values = (incoming_lines[pos_start+2:pos_end-1]).split(";")
    (ax,ay,az,gx,gy,gz) = tuple(values)
    timestamp = datetime.datetime.now()
    ts = incoming_lines[pos_end+1:ts_end]
    topic = incoming_lines[(incoming_lines.find("/")+1) :(incoming_lines.find(" 0"))]

    if topic=="ta_sensor1":
        df1.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
    elif topic=="ta_sensor2":
        df2.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
    elif topic=="ta_sensor3":
        df3.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
    elif topic=="ta_sensor4":
        df4.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
    elif topic=="ta_sensor5":
        df5.loc[counter] = [ts, ax, ay, az, gx, gy, gz]    
    elif topic=="ta_sensor6":
        df6.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
    elif topic=="ta_sensor7":
        df7.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
     
    counter=counter+1
  

    
df1.to_csv("sensor1.csv", index = False)  
df2.to_csv("sensor2.csv", index = False)  
df3.to_csv("sensor3.csv", index = False)  
df4.to_csv("sensor4.csv", index = False)  
df5.to_csv("sensor5.csv", index = False)  
df6.to_csv("sensor6.csv", index = False)   
df7.to_csv("sensor7.csv", index = False)  
file.close()


# query = "CREATE TABLE sensor7(TimeStamp CHAR(100), ax CHAR(20), ay CHAR(20), az CHAR(20), gx CHAR(20), gy CHAR(20), gz CHAR(20));"
# cursor.execute(query)

# putting into timescale db
f1 = open("sensor1.csv", 'r')
cursor.copy_from(f1, 'sensor1', sep=',')
f1.close()
f2 = open("sensor2.csv", 'r')
cursor.copy_from(f2, 'sensor2', sep=',')
f2.close()
f3 = open("sensor3.csv", 'r')
cursor.copy_from(f3, 'sensor3', sep=',')
f3.close()
f4 = open("sensor4.csv", 'r')
cursor.copy_from(f4, 'sensor4', sep=',')
f4.close()
f5 = open("sensor5.csv", 'r')
cursor.copy_from(f5, 'sensor5', sep=',')
f5.close()
f6 = open("sensor6.csv", 'r')
cursor.copy_from(f6, 'sensor6', sep=',')
f6.close()
f7 = open("sensor7.csv", 'r')
cursor.copy_from(f7, 'sensor7', sep=',')
f7.close()
conn.commit()
cursor.close()