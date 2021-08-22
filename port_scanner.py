#!/bin/python3

import sys # allows to enter command-line arg
import socket # allows to create connections
from datetime import datetime # to timestamp the finding
import re # allows to validate IP addr
import threading


def scanning(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # establishing connection
	socket.defaulttimeout(1) # connection timeout
	print("Checking port {} ...".format(port))
	err = s.connect_ex((taregt, port))
	if err == 0:
		print("Port {} is open".format(port))
		
	s.close()

thread_list = [] # list for threads


# Define target
if len(sys.argv) == 2: # validate ip_addr
	regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$" # compare IP address pattern
	if(re.search(regex, sys.argv[1])):
		f = open("{}.txt".format(sys.argv[1]),"a") # open file & append this file
		target = socket.gethostbyname(sys.argv[1]) # translate hostname to IPv4
	else:
		print("Invalid IP address.")
		print("NOTE: IP address should be in in IPv4.")
		sys.exit()
else:
	print("Invalid no. of arguments.")
	print("Syntax: python3 scanner.py <ip_addr>.")
	sys.exit()
	
# Add a banner
print("-" * 50)
print("Scanning target "+target)
print("Time started: "+str(datetime.now()))
print("-" * 50)

try:
# we can add arp table to get ports in a machine
# we can also use threading to make it fast
	for port in range(1, 65535): # scan all the ports
		thread = threading.Thread(target=scanning, args=(port))
		thread_list.append(thread)
		for thread in thread_list:
			thread.start()
		for thread in thread_list:
			thread.join()
		f.close()
except KeyboardInterrupt:
	print("\nExiting Program.")
	f.close()
	sys.exit()

except socket.gaierror:
	print("\nHostname couldn't resloved.")
	f.close()
	sys.exit()
	
except socket.error:
	print("\nCouldn't connect to a server.")
	f.close()
	sys.exit()