import sys
import time
import serial
import trackerUtils
from _datetime import datetime

class fonaGPS(object):
    global ser
    global piLog
    ser = trackerUtils.openSerialPort()
    piLog = "piTracker-" + str(time.time()) + ".log"
    trackerUtils.initFile(piLog)

    def openGPS(self):
        print("Turning on the GPS\r")
        ser.write(b'AT+CGNSPWR=1\r')  # Turn on the GPS
        time.sleep(1)
        # Check GPS power status is ON!
        while True:
            ser.write(b'AT+CGNSPWR?\r')
            gpsPower = ser.readline()
            if b'1' in gpsPower:
                print("GPS is powered on")
                return True
            else:
                print("GPS has no power")
                print("GPS is off. Turning on...")
                trackerUtils.writeToFile(piLog, ("GPS status is " + gpsPower))
                ser.write(b'AT+CGNSPWR=1')  # Power on GPS module
        time.sleep(0.5)
        ser.write(b'AT+CGNSRST=1\r')  # GPS reset set to hot start mode
        return True
        
    # Check to see if the GPS has aquired any satellites
    def getGPSFix(self):
        print("Checking for GPS Fix")
        ser.write(b'AT+CGPSSTATUS?\r')
        gpsFix = ser.readline()
        while b'+CGPSSTATUS: Location Not Fix' in gpsFix:
            time.sleep(5) # Wait for GPS fix
            ser.write(b'AT+CGPSSTATUS?\r')
        print("GPS location is fixed")
        return True    
        
    # Get GPS Coordinates
    def getGPS(self):
        print("Getting GPS Data\r")
        while True:
            ser.write(b'AT+CGNSINF \r')
            global gpsCoord
            gpsCoord = ser.readline()
            if b'+CGNSINF: ' in gpsCoord:  # 1 = gps fix, 0 = no fisx
                print(gpsCoord)
                return gpsCoord
                return True
            if b'ERROR' in gpsCoord:
                trackerUtils.writeToFile(piLog, ("Error in GPS Coord: " + gpsCoord))
                ser.write(b'AT+CGNSINF=0\r')

    # converts Rx data to Decimal Degree format
    def convertGPS(self, gpsV1):
        global deg
        deg = chr(37)
        array = gpsV1.split(b',')
        #### Format from DDMM.MMMMMM to DD MM.MMMMMM
        # Latitude
        global latDeg
        global latMin
        lat = array[1]  # text array pull latitude from input
        floatLat = float(lat)  # text to float
        floatLat = floatLat / 100  # float math
        strLat = str(floatLat)  # DD to string
        arrayLat = strLat.split(".")  # split string along .
        latDeg = arrayLat[0]  # DD array member
        latDeg = float(latDeg)
        latMin = arrayLat[1]  # MMMMMM array member
        latMin = float(latMin)  # str to float
        latMin = latMin / 60                  
        latMin = latMin / 10000               
        latitude = latDeg + latMin
        latitude = str(latitude)
        print(latitude + " is decimal degree latitude")
    
        # Longitude
        global lonDeg
        global lonMin
        lon = array[2]  # text array pulling longitude from ,,,
        floatLon = float(lon)  # text to float
        floatLon = floatLon / 100  # float math
        strLon = str(floatLon)
        arrayLon = strLon.split(".")  # split DDMM.MMMM to DD.MMMMMMM along .
        lonDeg = arrayLon[0]  # lonDeg = DD
        lonDeg = float(lonDeg)              
        lonMin = arrayLon[1]  # lonMin = MMMMMM
        lonMin = float(lonMin)  # str to float
        lonMin = lonMin / 60
        lonMin = lonMin / 10000
        longitude = lonDeg + lonMin
        longitude = str(longitude)
        print(longitude + " is decimal degree longitude")
    
        # Altitude
        global alt
        alt = array[3]
        print(b'GPS Altitude is ' + alt)
    
        # Time UTC
        global utc
        utc = array[4]
        print(b'UTC time is ' + utc)
    
        # Speed in knots
        global speed
        speed = array[7]
        print(b'speed in knots is ' + speed)
    
        # Heading in Degrees
        global heading
        heading = array[8]
        print(b'Heading is ' + heading + b' degrees')
    
        # Write parsed GPS to Log file
        gpsMsg1 = (latitude + "," + longitude + " Fix Coords in Decimal Degree")
        trackerUtils.writeToFile(piLog, gpsMsg1)
        gpsMsg2 = (b'Altitude: ' + alt + b' meters, Speed: ' + speed + b' knots, Heading: ' + heading + b' Time: ' + utc + b' UTC')
        trackerUtils.writeToFile(piLog, str(gpsMsg2)) 
        
        # Google Maps link
        global gMapsLink
        gMapsLink = ("https://www.google.com/maps/@" + latitude + "," + longitude)
        print(gMapsLink)
        return gMapsLink
    
        # Close GPS
        def closeGPS():
            ser.write(b'AT+CGNSPWR=0')        # Probably won't need, but hey...
            ser.close()
