# -*- coding: utf-8 -*-
import sys, serial, argparse
from datetime import date, datetime, timedelta
import requests
import numpy as np
import time
from time import sleep
from collections import deque
import requests
import json
import keyboard
from time import localtime

SERIAL_PORT = "/dev/ttyACM1"
SERIAL_BAUD_RATE = 9800

ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=SERIAL_BAUD_RATE
)

#username = "testuser2"
#password = "arrivederci"
#headers = {'Content-type':'application/json'}
#r = requests.post('http://localhost:8000/login_check')
# bisogna mettere l'header giusto e le info per il login nel body
# poi devo decodificare il json di ritorno
# prendo il token dal json
def main():
    print "Lettore di dati in live per i cavalli."
    urlLogin = "http://localhost:8000/login_check"
    username = "testUser2"
    password = "arrivederci"
    doLogin = (requests.post(urlLogin, data={'_username': username, '_password': password}))
    jsonToken = json.loads(doLogin.text)
    token = jsonToken['token']
    print("Ho ottenuto il token dal server")
    url = "http://localhost:8000/api/trend"
    state = "BUILDING"
    currentUtc = datetime.utcnow()
    datets = currentUtc + timedelta(hours=1)
    print(datets)
    since = datetime( 1970, 1, 1, 0, 0, 0 )
    ts = int((datets-since).total_seconds())
    horse = 1
    authorization = "Bearer %s" %token
    header = {'Access-Control-Allow-Origin':'*', 'Authorization': authorization}
    payload={"horse": horse, "begints":ts,"state":state , "distance": 0 , "maxhrt": 0 , "minhrt": 0 , "avghrt": 0 , "endTs": 0}
    openTrend = (requests.post(url, headers=header, json=(payload)))
    jsonResult = json.loads(openTrend.text)
    print(openTrend.text)
    trendId = jsonResult['id']
    print("Ho aperto il trend e l'id e %s") %trendId
    count = 0
    try:
        while(count<180):
            data = ser.readline()
            splitd = data.decode("utf-8").split(",")

            if len(splitd)==3:
                frequenza = splitd[0]
                speed = splitd[1]
                distance = splitd[2]
                urlMeasure = "http://localhost:8000/api/measure"
                currentUtc = datetime.utcnow()
                datets = currentUtc + timedelta(hours=1)
                measurets = int((datets-since).total_seconds())
                payload = {"ts": int(measurets) , "hrt": int(float(frequenza)), "dst": int(float(distance)), "spd": int(float(speed)), "trend": trendId}
                sendValue = (requests.post(urlMeasure, headers=header, json=(payload)))
                print(payload)
                count = count +1
    except serial.SerialException as e:
        urlCloseTrend = "http://localhost:8000/api/trend/%s" %trendId
        state = "INVALID"
        payload = {"endTs": measurets, "state":state}
        closeTrend = (requests.put(urlCloseTrend, headers=header, json=(payload)))
	Serial.close()
        return None
    except TypeError as e:
        #Disconnect of USB->UART occured
        urlCloseTrend = "http://localhost:8000/api/trend/%s" %trendId
        state = "INVALID"
        payload = {"endTs": measurets, "state":state}
        closeTrend = (requests.put(urlCloseTrend, headers=header, json=(payload)))
        Serial.close()
        return None   
            
    print("Ho inviato %d misurazioni per il trend %d") %(count, trendId)
    urlCloseTrend = "http://localhost:8000/api/trend/%s" %trendId
    state = "VALID"
    payload = {"endTs": measurets, "state":state}
    closeTrend = (requests.put(urlCloseTrend, headers=header, json=(payload)))
    print(closeTrend.text)
    print("Ho chiuso il trend %d") %trendId
# create parser
    parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
    parser.add_argument('--port', dest='port', required=True)
  # parse args
    args = parser.parse_args()
  #strPort = '/dev/ttyACM0'
    strPort = args.port
    print('Chiudo il lettore.') 
 
def send(packet):
      #if const.DEBUG == const.HIGH:
        #print("Packet sended:")
        #print(packet)
    ser.write(packet.encode())
    ser.flushOutput()
 
def receive():
    data = ser.readline()
    data = data.decode("utf-8").strip()
    return data

if __name__ == '__main__':
    main()
