#!/usr/bin/env python
# Copyleft Gter srl 2017
# roberto.marzocchi@gter.it

import spidev
import time
import sys
import navio.util
from navio.mpu9250 import MPU9250

import socket
#import time
from datetime import datetime, date


#socket data
TCP_IP = '192.168.2.126'
TCP_PORT = 8081
BUFFER_SIZE = 1024
check_connection=0



#Gestione dati IMU 
navio.util.check_apm()

imu = MPU9250()

if imu.testConnection():
    print "Connection established: True"
else:
    sys.exit("Connection established: False")

imu.initialize()


time.sleep(1)

while True:
    # imu.read_all()
    # imu.read_gyro()
    # imu.read_acc()
    # imu.read_temp()
    # imu.read_mag()

    # print "Accelerometer: ", imu.accelerometer_data
    # print "Gyroscope:     ", imu.gyroscope_data
    # print "Temperature:   ", imu.temperature
    # print "Magnetometer:  ", imu.magnetometer_data

    # time.sleep(0.1)

    m9a, m9g, m9m = imu.getMotion9()
    # calcolo ora UTC nello stesso formato dell'output di RTKLIB
    dt=datetime.utcnow()
    # Formatting datetime
    ora=dt.strftime("%Y/%m/%d|%H:%M:%S.%f")
    MESSAGE = "IMU|%s|%0.3f|%0.3f|%0.3f" % (ora, m9a[0], m9a[1], m9a[2])
    print MESSAGE

    #print "Acc:", "{:+7.3f}".format(m9a[0]), "{:+7.3f}".format(m9a[1]), "{:+7.3f}".format(m9a[2]),
    #print " Gyr:", "{:+8.3f}".format(m9g[0]), "{:+8.3f}".format(m9g[1]), "{:+8.3f}".format(m9g[2]),
    #print " Mag:", "{:+7.3f}".format(m9m[0]), "{:+7.3f}".format(m9m[1]), "{:+7.3f}".format(m9m[2])


    try:
        if (check_connection==0):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        #s.close()
        check_connection=1
        print "received data:", data
    except:
        print "Connessione socket non riuscita"
        check_connection=0
    time.sleep(0.5)


