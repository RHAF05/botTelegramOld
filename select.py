import sqlite3
import datetime

db = sqlite3.connect("data.db")

cursor = db.cursor()

now = datetime.datetime.now()
fecha_ant = str(now.year) + '-0' + str(now.month) + '-0' + str(now.day)


print("SELECT * FROM poles WHERE pole='pole' AND date >= '" +str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " 00:00:00 0.000'")
# datos = cursor.execute("SELECT * FROM personas where nombre='' AND id>0")
datos = cursor.execute("SELECT * FROM poles WHERE pole='pole' AND date >= '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + " 00:00:00 0.000'")
print(len(datos.fetchall()))