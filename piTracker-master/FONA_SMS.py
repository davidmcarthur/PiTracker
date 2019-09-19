import sys
import time
import serial
import trackerUtils

class fonaSMS(object):
    global ctrlZ
    ctrlZ = '\x1a'
        
    global ser
    global piLog
    ser = trackerUtils.openSerialPort()
    piLog = "piTracker-" + str(time.time()) + ".log"
    trackerUtils.initFile(piLog)

    # CHECK FONA
    def checkFONA(self):
        # SETUP SERIAL MODEM FOR PI/FONA
        while True:
            ser.write(b'AT\r')
            fonaStatus = ser.readline()
            if b'OK' in fonaStatus:
                print(b'The FONA is ' + fonaStatus)
                return True
            if b'ERROR' in fonaStatus:
                trackerUtils.writeToFile(piLog, ("FONA status is " + fonaStatus)) 
                print(b'The FONA is ' + fonaStatus)
        return True
            
    def initSMS(self):
        smsStatus = "SMS Status Default"
        while True:
            ser.write(b'AT+CMGF=1\r')            # Set SMS mode to TEXT
            smsStatus = ser.readline()
            if b'OK' in smsStatus:
                print(b'SMS status is ' + smsStatus)
                return True
            if b'ERROR' in smsStatus:
                trackerUtils.writeToFile(piLog, (("SMS status is " + smsStatus)))
                ser.write(b'AT+CMGF=1\r')
            time.sleep(1)
    
    # Send SMS
    def sendSMS(self, recipient, message):
        try:
            def get_num(x):
                return str("".join(ele for ele in x if ele.isdigit()))
        
            time.sleep(0.5)
            ser.write(b'AT\r\n')
            print(ser.readline())
            time.sleep(0.5)
            ser.write(b'AT+CMGF=1\r\n')
            time.sleep(0.5)
            ser.write(('AT+CMGS="'+ recipient +'"\r\n').encode())
            out = ''
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1).decode()
            if out != '':
                print('>>' + out)
            ser.write((message).encode())
            ser.write(b'\x1a')
            out = ''
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1).decode()
            #if out != '':
            #    print('>>' + out)
            #    number = get_num(out)
            #    ser.write(('AT+CMSS='+number+'\r\n').encode())
            out = ''
            time.sleep(1)
            #while ser.inWaiting() > 0:
            #    out += ser.read(1).decode()
            #if out != '':
            #    print('>>' + out)
            #print("Sending SMS message " + smsMessage + " to " + smsRecipient)
            #ser.write('ATZ') # Reset the FONA
            #ser.write('AT+CMGF=1\r\n')
            #sleep(0.5)
            #ser.write('AT+CMGS=')
            #ser.write(smsRecipient)
            #ser.write('\r\n')
            #ser.write(smsMessage.encode())
            #ser.write('\x1a')
            #sleep(3)
            #smsStatus = ser.readlines()
            #while "OK" in smsStatus:
            #    print("Sending status is: " + smsStatus)
        finally:
            ser.close()