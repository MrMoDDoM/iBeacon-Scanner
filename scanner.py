import blescan
import sys
import os
import bluetooth._bluetooth as bluez
import argparse

parser = argparse.ArgumentParser(description='Reliable Bluetooth LE (iBeacon) scanner')
parser.add_argument('--ID', type=int, default=0, help='Bluetooth adapter ID')
# parser.add_argument('', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

args = parser.parse_args()
#print(args.accumulate(args.integers))

# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray


def printLogo():
	logo = """
    _ ____                                 _____                                 
   (_) __ )___  ____ __________  ____     / ___/_________ _____  ____  ___  _____
  / / __  / _ \/ __ `/ ___/ __ \/ __ \    \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / / /_/ /  __/ /_/ / /__/ /_/ / / / /   ___/ / /__/ /_/ / / / / / / /  __/ /    
/_/_____/\___/\__,_/\___/\____/_/ /_/   /____/\___/\__,_/_/ /_/_/ /_/\___/_/     
                                                                                 
"""
	print logo

def printInfo(str):
	print G + "[INFO]" + str

def printError(str):
	print R + "[ERROR]" + str

def gracefulExit():
	print
	print R + "Quitting... ByeBye!"
	print W
	sys.exit(0)

def badExit():
	print
	print R + "Somethings went wrong...! Quitting!"
	print W
	sys.exit(1)

print O
printLogo()

printInfo("Starting BLE thread on device ID: " + str(args.ID) + "...")
try:
	sock = bluez.hci_open_dev(int(args.ID))

except:
	printError("Error accessing bluetooth device!")
    	badExit()

try:
	printInfo("Setting up BLE device ...")
	blescan.hci_le_set_scan_parameters(sock)

except:
	printError("Error setting up bluetooth device!")
	badExit()

try:
	printInfo("Start scanning...")
	blescan.hci_enable_le_scan(sock)
except:
	printError("Error scanning! Maybe not root?")
	badExit()

while True:
	try:
		returnedList = blescan.parse_events(sock, 10)

		purgedList = []
		seen = set()
		purgedList = []
		for d in returnedList:
		    #t = tuple(d.items())
		    t = d['MAC']
		    if t not in seen:
		        seen.add(t)
		        purgedList.append(d)

		os.system('clear')

		print O
		printLogo()

		print G + "Mac \t\t  UUID \t\t\t\t   MAJOR \t  MINUM \t RSSI \t\t Unknow"
		for beacon in purgedList:
			print beacon['MAC'] ,
			print beacon['UUID'] ,
			print beacon['MAJOR'] ,
			print beacon['MINOR'] ,
			print beacon['RSSI'] ,
			print beacon['UNKNOW']
		print P+"Scanning.... "
	except KeyboardInterrupt:
		print
		printInfo("User press CTRL+C")
		gracefulExit()
	except:
		badExit()





# teams_list = ["Man Utd", "Man City", "T Hotspur"]
# data = np.array([[1, 2, 1],
#                  [0, 1, 0],
#                  [2, 4, 2]])


# row_format ="{:>15}" * (len(teams_list) + 1)
# print row_format.format("", *teams_list)
# for team, row in zip(teams_list, data):
#     print row_format.format(team, *row)