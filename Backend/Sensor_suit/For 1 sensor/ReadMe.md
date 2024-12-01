# Get data from Sensor and push to Timescale DB
Run the following commands :
```console
python mqtt_paho.py
```
```console 
python push_data_to_timescale_db.py
```

# Get data from Timescale DB and save on the local device
Run the following command:
```console
python get_data_from_timescale_db.py
```

# View the incoming sensor data in real time:
Run the following command:
```console
python live_sensor_data_visualization.py
```