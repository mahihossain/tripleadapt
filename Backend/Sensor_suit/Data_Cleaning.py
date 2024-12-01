import pandas as pd
import numpy as np
import psycopg2
from scipy import stats
from sklearn.preprocessing import StandardScaler

# Creating the sensor csv files from timescale db
def createCSV(sensor_name):
    CONNECTION = "dbname =tsdb user=tsdbadmin password=ktk5j0c2aomvdrzb host=m125t7sid4.rapfduobbe.tsdb.cloud.timescale.com port=34231 sslmode=require"
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    query = "SELECT * from {sn}".format(sn=sensor_name)
    cursor.execute(query)
    df = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['Timestamp','ax','ay','az','gx','gy','gz'])
    counter = 0 

    for row in cursor.fetchall():
        (ts, ax, ay, az, gx, gy, gz) = row
        df.loc[counter] = [ts, ax, ay, az, gx, gy, gz]
        counter = counter + 1

    new_df=df[2:]
    new_df.to_csv(sensor_name+".csv", index=False) 
    conn.commit()
    cursor.close()
  
# Data Type Converstion
def convert(df):
    cols = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
    # Trimming the dataset timestamp column
    df['Timestamp'] = df['Timestamp'].apply(lambda x: x.strip())
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M:%S.%f', errors='coerce')
    return(df)

# drop rows with missing values
def removeEmptyRows(df):  
    df.dropna(inplace=True)
    return(df)

# drop rows with zeros
def removeRowsWithZeros(df):
    ax_list = df.index[ df.ax==0.0].tolist()
    ay_list = df.index[ df.ay==0.0].tolist()
    az_list = df.index[ df.az==0.0].tolist()
    i_list = list(set(ax_list) & set(ay_list) & set(az_list))
    df.drop(i_list, inplace = True)
    return(df)

# Outlier removal using z statistics (dropping 1.2% values)
def outlierRemoval(df):
    z_scores = stats.zscore(df.iloc[: , 1:])
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 2.5).all(axis=1)
    new_df = df[filtered_entries]
    return(new_df)

# Standardization of data
def standardizingData(df):
    df[['ax', 'ay', 'az', 'gx', 'gy', 'gz']] = StandardScaler().fit_transform(df[['ax', 'ay', 'az', 'gx', 'gy', 'gz']])
    return(df)

# Normalizing the data
def normalizingData(df):
    col = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
    for i in col:
        df[i] = (df[i]-df[i].mean())/df[i].std()
    return(df)

# Main program

sensor_list = ["sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "sensor6", "sensor7"]

# Data creation
for i in sensor_list:
    createCSV(sensor_name=i)   

# Data preprocessing
for j in sensor_list:    
    file_name = j +".csv"
    data_frame = pd.read_csv(file_name)

    dt_frame = convert(data_frame)
    dt_frame = removeEmptyRows(dt_frame)
    dt_frame = removeRowsWithZeros(dt_frame)
    dt_frame = outlierRemoval(dt_frame)
    dt_frame = normalizingData(dt_frame)
#    dt_frame = standardizingData(dt_frame)
# Sort values = Problems
    dt_frame = dt_frame.sort_values(by=['Timestamp'], ascending=True)
    dt_frame.to_csv(file_name, index=False) 

# Combining the dataframes
a = pd.read_csv("sensor1.csv")
a = a.rename(columns={'ax':'ax1','ay':'ay1','az':'az1','gx':'gx1','gy':'gy1','gz':'gz1'})
a = a.iloc[: , 1:]
b = pd.read_csv("sensor2.csv")
b = b.rename(columns={'ax':'ax2','ay':'ay2','az':'az2','gx':'gx2','gy':'gy2','gz':'gz2'})
b = b.iloc[: , 1:]
c = pd.read_csv("sensor3.csv")
c = c.rename(columns={'ax':'ax3','ay':'ay3','az':'az3','gx':'gx3','gy':'gy3','gz':'gz3'})
c = c.iloc[: , 1:]
d = pd.read_csv("sensor4.csv")
d = d.rename(columns={'ax':'ax4','ay':'ay4','az':'az4','gx':'gx4','gy':'gy4','gz':'gz4'})
d = d.iloc[: , 1:]
e = pd.read_csv("sensor5.csv")
e = e.rename(columns={'ax':'ax5','ay':'ay5','az':'az5','gx':'gx5','gy':'gy5','gz':'gz5'})
e = e.iloc[: , 1:]
f = pd.read_csv("sensor6.csv")
f = f.rename(columns={'ax':'ax6','ay':'ay6','az':'az6','gx':'gx6','gy':'gy6','gz':'gz6'})
f = f.iloc[: , 1:]
g = pd.read_csv("sensor7.csv")
g = g.rename(columns={'ax':'ax7','ay':'ay7','az':'az7','gx':'gx7','gy':'gy7','gz':'gz7'})
g = g.iloc[: , 1:]

final = pd.concat([a, b, c, d, e, f, g], axis=1)   

# Splits of dataframes
splits = list(np.array_split(final, 64))