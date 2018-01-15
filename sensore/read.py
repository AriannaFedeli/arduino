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
contenttype = {'Content-type':'application/json'}
datiAutenticazione = {'_username:':username, '_password':password}
# r = requests.post('http://localhost:8000/login_check', headers=headers, data=payload)
# print(r.text)
url = "http://localhost:8000/api/trend"
authorization = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJyb2xlcyI6WyJST0xFX09QRVJBVE9SIiwiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoidGVzdHVzZXIyIiwiaWF0IjoxNTE2MDA0NzM0LCJleHAiOjE1MTYwMDgzMzR9.eBvsuhbxdMy16kNUxkRcBbylgSmOhmNt9cLb55qO1vyXuYAoZai5iHpPT3ds6GooSGq5P95Y7IiojiK6NZtl7pZtcLmDv7oyK6m3T54wQRquNjG27VC2lQ6lM3hNSb9sKwT9QdFroQe4PdI200hkAoyQ96QmtslvVjhl-IqlKiY59fsBXcNJokxH_hfuwxHZanzyUMZb-B968LJdW0jfVI9Bnf7ONKaKpRcl_gJPTslGc3MKlLfsdrGDbSMhnWJkqiU1KGzOqCYFMzCRPdefz1-nggFtrDLbwUpR0TsYZEVqSLb_5BVXdMiUM0YvgvjfNgSgBw9Od_9QgNGRbB5oIJ6-AhbPjhIGgrRKZWnYaBiAN_PHbqiXX_3nFmO5pD1YUT9s1PtJ2nlZyb1ft13VuTF_VxmI9ILBezlZg7fqKcQVEy4-lS0jrZTlX0m3gOf0G9UK2UG0hN4FrNI-ZTIjJOPPcDD6mSjm4_Wkw6orx-O8XumBe-IUOIpRmU2hWpdMZ8EwwxPkes4j8ksb_V27sHw_rbNJF9FCggNGvKhqwJ6OCGvGvjURbrW9Pl7QgyiwFK6oS9dsdI3dEYI6E9Bqt8TxIQyBZcJUp9VwLnptD2KMeyTM7NpSmE9brBF28O7vLtZuu92hPGnHOI8yBlPUY5S5NDr412bIAJsl5_z_V_I'}
state = "BUILDING"
ts=time.time()
beginTs = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
horse = 1
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
        payload = {'state':state, 'beginTs': beginTs, 'horse':horse}
        r = requests.post(url, headers={authorization}, data=payload)
        print(r.text)
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
