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
  username = "testuser2"
  password = "arrivederci"
  doLogin = (requests.post(urlLogin, data={username, password})
  print(doLogin.text)
  jsonToken = json.loads(doLogin.text)
  token = jsonToken['token']
  url = "http://localhost:8000/api/trend"
  state = "BUILDING"
  ts=time.time()
  #ATTENZIONE: L'APERTURA DEL TREND NON DEVE ESSERE ESEGUITA IN MANIERA CICLICA
  horse = 1
  authorization = "Bearer %s" %token
  header = {'Access-Control-Allow-Origin':'*', 'Authorization': authorization}
  payload={"horse":horse, "beginTs": int(ts), "state": state , "distance": 20.0 , "maxhrt": 120 , "minhrt": 80 , "avghrt": 100}
  #print(payload)
  #print(header)
  openTrend = (requests.post(url, headers=header, json=(payload)))
  print(openTrend.text)
  jsonResult = json.loads(openTrend.text)
  trendId = jsonResult['id']
  


  #questa operazione deve essere eseguita finché ho dati nella Serial port
  urlMeasure = "http://localhost:8000/api/measure" 
  ts=time.time()
  hrt = "DEVO PRENDERE IL BATTITO DALLA PORTA SERIALE"
  dst = "DEVO PRENDERE IL BATTITO DALLA PORTA SERIALE"
  spd = "DEVO PRENDERE IL BATTITO DALLA PORTA SERIALE"
  payload = {"ts": ts , "hrt": hrt , "dst": dst , "spd": spd, "trend": trendId}
  sendValue = (requests.post(urlMeasure, headers=header, json=(payload)))
  print(sendValue.text) #mi assicuro di ricevere dal server uno status code == 200

  #una volta che la Serial port non genera più dati, allora devo chiudere il trend settando lo state a valid. 
  urlTrend = "http://localhost:8000/api/trend/%s" %trendId
  stateClose = "VALID"
  distance = "DA DOVE LO PRENDO IL PARAMETRO FINALE?"
  maxhrt = "DA DOVE LO PRENDO IL PARAMETRO FINALE?"
  minhrt = "DA DOVE LO PRENDO IL PARAMETRO FINALE?"
  avghrt = "DA DOVE LO PRENDO IL PARAMETRO FINALE?"
  payloadClose = {"horse":horse, "beginTs": int(ts), "state": stateClose , "distance": distance , "maxhrt": maxhrt , "minhrt": minhrt , "avghrt": avghrt}
  closeTrend = (requests.put(urlTrend, headers=header, json=(payloadClose)))
  print(closeTrend.text)
  #problema: come posso sapere se ho avuto perdite di dati e settare quindi il trend con state a invalid?


  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
