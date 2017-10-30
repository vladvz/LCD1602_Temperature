#!/usr/bin/env python
import os
from time import sleep
from datetime import datetime
import LCD1602
import pymysql
import ptvsd

ptvsd.enable_attach(secret='scripts')
#ptvsd.wait_for_attach()

LCD_ADDRESS = 0x27

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

def getTemperature():
    temperature = "-100"
    conn = pymysql.connect(host='192.168.0.50', port=3306, user='root', passwd='', db='Measures')
    cur = conn.cursor()
    cur.execute("SELECT Temperature FROM Measure WHERE Id IN (SELECT MAX(Id) FROM Measure)")

    for r in cur:
        temperature = "%.1f" % r

    cur.close()
    conn.close()

    return temperature

if __name__ == "__main__":
    is_initialized = False
	
    try:
        while True:
            if LCD1602.is_lcd_on(LCD_ADDRESS):
                if not(is_initialized):
                    if LCD1602.init(LCD_ADDRESS, 1):
                        is_initialized = True
                        currentDate = datetime.now().strftime('%d-%m-%Y')
                        currentTime = datetime.now().strftime('%H:%M')
                        #currentTemperature = readSensor(getSensorId())
                        currentTemperature = getTemperature()
                        LCD1602.write(0, 0, currentDate + ' ' + currentTime)
                        LCD1602.write(0, 1, currentTemperature + " C")
            else:
                is_initialized = False
            sleep(0.2)
    except KeyboardInterrupt:
        pass