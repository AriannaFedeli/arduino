"""
ldr.py
Display analog data from Arduino using Python (matplotlib)
Author: Mahesh Venkitachalam
Website: electronut.in
"""

import sys, serial, argparse
import numpy as np
from time import sleep
import time
from datetime import date, datetime, timedelta
from collections import deque
import requests

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
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
  authorization = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJyb2xlcyI6WyJST0xFX09QRVJBVE9SIiwiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoidGVzdHVzZXIyIiwiaWF0IjoxNTE2MDE3NTE0LCJleHAiOjE1MTYwNTM1MTR9.gQmdZlomJLANxNPfjYvM_aB8qJodJmIOfraDu0qtHtUrqa21ImDHLTztfLFED47iM_8pMd0E0UrW_qCBYuSe9bKGWsbafp6ntvb2EAYA_f0x7zTZBtuylg9-fiqk96nT8Kt4pCffeoMawhLY_nllkzByJbA8UgUMx6Ged95rbZmpph4HOb4WbRy6avgCXunlbXRGafIeMyym1I5N2oXVgBgd1KrE11xp845Ut1viVAClyswTGrKeYadnXRLKfnJZkdSpQOtEhXGmDgbms63niH_780-LJLFsAU84amxcU0VM6MDyyt3HY8xU6Yg6IDFNuxG3AeBNPOiSyM6CHL4DMkqNs8bw4VLD_X1JeGLU78kaQj--0OVWPM46kR7EuY6UmjuwCtQkn5cKsZpROmxwbWBUrf64G59HDPQNUGHcpXqir3zrDhYSx3XzHYCzaB19NPuRhv9RrqBkl_mLmwmt0u4xtf_Rk9Jgg1e8spQu5dqvS1K1mtuFZPZHi0Xwqvzu4BmSRP4PBoXR6z1WuQ-ZGZouJ4SVZXPWlOke4cREtOGl8sr1t_udMk9BO6FJ4BYheVrZf0-jISE4ZX3G9Bp0cTsZkljav5VrGZAM2W2fnG0i7XDmCY4vqBLPEvlJAZMSBb2V5ZQ_LsXhSa5esudb-Y5xYS5QQL5RVAEIyrQ7L_E'}
  state = "BUILDING"
  ts=time.time()
  #beginTs = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  horse = 1
  print('this is authorization: %s; this is state: %s; this is ts: %d;') %(authorization, state, ts)
  payload={'horse':horse, 'beginTs': ts, 'state':state} 
  openTrend = requests.post(url, headers=authorization, data=payload)
  print(openTrend.text)
  # plot parameters
  '''analogPlot = AnalogPlot(strPort, 100)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1), 
                                 interval=50)

  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()'''

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
