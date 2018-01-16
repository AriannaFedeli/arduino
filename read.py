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
    print "Programma di monitoraggio cavalli."
    urlLogin = "http://localhost:8000/login_check"
    username = "testUser2"
    password = "arrivederci"
    doLogin = (requests.post(urlLogin, data={'_username': username, '_password': password}))
    jsonToken = json.loads(doLogin.text)
    token = jsonToken['token']
    print("ho il token")
    url = "http://localhost:8000/api/trend"
    state = "BUILDING"
    ts=time.time()
    #ATTENZIONE: L'APERTURA DEL TREND NON DEVE ESSERE ESEGUITA IN MANIERA CICLICA
    horse = 1
    authorization = "Bearer %s" %token
    header = {'Access-Control-Allow-Origin':'*', 'Authorization': authorization}
    payload={"horse": horse, "beginTs": int(ts), "state": state}
    openTrend = (requests.post(url, headers=header, json=(payload)))
    jsonResult = json.loads(openTrend.text)
    trendId = jsonResult['id']
    print("ho aperto il trend e l'id e %s") %trendId
    while(1):
        data = ser.readline()
        splitd = data.decode("utf-8").split(",")
	#splitd = data.split(",")
     
        if len(splitd)==3:
            frequenza = splitd[0]
            speed = splitd[1]
            distance = splitd[2]
            print frequenza, speed, distance
            urlMeasure = "http://localhost:8000/api/measure"
            measurets=time.time()
            payload = {"ts": int(measurets) , "hrt": frequenza , "dst": distance , "spd": speed, "trend": trendId}
            sendValue = (requests.post(urlMeasure, headers=header, json=(payload)))
            print("ho inviato una misurazione al server")
        # qui dovrei eseguire ogni volta una post della measure
        # fare json, formattarlo e inviarlo nella request
        #r = requests.post(url, headers=headers)
# create parser
    parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
    parser.add_argument('--port', dest='port', required=True)

  # parse args
    args = parser.parse_args()
  
  #strPort = '/dev/ttyACM0'
    strPort = args.port

    print('reading from serial port %s...' % strPort)
    
# questo lo devo eseguire in loop fino a quando la serial non prende piu alcun dato  
    

    
    print('exiting.') 
 
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
