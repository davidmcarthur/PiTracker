# PiTracker

Required parts: FONA 808, Antennas for GPS and GSM, Raspberry Pi 3 or Zero, don't forget a 2G SIM (hopefully they still exist)

Raspbian OS

You will need to enable the UART0 port as it is off by default on the newer Pi.
To correct perform command to "sudo nano config.txt" ensure "enable_uart=1" may need to change config file
sudo nano /boot/config.txt enable_uart=1

For GSM internet you will need a point to point dameon service. 
To install simply:

    pip install python-pppd

Alternatively, install from the repository:

  git clone https://github.com/cour4g3/python-pppd
  cd python-pppd
  python setup.py install


reference: https://www.digikey.com/en/maker/projects/cellular-gps-enabled-pi-3-fona-pi-3/d0cf660bfc144842a49bfbc5c1dc2ff0
