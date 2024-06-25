import requests


with open('data.txt', 'r') as file:
    lines = file.readlines()

    records = []
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:
            datetime_part, sensor_id, temp_humidity = line.rsplit(
                ' ', 2)
            if sensor_id == '2':
                date_part, time_part = datetime_part.split(' ')
                temperature, humidity = temp_humidity.split(',')
                url = 'http://127.0.0.1:8000/device/data'
                # Send the GET request with parameters
                record = {
                    'serial_no':'1235',
                    'date': date_part,
                    'time': time_part,
                    'sensor_id': sensor_id,
                    'temperature': temperature,
                    'humidity': humidity
                }
                response = requests.get(url, params=record)


