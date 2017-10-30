import os
from datetime import datetime
import pymysql

# Reads temperature from sensor and prints to stdout
# id is the id of the sensor
def readSensor(id):
	if id == "-1":
		return "No data"
		
	tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")
	text = tfile.read()
	tfile.close()
	secondLine = text.split("\n")[1]
	temperatureData = secondLine.split(" ")[9]
	temperature = float(temperatureData[2:])
	temperature = temperature / 1000
	
	return "{:0.1f}".format(temperature)

# Reads temperature from all sensors found in /sys/bus/w1/devices/
# starting with "28-...
def getSensorId():
	for file in os.listdir("/sys/bus/w1/devices/"):
		if (file.startswith("28-")):
			return file
		else:
			return "-1"

conn = pymysql.connect(host='192.168.0.50', port=3306, user='root', passwd='', db='Measures')
cur = conn.cursor()
dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
currentTemperature = readSensor(getSensorId())
data = (dt, currentTemperature)

cur.execute("INSERT INTO Measure (Time, Temperature) VALUES (%s, %s)", data)
cur.execute("COMMIT")

cur.close()
conn.close()
