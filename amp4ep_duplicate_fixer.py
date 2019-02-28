#This python script is intended to delete duplicated AMP for EndPoint hostnames.

#The script executes as follows: Enter AMP4E - API Credentials -> Search all hostnames -> Create hostname duplicate list -> Query duplicate install date -> delete dated hostname. After the script runs, check AMP4E Console > Accounts > Audit Log, for changes the script performed.

#Authors: Max Wijnbladh and Chris Maxwell

import json
import requests
import urllib3
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import sys
import time
import ConfigParser

#parameters:

#Update parameters
client_id = "<<Enter Client ID>>"
api_key = "<<Enter API Key>>"
guid = "<<Enter GUID>>"
sleep_time = 5
auth_string = ""

<<<<<<< HEAD
def authenticate():

	global auth_string

	auth_string = "https://{}:{}@api.amp.cisco.com".format(client_id, api_key)
	#print (auth_string)

	url = auth_string + "/v1/computers" #JSON parse data
	r =  requests.request("GET", url)
	if r.status_code == 200:
		json_data = r.json()
		return json_data
	else:
		print ("Unable to authenticate, response code: {}".format(r.status_code))
		exit()

#script main start
def main():

	init_params()
	#run this forever

	while(1):
		os.system("clear")
		print("______________________________________")
		print('\nAMP4E Duplicate Fixer')
		print("______________________________________\n")
		print("Getting endpoints")
		spinner = spinning_cursor()
		for _ in range(5):
				sys.stdout.write(next(spinner))
				sys.stdout.flush()
				time.sleep(0.5)
				sys.stdout.write("\a")
		json_data = authenticate()
		endpoints = get_endpoints(json_data)
		print("Finding duplicates")
		duplicates = find_duplicates(endpoints)
		if duplicates == []:
			print ("No duplicates found")
		else:
			oldest = find_oldest_duplicates(duplicates)
			print("Removing duplicates")
			delete_endpoints(oldest)
			print("Posting to AMP Console")
			#console_post(guid_post)
		print("\nWaiting for next scan")
		time.sleep(sleep_time)


def init_params():
    """
    Screen which allows the user to choose how to enter parameters for the script runtime.
    current options are by entering the information manually, or by reading them from the config.ini
    file.

    """
    config_path = "config.ini"
    global client_id
    global api_key
    global sleep_time

    print("______________________________________")
    print('\nAMP4E Duplicate Fixer')
    print("______________________________________\n")

    op = raw_input("Enter settings manually? [y/n]")

    if (op == "y"):

        temp = raw_input("Client ID:")
        if (temp != ""):
            client_id = temp

        temp = raw_input("API Key:")
        if (temp != ""):
            api_key = temp

        temp = raw_input("Scanning Interval (hours):")
        if (temp != ""):
            sleep_time = float(temp) * 60

    elif (op == "n"):
		temp = raw_input("Enter relative path to config file ['/config.ini']")
		if (temp != ""):
			config_path = temp
		config = ConfigParser.ConfigParser()
		config.read(config_path)

		client_id = config.get("Parameters", "clientID")
		api_key = config.get("Parameters", "apiKey")
		sleep_time = config.get("Parameters", "scanInterval")
		sleep_time = float(sleep_time) * 60
		auth_string  = "https://{}:{}@api.amp.cisco.com".format(client_id, api_key)

def spinning_cursor(): #Cisco Loading bar
	while True:
		for cursor in '.:|:.':
			yield cursor

def authenticate(): #Authenticate with AMP4E API Credentials

	auth_string = "https://{}:{}@api.amp.cisco.com".format(client_id, api_key)
	#print (auth_string)

	url = auth_string + "/v1/computers" #JSON parse data
	r =  requests.request("GET", url)
	if r.status_code == 200:
		print(" Successfully authenticated you with the AMP Console!")
		json_data = r.json()
		return json_data
	else:
		print (" Unable to authenticate you with the AMP Console, response code: {}".format(r.status_code))
		exit()


def get_endpoints(json_data): #RETURNS: dict[guid]=[hostname,install date]
	endpoints = {}

	#get all endpoints stored in amp portal
	for host in json_data["data"]:
		endpoints[host["connector_guid"]] = [host['hostname'], host["install_date"]]

	return endpoints #create dict with all endpoints

#RETURNS: dict
def find_duplicates(endpoints):

	hostnames = []
	duplicate_hosts = []

	final_dict = {}

	for key in endpoints:
		hostname = endpoints[key][0]
		if hostname in hostnames:
			duplicate_hosts.append(hostname)
		else:
			hostnames.append(hostname)

	for key in endpoints:
		hostname = endpoints[key][0]
		if hostname in duplicate_hosts:
			duple = (key, endpoints[key][1])
			try:
				final_dict[hostname].append(duple)
			except:
				final_dict[hostname] = []
				final_dict[hostname].append(duple)

	return final_dict



#RETURN dict
def find_oldest_duplicates(duplicates):

	youngest = {}
	oldest = []

	for key in duplicates:
		for tuples in duplicates[key]:
			guid = tuples[0]
			age = tuples[1]
			try:
				if (datetime.strptime(age, '%Y-%m-%dT%H:%M:%SZ') > datetime.strptime(youngest[key][1], '%Y-%m-%dT%H:%M:%SZ')):
					#print(str(datetime.strptime(age, '%Y-%m-%dT%H:%M:%SZ')) + "is younger than " + str(youngest[key][1]))
					youngest[key] = (guid, age)
				else:
					#print(str(datetime.strptime(age, '%Y-%m-%dT%H:%M:%SZ')) + "is older than " + str(youngest[key][1]))
					pass
			except Exception as e:
				#print(e) 
				youngest[key] = (guid, age)
				#print("youngest key is " + str(age))

	for key in duplicates:
		for tuples in duplicates[key]:
			if tuples[0] != youngest[key][0] and key == "localhost.localdomain":
				oldest.append(tuples[0])

	return oldest

#RETURN NONE
def delete_endpoints(duplicates):

	for guid in duplicates:
		url = auth_string + "/v1/computers/" + guid
		print guid
		response =  requests.request("DELETE", url)

if __name__ == '__main__':
	main()
