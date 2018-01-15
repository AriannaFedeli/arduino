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
  url = "http://localhost:8000/api/trend"
  state = "BUILDING"
  ts=time.time()
  #beginTs = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  horse = 1
  header = {'Access-Control-Allow-Origin':'*',
  'Authorization': "Bearer eyJhbGciOiJSUzI1NiJ9.eyJyb2xlcyI6WyJST0xFX09QRVJBVE9SIiwiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoidGVzdHVzZXIyIiwiaWF0IjoxNTE2MDI0MjcyLCJleHAiOjE1MTYwMjc4NzJ9.MDsZXExujwyJz8ubeBcqFxdwBnzSHXuOjFqJVXarmWU-ERZoYrpkW0U1NIzxBvLe2u1KIO61a43hgeDigkHN5cgoq48p10yqDaCGdujYinz6RKzI51nXKPkruC-ETyN8fSIFNwVJfvSJ2B-hTFnBbRXQ6fPdxgtV-kZaa_T9409-OOrXMMWjzRrRCNWlluu48yE5ZkpiXzWAPEKlr4eMvhqBxKYSIjfBeIG98xWEtQYwqbj0sJU9wCme6HjhzL_V0ggNr9Xmd3eSy6WenROWMMWX4T_tgq10ymoWfLFoTy3pF39mMNW1BEBmPR4UWsiwtluIJhcb90M4zdavaDMv2TzBa0vWl4bKYkroIMCPt5BkWyPShebGmn4ZX4GyH6NZF4-qAVXV8ZIhhQ6hJ27oD67vs7VKH8H-5SBXP2_0fpE9Pv89Bzc0hOaGlDQWLN27mF_MI0vFRHOg7enPtBUh6Xz8gt3ENdp_B6ZALXomZ9EAUBwzz0rh-LM-gzt_hek4Od2RS915iMmSrf6nkz31Tsu3qabNVe_6rO4TRQYRDfigr6WkUMHf2K8y6eANcRM3v2WqKE_gcQz3Ke4KPZzuRzHmdtmIQhsP30vwuHq4K-GW5YsmeVHaeGGVNRBN4CW1yKNReUBD3fA7UItf4kcDTZpHRsZu19OxYXoSVwyiKTQ"}
  payload={"horse":horse, "beginTs": int(ts), "state": state , "distance": 20.0 , "maxhrt": 120 , "minhrt": 80 , "avghrt": 100}
  print(payload)
  print(header)
  openTrend = (requests.post(url, headers=header, json=(payload)))
  print(openTrend.text)
  jsonResult = json.loads(openTrend.text)
  #devo capire com'è strutturato questo oggetto per poter poi prendere l'id del trend
  for value in jsonResult:
    print(value['id'])

  #faccio finta di avere l'id del trend nella variabile id
  #questa operazione deve essere eseguita finché ho dati nella Serial port
  id=1
  urlMeasure = "http://localhost:8000/api/measure" 
  payload = {}
  sendValue = (requests.post(urlMeasure, headers=header, json=(payload)))
  print(sendValue.text) #mi assicuro di ricevere dal server uno status code == 200

  #una volta che la Serial port non genera più dati, allora devo chiudere il trend settando lo state a valid. 

  #problema: come posso sapere se ho avuto perdite di dati e settare quindi il trend con state a invalid?


  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
