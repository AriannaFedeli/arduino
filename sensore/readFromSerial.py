import sys, serial, argparse
import numpy as np
from time import sleep
import time
from datetime import date, datetime, timedelta
from collections import deque
import requests
import json


    
class SendData:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)

      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # add data
  def add(self, data):
      assert(len(data) == 2)
      self.addToBuf(self.ax, data[0])
      self.addToBuf(self.ay, data[1])

  # update plot
  def update(self, frameNum, a0, a1):
      try:
          line = self.ser.readline()
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 2):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax)
              a1.set_data(range(self.maxLen), self.ay)
      except KeyboardInterrupt:
          print('exiting')
      
      return a0, 

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = args.port

  print('reading from serial port %s...' % strPort)
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
  payload={"horse": horse, "beginTs": int(ts), "state": state , "distance": 20.0 , "maxhrt": 120 , "minhrt": 80 , "avghrt": 100 , "endTs" : 1}
  openTrend = (requests.post(url, headers=header, json=(payload)))
  jsonResult = json.loads(openTrend.text)
  trendId = jsonResult['id']
  print("ho aperto il trend e l'id e %s") %trendId
# questo lo devo eseguire in loop fino a quando la serial non prende piu alcun dato  
  urlMeasure = "http://localhost:8000/api/measure" 
  measurets=time.time()
# hrt = freq; dst = non generato, da fare; spd = sped; tutto da SERIAL PORT
  hrt = 1
  dst = 100.0
  spd = 50
  payload = {"ts": int(measurets) , "hrt": hrt , "dst": dst , "spd": spd, "trend": trendId}
  sendValue = (requests.post(urlMeasure, headers=header, json=(payload)))
  print("ho inviato una misurazione al server")

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
