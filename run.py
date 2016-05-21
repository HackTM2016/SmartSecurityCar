#!/usr/bin/python
import RPi.GPIO as GPIO
import serial
import MySQLdb
import time


motor1_1 = 7
motor1_2 = 11

motor2_1 = 13
motor2_2 = 15

alarm = 40;
lanterna = 38;


GPIO.setmode(GPIO.BOARD) 

GPIO.setup(motor1_1, GPIO.OUT) 
GPIO.setup(motor1_2, GPIO.OUT)
GPIO.setup(motor2_1, GPIO.OUT)
GPIO.setup(motor2_2, GPIO.OUT)

GPIO.setup(alarm, GPIO.OUT)
GPIO.setup(lanterna, GPIO.OUT)


ser = serial.Serial(
   port='/dev/ttyUSB0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)



db = MySQLdb.connect("localhost","root","motocicleta","car" )

cursor = db.cursor()
cursor1 = db.cursor()
cursor2 = db.cursor()
try:
  while 1:
    x1 = ser.readline()
    d = x1.split("/")
    print d
    if(d[0]):
       #print data[3]
       fata = d[0]
       spate = d[1]
       
  
   
    cursor.execute("SELECT * FROM run WHERE Id = 1")
    cursor1.execute("SELECT * FROM sensors ORDER BY `Id` DESC LIMIT 1")
    s  = (fata, spate)
    cursor2.execute("INSERT INTO sensors(fata,spate) VALUES (%s,%s)", s)
    
    data = cursor.fetchone()
    data1 = cursor1.fetchone()
    #print data1
    print data
    
    #print data[1]
    GPIO.output(alarm, GPIO.HIGH)
    GPIO.output(lanterna, GPIO.HIGH) 
    
    if float(data[1]) == 1:
       print "Command fata -- sensor data:"+data1[1]
       
       if(float(data1[1]) > 20):
          GPIO.output(motor1_1, GPIO.LOW) #spate dreapta
          GPIO.output(motor1_2, GPIO.HIGH)
          GPIO.output(motor2_1, GPIO.HIGH) #spate stanga
          GPIO.output(motor2_2, GPIO.LOW)
          
          GPIO.output(alarm, GPIO.HIGH)
          GPIO.output(lanterna, GPIO.LOW)
          print "fata RUN"
       else:
          GPIO.output(motor1_1, GPIO.LOW) #spate dreapta
          GPIO.output(motor1_2, GPIO.LOW)
          GPIO.output(motor2_1, GPIO.LOW) #spate stanga
          GPIO.output(motor2_2, GPIO.LOW)
          
          GPIO.output(alarm, GPIO.LOW)
          GPIO.output(lanterna, GPIO.HIGH)
          
          time.sleep(1)
          
          GPIO.output(motor1_1, GPIO.HIGH) #spate dreapta
          GPIO.output(motor1_2, GPIO.LOW)
          GPIO.output(motor2_1, GPIO.LOW) #spate stanga
          GPIO.output(motor2_2, GPIO.HIGH)
          
          time.sleep(2)
          
          #auto evitare
          
          print "fata STOP"
           
       
    elif float(data[2]) == 1:
       print "Command spate -- sensor data:"+data1[2]
       
       if(float(data1[2]) > 20):
         
         GPIO.output(motor1_1, GPIO.HIGH) #spate dreapta
         GPIO.output(motor1_2, GPIO.LOW)
         GPIO.output(motor2_1, GPIO.LOW) #spate stanga
         GPIO.output(motor2_2, GPIO.HIGH)
         
         GPIO.output(alarm, GPIO.HIGH)
         GPIO.output(lanterna, GPIO.HIGH)
         print ("Spate RUN")
         
       else:
         
         GPIO.output(motor1_1, GPIO.LOW) #spate dreapta
         GPIO.output(motor1_2, GPIO.LOW)
         GPIO.output(motor2_1, GPIO.LOW) #spate stanga
         GPIO.output(motor2_2, GPIO.LOW)
         
         GPIO.output(alarm, GPIO.LOW)
         GPIO.output(lanterna, GPIO.HIGH)
         print ("Spate STOP")
         
            
    elif float(data[3]) == 1:
       print "drepata"
       GPIO.output(motor1_1, GPIO.LOW) #spate dreapta
       GPIO.output(motor1_2, GPIO.HIGH)
       GPIO.output(motor2_1, GPIO.LOW) #spate stanga
       GPIO.output(motor2_2, GPIO.LOW)
       
       GPIO.output(alarm, GPIO.LOW)
       GPIO.output(lanterna, GPIO.HIGH)
    elif float(data[4]) == 1:
       print "stanga"  
       GPIO.output(motor1_1, GPIO.LOW) #spate dreapta
       GPIO.output(motor1_2, GPIO.LOW)
       GPIO.output(motor2_1, GPIO.HIGH) #spate stanga
       GPIO.output(motor2_2, GPIO.LOW)
       
       GPIO.output(alarm, GPIO.LOW)
       GPIO.output(lanterna, GPIO.HIGH)
    elif float(data[5]) == 1:
       print "stop"
       GPIO.output(motor1_1, GPIO.LOW) #spate dreapta
       GPIO.output(motor1_2, GPIO.LOW)
       GPIO.output(motor2_1, GPIO.LOW) #spate stanga
       GPIO.output(motor2_2, GPIO.LOW)   
       
       GPIO.output(alarm, GPIO.HIGH)
       GPIO.output(lanterna, GPIO.HIGH) 
    
    
  
    time.sleep(0.01)
except KeyboardInterrupt:
  GPIO.cleanup()  
  # disconnect from server
db.close()