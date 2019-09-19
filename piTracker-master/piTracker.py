import serial
from curses.ascii import ascii
from time import sleep
from FONA_GPS import fonaGPS
from FONA_SMS import fonaSMS
import trackerUtils
    
#Get GPS Data
GPSData = fonaGPS()
GPSData.openGPS()
GPSData.getGPSFix()
rawGPS = GPSData.getGPS()
fullLocData = GPSData.convertGPS(rawGPS)

conn = trackerUtils.initDB()

db = conn.database()
currentData = db.child("current-time").child("moment").get()
print("The current moment is " + str(currentData.val()))


# Send GPS data to text
device = fonaSMS()
device.checkFONA()
device.initSMS()

smsRecipient = "6145882596" #Ron's ser
smsMessage = fullLocData



device.sendSMS(smsRecipient, smsMessage)
