# -*- coding: utf-8 -*-
import serial
from datetime import date, datetime, timedelta
import requests


SERIAL_PORT = "/dev/ttyACM0"
SERIAL_BAUD_RATE = 9800

ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=SERIAL_BAUD_RATE
)

cnx = mysql.connector.connect(user='testUser2', database='unicam-horse')

username = "testuser2"
password = "arrivederci"
headers = {'Content-type':'application/json'}
r = requests.post('http://localhost:8000/login_check')
# bisogna mettere l'header giusto e le info per il login nel body
# poi devo decodificare il json di ritorno
# prendo il token dal json
def main():
    print "Programma di monitoraggio cavalli."
    while(1):
        data = ser.readline()
        data = data.decode("utf-8").strip("|")
        print data
        # qui dovrei eseguire ogni volta una post della measure
        # fare json, formattarlo e inviarlo nella request
        r = requests.post(url, headers=headers)
        # nell'header ci va il token, key Authorization, nel value mettere Bearer



 
 
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
