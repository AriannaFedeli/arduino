# -*- coding: utf-8 -*-
import serial
from datetime import date, datetime, timedelta
import mysql.connector


SERIAL_PORT = "/dev/ttyACM0"
SERIAL_BAUD_RATE = 9800

ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=SERIAL_BAUD_RATE
)

cnx = mysql.connector.connect(user='root', database='unicam-horse')

def main():
    print "Programma di monitoraggio cavalli."
    while(1):
        data = ser.readline()
        data = data.decode("utf-8").strip("|")
        print data

cursor = cnx.cursor()

tomorrow = datetime.now().date() + timedelta(days=1)

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

# Insert new employee
cursor.execute(add_employee, data_employee)
emp_no = cursor.lastrowid

# Insert salary information
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}
cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()



 
 
def send(packet):
      if const.DEBUG == const.HIGH:
        print("Packet sended:")
        print(packet)
    ser.write(packet.encode())
    ser.flushOutput()
 
 
def receive():
    data = ser.readline()
    data = data.decode("utf-8").strip()
    return data
 
 
 
if __name__ == '__main__':
    main()