import pymysql
from datetime import datetime

conn = pymysql.connect(host='192.168.0.50', port=3306, user='root', passwd='Mars1972!', db='Measures')
cur = conn.cursor()

for i in range(10):
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp=34.125 + i
    data = (dt, "%.1f" % temp)
    cur.execute("INSERT INTO Measure (Time, Temperature) VALUES (%s, %s)", data)

cur.execute("COMMIT")

cur.execute("SELECT * FROM Measure")

for r in cur:
    print(r)

cur.close()
conn.close()
