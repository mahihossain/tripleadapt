import psycopg2
import pandas as pd

CONNECTION = "dbname =tsdb user=tsdbadmin password=ktk5j0c2aomvdrzb host=m125t7sid4.rapfduobbe.tsdb.cloud.timescale.com port=34231 sslmode=require"
query = "SELECT * from sensor_data" 
conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()
cursor.execute(query)

df = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
counter = 0 

for row in cursor.fetchall():
    (ts, ax, ay, az, gx, gy, gz) = row
    df.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
    counter = counter + 1

new_df=df[8:]
new_df.to_csv("sensor_data.csv", index=False) 
conn.commit()
cursor.close()
